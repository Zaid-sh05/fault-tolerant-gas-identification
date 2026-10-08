#!/usr/bin/env bash
# The single final-test run. Usage: bash scripts/run_final_test.sh configs/final_test.yaml
# (dry run on Validation: configs/final_test_dryrun.yaml). Stops at the first failing step (set -e): a failure is NOT
# fixed and re-run silently; it is reported to the user. A second start is refused (RUN_STARTED marker).
set -euo pipefail
CFG=${1:?config file}
NAME=test
JOBS=${JOBS:-6}                     # worker processes (operational setting only; the chunking and every result are independent of it)
ROOT=$(python -c "from src.splits import load_config; print(load_config('$CFG')['output_root'])")
mkdir -p "$ROOT"
if [ -e "$ROOT/RUN_STARTED" ]; then echo "refusing to start again: $ROOT/RUN_STARTED exists"; exit 1; fi
date -Iseconds > "$ROOT/RUN_STARTED"
run() { echo "=== $(date -Iseconds) $*"; python -u "$@"; }
run scripts/ft_prepare.py --config "$CFG" --name $NAME
run scripts/ov2_faults_g1.py --config "$CFG" --name $NAME --jobs "$JOBS"
run scripts/ov3_detector.py --config "$CFG" --name $NAME --jobs "$JOBS" --frozen-choice results/overnight/temporal/g2_verdict.json
run scripts/ov4_strategies.py --config "$CFG" --name $NAME --jobs "$JOBS"
run scripts/ov4_analysis.py --config "$CFG" --name $NAME --jobs "$JOBS"
run scripts/ov4_clean_reference.py --config "$CFG" --name $NAME
run scripts/ft_analysis.py --config "$CFG" --name $NAME --jobs "$JOBS"
run scripts/ft_detector.py --config "$CFG" --name $NAME --jobs "$JOBS"
run scripts/ft_s01s02.py --config "$CFG" --name $NAME
date -Iseconds > "$ROOT/RUN_FINISHED"
echo "=== finished"
