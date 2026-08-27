# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| direct | 84 | 0.917 | 0.004 | 1.000 | 0.893 | 1.000 | 0.858 |
| full_history | 84 | 0.941 | 0.001 | 1.000 | 0.905 | 1.000 | 0.871 |
| reflection | 84 | 0.774 | 0.059 | 0.976 | 0.762 | 1.000 | 0.830 |
| summary | 84 | 0.869 | 0.015 | 1.000 | 0.833 | 1.000 | 0.850 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| direct | auction_bob_conditional | 6 | 1.000 | 0.000 | 0.383 | 1.000 | 0.902 |
| direct | auction_self_need_shift | 6 | 0.667 | 0.033 | 0.200 | 1.000 | 0.867 |
| direct | entity_binding_bob_not_david | 6 | 1.000 | 0.000 | 0.467 | 1.000 | 0.871 |
| direct | epidemic_other_violation | 6 | 1.000 | 0.000 | 0.517 | 1.000 | 0.877 |
| direct | fish_other_shift | 6 | 1.000 | 0.000 | 0.517 | 1.000 | 0.877 |
| direct | fish_world_anomaly_recovery | 6 | 1.000 | 0.000 | 0.667 | 0.500 | 0.896 |
| direct | fish_world_regime | 6 | 1.000 | 0.000 | 0.317 | 0.500 | 0.748 |
| direct | grid_bob_overuse | 6 | 1.000 | 0.000 | 0.800 | 1.000 | 0.954 |
| direct | long_history_late_world_shift | 6 | 1.000 | 0.000 | 0.317 | 0.833 | 0.769 |
| direct | public_goods_david_free_rider | 6 | 1.000 | 0.000 | 0.683 | 1.000 | 0.940 |
| direct | public_goods_world_multiplier | 6 | 1.000 | 0.000 | 0.367 | 1.000 | 0.796 |
| direct | salience_other_storm_named | 6 | 1.000 | 0.000 | 0.800 | 0.833 | 0.954 |
| direct | team_self_capability_drop | 6 | 0.333 | 0.022 | -0.033 | 0.833 | 0.772 |
| direct | traffic_world_lane_closure | 6 | 0.833 | 0.000 | 0.433 | 1.000 | 0.783 |
| full_history | auction_bob_conditional | 6 | 1.000 | 0.000 | 0.333 | 1.000 | 0.917 |
| full_history | auction_self_need_shift | 6 | 1.000 | 0.000 | 0.317 | 1.000 | 0.915 |
| full_history | entity_binding_bob_not_david | 6 | 1.000 | 0.000 | 0.650 | 1.000 | 0.956 |
| full_history | epidemic_other_violation | 6 | 1.000 | 0.000 | 0.700 | 1.000 | 0.900 |
| full_history | fish_other_shift | 6 | 1.000 | 0.000 | 0.583 | 1.000 | 0.885 |
| full_history | fish_world_anomaly_recovery | 6 | 1.000 | 0.000 | 0.750 | 0.500 | 0.906 |
| full_history | fish_world_regime | 6 | 1.000 | 0.000 | 0.617 | 0.500 | 0.765 |
| full_history | grid_bob_overuse | 6 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| full_history | long_history_late_world_shift | 6 | 1.000 | 0.000 | 0.633 | 0.667 | 0.787 |
| full_history | public_goods_david_free_rider | 6 | 1.000 | 0.000 | 0.617 | 1.000 | 0.869 |
| full_history | public_goods_world_multiplier | 6 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| full_history | salience_other_storm_named | 6 | 1.000 | 0.000 | 0.733 | 1.000 | 0.967 |
| full_history | team_self_capability_drop | 6 | 0.167 | 0.011 | -0.033 | 1.000 | 0.769 |
| full_history | traffic_world_lane_closure | 6 | 1.000 | 0.000 | 0.367 | 1.000 | 0.796 |
| reflection | auction_bob_conditional | 6 | 0.500 | 0.161 | -0.217 | 0.833 | 0.732 |
| reflection | auction_self_need_shift | 6 | 0.667 | 0.000 | 0.433 | 0.667 | 0.846 |
| reflection | entity_binding_bob_not_david | 6 | 1.000 | 0.011 | 0.367 | 1.000 | 0.861 |
| reflection | epidemic_other_violation | 6 | 0.667 | 0.094 | 0.333 | 1.000 | 0.807 |
| reflection | fish_other_shift | 6 | 1.000 | 0.072 | 0.583 | 0.833 | 0.941 |
| reflection | fish_world_anomaly_recovery | 6 | 0.167 | 0.075 | 0.233 | 0.500 | 0.757 |
| reflection | fish_world_regime | 6 | 1.000 | 0.011 | 0.750 | 0.500 | 0.867 |
| reflection | grid_bob_overuse | 6 | 0.833 | 0.078 | 0.400 | 0.833 | 0.861 |
| reflection | long_history_late_world_shift | 6 | 1.000 | 0.044 | 0.700 | 0.500 | 0.863 |
| reflection | public_goods_david_free_rider | 6 | 1.000 | 0.028 | 0.650 | 0.833 | 0.855 |
| reflection | public_goods_world_multiplier | 6 | 1.000 | 0.000 | 0.233 | 1.000 | 0.779 |
| reflection | salience_other_storm_named | 6 | 1.000 | 0.000 | 0.817 | 0.667 | 0.935 |
| reflection | team_self_capability_drop | 6 | 0.000 | 0.183 | -0.517 | 1.000 | 0.710 |
| reflection | traffic_world_lane_closure | 6 | 1.000 | 0.067 | 0.567 | 0.500 | 0.808 |
| summary | auction_bob_conditional | 6 | 1.000 | 0.011 | 0.300 | 1.000 | 0.915 |
| summary | auction_self_need_shift | 6 | 0.500 | 0.006 | 0.183 | 1.000 | 0.837 |
| summary | entity_binding_bob_not_david | 6 | 1.000 | 0.000 | 0.417 | 1.000 | 0.906 |
| summary | epidemic_other_violation | 6 | 1.000 | 0.000 | 0.733 | 0.833 | 0.904 |
| summary | fish_other_shift | 6 | 1.000 | 0.000 | 0.667 | 1.000 | 0.896 |
| summary | fish_world_anomaly_recovery | 6 | 0.667 | 0.017 | 0.667 | 0.500 | 0.860 |
| summary | fish_world_regime | 6 | 1.000 | 0.000 | 0.750 | 0.500 | 0.885 |
| summary | grid_bob_overuse | 6 | 1.000 | 0.022 | 0.583 | 1.000 | 0.933 |
| summary | long_history_late_world_shift | 6 | 1.000 | 0.000 | 0.200 | 0.667 | 0.733 |
| summary | public_goods_david_free_rider | 6 | 1.000 | 0.022 | 0.600 | 1.000 | 0.893 |
| summary | public_goods_world_multiplier | 6 | 1.000 | 0.000 | 0.233 | 1.000 | 0.779 |
| summary | salience_other_storm_named | 6 | 1.000 | 0.000 | 0.733 | 0.667 | 0.904 |
| summary | team_self_capability_drop | 6 | 0.000 | 0.133 | -0.400 | 1.000 | 0.733 |
| summary | traffic_world_lane_closure | 6 | 1.000 | 0.000 | 0.467 | 0.500 | 0.725 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| direct | entity_binding | 6 | 1.000 | 0.000 | 1.000 | 1.000 |
| direct | history_pressure | 6 | 1.000 | 0.000 | 1.000 | 0.833 |
| direct | salience_misdirection | 6 | 1.000 | 0.000 | 1.000 | 0.833 |
| direct | self_vs_world | 6 | 0.333 | 0.022 | 1.000 | 0.833 |
| direct | source_attribution | 30 | 0.933 | 0.007 | 1.000 | 0.800 |
| direct | world_vs_other | 30 | 0.967 | 0.000 | 1.000 | 1.000 |
| full_history | entity_binding | 6 | 1.000 | 0.000 | 1.000 | 1.000 |
| full_history | history_pressure | 6 | 1.000 | 0.000 | 1.000 | 0.667 |
| full_history | salience_misdirection | 6 | 1.000 | 0.000 | 1.000 | 1.000 |
| full_history | self_vs_world | 6 | 0.167 | 0.011 | 1.000 | 1.000 |
| full_history | source_attribution | 30 | 1.000 | 0.000 | 1.000 | 0.800 |
| full_history | world_vs_other | 30 | 1.000 | 0.000 | 1.000 | 1.000 |
| reflection | entity_binding | 6 | 1.000 | 0.011 | 1.000 | 1.000 |
| reflection | history_pressure | 6 | 1.000 | 0.044 | 1.000 | 0.500 |
| reflection | salience_misdirection | 6 | 1.000 | 0.000 | 1.000 | 0.667 |
| reflection | self_vs_world | 6 | 0.000 | 0.183 | 1.000 | 1.000 |
| reflection | source_attribution | 30 | 0.667 | 0.064 | 1.000 | 0.667 |
| reflection | world_vs_other | 30 | 0.900 | 0.053 | 0.933 | 0.833 |
| summary | entity_binding | 6 | 1.000 | 0.000 | 1.000 | 1.000 |
| summary | history_pressure | 6 | 1.000 | 0.000 | 1.000 | 0.667 |
| summary | salience_misdirection | 6 | 1.000 | 0.000 | 1.000 | 0.667 |
| summary | self_vs_world | 6 | 0.000 | 0.133 | 1.000 | 1.000 |
| summary | source_attribution | 30 | 0.833 | 0.007 | 1.000 | 0.800 |
| summary | world_vs_other | 30 | 1.000 | 0.009 | 1.000 | 0.867 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 1
