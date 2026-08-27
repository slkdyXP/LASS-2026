# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| evidence_gated_reflection | 84 | 0.845 | 0.012 | 1.000 | 0.893 | 1.000 | 0.818 |
| guarded_reflection | 84 | 0.833 | 0.014 | 0.964 | 0.857 | 1.000 | 0.797 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| evidence_gated_reflection | auction_bob_conditional | 6 | 1.000 | 0.017 | 0.233 | 1.000 | 0.906 |
| evidence_gated_reflection | auction_self_need_shift | 6 | 0.167 | 0.000 | 0.033 | 1.000 | 0.775 |
| evidence_gated_reflection | entity_binding_bob_not_david | 6 | 1.000 | 0.000 | 0.250 | 1.000 | 0.802 |
| evidence_gated_reflection | epidemic_other_violation | 6 | 1.000 | 0.000 | 0.400 | 1.000 | 0.842 |
| evidence_gated_reflection | fish_other_shift | 6 | 1.000 | 0.000 | 0.450 | 1.000 | 0.848 |
| evidence_gated_reflection | fish_world_anomaly_recovery | 6 | 1.000 | 0.000 | 0.667 | 0.500 | 0.896 |
| evidence_gated_reflection | fish_world_regime | 6 | 1.000 | 0.000 | 0.417 | 0.500 | 0.802 |
| evidence_gated_reflection | grid_bob_overuse | 6 | 1.000 | 0.000 | 0.417 | 1.000 | 0.865 |
| evidence_gated_reflection | long_history_late_world_shift | 6 | 0.667 | 0.000 | 0.367 | 1.000 | 0.754 |
| evidence_gated_reflection | public_goods_david_free_rider | 6 | 1.000 | 0.011 | 0.433 | 1.000 | 0.869 |
| evidence_gated_reflection | public_goods_world_multiplier | 6 | 1.000 | 0.000 | 0.317 | 1.000 | 0.790 |
| evidence_gated_reflection | salience_other_storm_named | 6 | 1.000 | 0.000 | 0.483 | 1.000 | 0.852 |
| evidence_gated_reflection | team_self_capability_drop | 6 | 0.000 | 0.139 | -0.417 | 1.000 | 0.733 |
| evidence_gated_reflection | traffic_world_lane_closure | 6 | 1.000 | 0.000 | 0.200 | 0.500 | 0.713 |
| guarded_reflection | auction_bob_conditional | 6 | 0.833 | 0.050 | 0.133 | 1.000 | 0.879 |
| guarded_reflection | auction_self_need_shift | 6 | 0.500 | 0.000 | 0.267 | 1.000 | 0.846 |
| guarded_reflection | entity_binding_bob_not_david | 6 | 1.000 | 0.000 | 0.317 | 1.000 | 0.810 |
| guarded_reflection | epidemic_other_violation | 6 | 1.000 | 0.000 | 0.233 | 1.000 | 0.779 |
| guarded_reflection | fish_other_shift | 6 | 1.000 | 0.000 | 0.383 | 1.000 | 0.840 |
| guarded_reflection | fish_world_anomaly_recovery | 6 | 1.000 | 0.000 | 0.817 | 0.500 | 0.915 |
| guarded_reflection | fish_world_regime | 6 | 1.000 | 0.000 | 0.533 | 0.500 | 0.796 |
| guarded_reflection | grid_bob_overuse | 6 | 0.667 | 0.050 | 0.233 | 1.000 | 0.750 |
| guarded_reflection | long_history_late_world_shift | 6 | 1.000 | 0.000 | 0.433 | 0.500 | 0.742 |
| guarded_reflection | public_goods_david_free_rider | 6 | 0.833 | 0.011 | 0.283 | 1.000 | 0.767 |
| guarded_reflection | public_goods_world_multiplier | 6 | 1.000 | 0.000 | 0.133 | 1.000 | 0.767 |
| guarded_reflection | salience_other_storm_named | 6 | 1.000 | 0.000 | 0.483 | 1.000 | 0.831 |
| guarded_reflection | team_self_capability_drop | 6 | 0.000 | 0.083 | -0.250 | 1.000 | 0.740 |
| guarded_reflection | traffic_world_lane_closure | 6 | 0.833 | 0.000 | 0.233 | 0.500 | 0.696 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| evidence_gated_reflection | entity_binding | 6 | 1.000 | 0.000 | 1.000 | 1.000 |
| evidence_gated_reflection | history_pressure | 6 | 0.667 | 0.000 | 1.000 | 1.000 |
| evidence_gated_reflection | salience_misdirection | 6 | 1.000 | 0.000 | 1.000 | 1.000 |
| evidence_gated_reflection | self_vs_world | 6 | 0.000 | 0.139 | 1.000 | 1.000 |
| evidence_gated_reflection | source_attribution | 30 | 0.833 | 0.003 | 1.000 | 0.800 |
| evidence_gated_reflection | world_vs_other | 30 | 1.000 | 0.002 | 1.000 | 0.900 |
| guarded_reflection | entity_binding | 6 | 1.000 | 0.000 | 1.000 | 1.000 |
| guarded_reflection | history_pressure | 6 | 1.000 | 0.000 | 1.000 | 0.500 |
| guarded_reflection | salience_misdirection | 6 | 1.000 | 0.000 | 1.000 | 1.000 |
| guarded_reflection | self_vs_world | 6 | 0.000 | 0.083 | 1.000 | 1.000 |
| guarded_reflection | source_attribution | 30 | 0.867 | 0.010 | 1.000 | 0.800 |
| guarded_reflection | world_vs_other | 30 | 0.867 | 0.012 | 0.900 | 0.900 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
