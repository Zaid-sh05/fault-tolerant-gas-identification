First run (kept unchanged for transparency). Differences from the final run:
- `iterative` imputed values were NOT bounded to the Train range; it diverged on the DR block of
  S03/S04 (RMSE up to 97 standardised units). The final run bounds them.
- `knn` used sklearn KNNImputer directly (~10 min per space); the final run uses an equivalent
  NearestNeighbors implementation (tests/test_imputation.py proves equal output).
All other methods are unchanged and give the same numbers.
