"""Memory guard for an ALREADY RUNNING process tree (decisions_log M1): kills the whole tree if the memory load reaches the limit.

Usage: python scripts/tree_guard.py --pid <root pid> [--limit 85] --log <file>
Ends by itself when the root process is gone. Operational only.
"""
import argparse
import time
from datetime import datetime

from run_guarded import kill_tree, memory_load, process_table


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pid", type=int, required=True)
    ap.add_argument("--limit", type=int, default=85)
    ap.add_argument("--log", required=True)
    a = ap.parse_args()
    with open(a.log, "a") as log:
        log.write(f"##### tree guard on pid {a.pid} from {datetime.now().isoformat(timespec='seconds')} (limit {a.limit}%, load {memory_load()}%)\n")
        log.flush()
        while a.pid in process_table():
            if memory_load() >= a.limit:
                left = kill_tree(a.pid)
                log.write(f"##### tree guard: stopped pid {a.pid} at {memory_load()}% on {datetime.now().isoformat(timespec='seconds')}; "
                          f"still alive: {left or 'none'}\n")
                return 3
            time.sleep(10)
        log.write(f"##### tree guard: pid {a.pid} ended on its own at {datetime.now().isoformat(timespec='seconds')}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
