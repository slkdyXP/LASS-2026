# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| direct | 42 | 0.929 | 0.005 | 1.000 | 0.929 | 1.000 | 0.873 |
| full_history | 42 | 1.000 | 0.000 | 1.000 | 0.929 | 1.000 | 0.878 |
| reflection | 42 | 0.762 | 0.049 | 0.952 | 0.762 | 1.000 | 0.816 |
| summary | 42 | 0.881 | 0.009 | 1.000 | 0.833 | 1.000 | 0.847 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| direct | auction_self_need_shift | 6 | 0.667 | 0.033 | 0.200 | 1.000 | 0.867 |
| direct | epidemic_other_violation | 6 | 1.000 | 0.000 | 0.517 | 1.000 | 0.877 |
| direct | fish_world_anomaly_recovery | 6 | 1.000 | 0.000 | 0.667 | 0.500 | 0.896 |
| direct | grid_bob_overuse | 6 | 1.000 | 0.000 | 0.800 | 1.000 | 0.954 |
| direct | public_goods_david_free_rider | 6 | 1.000 | 0.000 | 0.683 | 1.000 | 0.940 |
| direct | public_goods_world_multiplier | 6 | 1.000 | 0.000 | 0.367 | 1.000 | 0.796 |
| direct | traffic_world_lane_closure | 6 | 0.833 | 0.000 | 0.433 | 1.000 | 0.783 |
| full_history | auction_self_need_shift | 6 | 1.000 | 0.000 | 0.317 | 1.000 | 0.915 |
| full_history | epidemic_other_violation | 6 | 1.000 | 0.000 | 0.700 | 1.000 | 0.900 |
| full_history | fish_world_anomaly_recovery | 6 | 1.000 | 0.000 | 0.750 | 0.500 | 0.906 |
| full_history | grid_bob_overuse | 6 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| full_history | public_goods_david_free_rider | 6 | 1.000 | 0.000 | 0.617 | 1.000 | 0.869 |
| full_history | public_goods_world_multiplier | 6 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| full_history | traffic_world_lane_closure | 6 | 1.000 | 0.000 | 0.367 | 1.000 | 0.796 |
| reflection | auction_self_need_shift | 6 | 0.667 | 0.000 | 0.433 | 0.667 | 0.846 |
| reflection | epidemic_other_violation | 6 | 0.667 | 0.094 | 0.333 | 1.000 | 0.807 |
| reflection | fish_world_anomaly_recovery | 6 | 0.167 | 0.075 | 0.233 | 0.500 | 0.757 |
| reflection | grid_bob_overuse | 6 | 0.833 | 0.078 | 0.400 | 0.833 | 0.861 |
| reflection | public_goods_david_free_rider | 6 | 1.000 | 0.028 | 0.650 | 0.833 | 0.855 |
| reflection | public_goods_world_multiplier | 6 | 1.000 | 0.000 | 0.233 | 1.000 | 0.779 |
| reflection | traffic_world_lane_closure | 6 | 1.000 | 0.067 | 0.567 | 0.500 | 0.808 |
| summary | auction_self_need_shift | 6 | 0.500 | 0.006 | 0.183 | 1.000 | 0.837 |
| summary | epidemic_other_violation | 6 | 1.000 | 0.000 | 0.733 | 0.833 | 0.904 |
| summary | fish_world_anomaly_recovery | 6 | 0.667 | 0.017 | 0.667 | 0.500 | 0.860 |
| summary | grid_bob_overuse | 6 | 1.000 | 0.022 | 0.583 | 1.000 | 0.933 |
| summary | public_goods_david_free_rider | 6 | 1.000 | 0.022 | 0.600 | 1.000 | 0.893 |
| summary | public_goods_world_multiplier | 6 | 1.000 | 0.000 | 0.233 | 1.000 | 0.779 |
| summary | traffic_world_lane_closure | 6 | 1.000 | 0.000 | 0.467 | 0.500 | 0.725 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| direct | source_attribution | 12 | 0.833 | 0.017 | 1.000 | 0.750 |
| direct | world_vs_other | 30 | 0.967 | 0.000 | 1.000 | 1.000 |
| full_history | source_attribution | 12 | 1.000 | 0.000 | 1.000 | 0.750 |
| full_history | world_vs_other | 30 | 1.000 | 0.000 | 1.000 | 1.000 |
| reflection | source_attribution | 12 | 0.417 | 0.037 | 1.000 | 0.583 |
| reflection | world_vs_other | 30 | 0.900 | 0.053 | 0.933 | 0.833 |
| summary | source_attribution | 12 | 0.583 | 0.011 | 1.000 | 0.750 |
| summary | world_vs_other | 30 | 1.000 | 0.009 | 1.000 | 0.867 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
