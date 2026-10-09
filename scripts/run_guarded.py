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


def process_table():
    """{pid: parent pid} of every process (PowerShell CIM; no extra dependency)."""
    out = subprocess.run(["powershell", "-NoProfile", "-Command",
                          "Get-CimInstance Win32_Process | ForEach-Object { \"$($_.ProcessId) $($_.ParentProcessId)\" }"],
                         capture_output=True, text=True).stdout
    return {int(a): int(b) for a, b in (line.split() for line in out.splitlines() if line.strip())}


def descendants(root):
    table, out, todo = process_table(), [], [root]
    while todo:
        p = todo.pop()
        kids = [c for c, parent in table.items() if parent == p and c != p]
        out += kids
        todo += kids
    return out


def kill_tree(root):
    """Kill root and every descendant (children first), then verify. `taskkill /T` alone missed the loky workers behind the venv
    launcher on 2026-10-09 (decisions_log M1). Returns the pids still alive (should be empty)."""
    pids = descendants(root)[::-1] + [root]
    for pid in pids:
        subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True)
    time.sleep(2)
    alive = set(process_table())
    return [p for p in pids if p in alive]


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
                left = kill_tree(p.pid)
                if left:
                    log.write(f"##### WARNING: processes still alive after the kill: {left}" + chr(10))
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
