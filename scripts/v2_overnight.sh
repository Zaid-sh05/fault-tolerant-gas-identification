#!/usr/bin/env bash
# Overnight chain (decisions_log K2). Waits for the running arbiter, then: report with retention, refactor check,
# recalibration stage 1, then stage 2 if J4 allows. Each computation under the memory guard. Stops at the first failure.
# Usage: bash scripts/v2_overnight.sh "<path to venv python.exe>"
set -euo pipefail
PY=${1:?python path}
LOG=results/v2/overnight.log
say() { echo "=== $(date -Iseconds) $*" | tee -a "$LOG"; }
say "waiting for the arbiter run"
until grep -qE "command ended|stopped by" results/v2/arbiter_run.log; do sleep 30; done
grep -q "command ended with exit code 0" results/v2/arbiter_run.log || { say "arbiter run did not end with exit code 0: STOP"; exit 1; }
say "arbiter tables with retention"
"$PY" -u scripts/v2_arbiter.py --report-only >> "$LOG" 2>&1
say "refactor check"
"$PY" -u scripts/v2_check_refactor.py >> "$LOG" 2>&1
say "recalibration stage 1 (clean)"
"$PY" scripts/run_guarded.py --limit 85 --log results/v2/recal_run.log -- "$PY" -u scripts/v2_recal.py --stage clean --jobs 3
if "$PY" -c "import json,sys; sys.exit(0 if json.load(open('results/v2/recal/choice.json'))['n_star'] else 1)"; then
  say "recalibration stage 2 (faults)"
  "$PY" scripts/run_guarded.py --limit 85 --log results/v2/recal_run.log -- "$PY" -u scripts/v2_recal.py --stage faults --jobs 3
else
  say "J4: calibration does not help; stage 2 not run"
fi
say "chain finished"
