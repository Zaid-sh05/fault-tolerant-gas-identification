**Table 3. Reliability detector (median normalisation, thresholds fixed on Train).** (a) isolation AUROC: faulty vs healthy sensor blocks in the same rows, k=1, medium severity. (b) False-alarm rate on clean rows, per sensor-row, per gas, with and without the two replicate sensors S01/S02. (c) Sensors ordered from least to most reliable on clean rows.

(a)

| fault (k=1, medium)   |   Validation |   pooled |    b8 |    b9 |   b10 |
|:----------------------|-------------:|---------:|------:|------:|------:|
| dropout               |        1.000 |    1.000 | 1.000 | 1.000 | 1.000 |
| bias                  |        0.980 |    0.978 | 0.973 | 0.991 | 0.977 |
| stuck                 |        0.937 |    0.948 | 0.906 | 0.963 | 0.950 |
| random                |        0.974 |    0.979 | 0.958 | 0.986 | 0.981 |
| median (G2)           |        0.977 |    0.979 | 0.966 | 0.988 | 0.979 |

(b)

| gas          |   Val all sensors |   Test pooled all sensors |   Test b8 all sensors |   Test b9 all sensors |   Test b10 all sensors |   Val without S01,S02 |   Test pooled without S01,S02 |   Test b8 without S01,S02 |   Test b9 without S01,S02 |   Test b10 without S01,S02 |
|:-------------|------------------:|--------------------------:|----------------------:|----------------------:|-----------------------:|----------------------:|------------------------------:|--------------------------:|--------------------------:|---------------------------:|
| all          |             0.135 |                     0.078 |                 0.152 |                 0.067 |                  0.074 |                 0.032 |                         0.045 |                     0.032 |                     0.051 |                      0.046 |
| Acetaldehyde |             0.141 |                     0.089 |                 0.151 |                 0.123 |                  0.081 |                 0.036 |                         0.045 |                     0.030 |                     0.056 |                      0.045 |
| Acetone      |             0.147 |                     0.113 |                 0.147 |                 0.103 |                  0.107 |                 0.041 |                         0.057 |                     0.025 |                     0.059 |                      0.064 |
| Ammonia      |             0.116 |                     0.083 |                 0.164 |                 0.007 |                  0.090 |                 0.016 |                         0.051 |                     0.045 |                     0.007 |                      0.058 |
| Ethanol      |             0.142 |                     0.035 |                 0.148 |                 0.081 |                  0.025 |                 0.052 |                         0.028 |                     0.026 |                     0.090 |                      0.021 |
| Ethylene     |             0.117 |                     0.067 |                 0.133 |                 0.039 |                  0.067 |                 0.024 |                         0.029 |                     0.019 |                     0.043 |                      0.028 |
| Toluene      |             0.138 |                     0.075 |                 0.201 |                 0.064 |                  0.073 |                 0.015 |                         0.061 |                     0.087 |                     0.062 |                      0.060 |

(c)

|   rank_from_least_reliable | b10   | b8   | b9   | pooled   |
|---------------------------:|:------|:-----|:-----|:---------|
|                          1 | S01   | S01  | S08  | S01      |
|                          2 | S08   | S02  | S16  | S08      |
|                          3 | S07   | S12  | S01  | S07      |
|                          4 | S14   | S09  | S05  | S09      |
|                          5 | S09   | S03  | S02  | S14      |
|                          6 | S12   | S04  | S15  | S16      |
|                          7 | S16   | S08  | S07  | S12      |
|                          8 | S04   | S07  | S03  | S04      |
|                          9 | S15   | S06  | S04  | S15      |
|                         10 | S06   | S16  | S06  | S06      |
|                         11 | S13   | S15  | S12  | S05      |
|                         12 | S05   | S13  | S09  | S03      |
|                         13 | S03   | S05  | S13  | S13      |
|                         14 | S02   | S10  | S14  | S02      |
|                         15 | S11   | S14  | S11  | S11      |
|                         16 | S10   | S11  | S10  | S10      |

Intervals: paired bootstrap over evaluation rows only (1000 resamples), so they are optimistic: they ignore the variation of the fault draw, of the training set and of the batch. Gate G3 passes if a single comparison passes (lenient).
