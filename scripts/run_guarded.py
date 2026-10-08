"""Run a command and stop it safely if the memory load of the machine reaches a limit (default 85%).

Usage: python scripts/run_guarded.py [--limit 85] [--log results/final_test/run.log] -- bash scripts/run_final_test.sh configs/final_test.yaml
Operational only: it does not touch any computation. On pressure it kills the command's process tree, moves truncated chunk files aside
(scripts/ft_ops.py verify-chunks; finished chunks stay, so the run can resume) and exits with code 3 after writing results/final_test/STOPPED_MEMORY.
"""
import argparse
import ctypes
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


class MemoryStatus(ctypes.Structure):
    _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong), ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong), ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong), ("sullAvailExtendedVirtual", ctypes.c_ulonglong)]


def memory_load():
    s = MemoryStatus()
    s.dwLength = ctypes.sizeof(MemoryStatus)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(s))
    return int(s.dwMemoryLoad)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=85)
    ap.add_argument("--log", default="results/final_test/run.log")
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    a = ap.parse_args()
    cmd = a.cmd[1:] if a.cmd and a.cmd[0] == "--" else a.cmd
    with open(a.log, "a") as log:
        log.write(f"\n##### guarded start {datetime.now().isoformat(timespec='seconds')} (memory limit {a.limit}%, load now {memory_load()}%)\n")
        log.flush()
        p = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT)
        while p.poll() is None:
            if memory_load() >= a.limit:
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True)
                subprocess.run([sys.executable, "scripts/ft_ops.py", "verify-chunks"], stdout=log, stderr=subprocess.STDOUT)
                msg = f"stopped by the memory guard at {memory_load()}% on {datetime.now().isoformat(timespec='seconds')}; finished chunks are kept"
                Path("results/final_test/STOPPED_MEMORY").write_text(msg + "\n")
                log.write(f"##### {msg}\n")
                sys.exit(3)
            time.sleep(5)
        log.write(f"##### command ended with exit code {p.returncode} at {datetime.now().isoformat(timespec='seconds')}\n")
    sys.exit(p.returncode)


if __name__ == "__main__":
    main()
