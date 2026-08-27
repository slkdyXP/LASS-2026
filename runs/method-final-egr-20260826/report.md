# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| evidence_gated_reflection | 84 | 0.893 | 0.002 | 1.000 | 0.845 | 1.000 | 0.815 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| evidence_gated_reflection | auction_bob_conditional | 6 | 1.000 | 0.000 | 0.217 | 1.000 | 0.902 |
| evidence_gated_reflection | auction_self_need_shift | 6 | 0.167 | 0.000 | 0.033 | 1.000 | 0.775 |
| evidence_gated_reflection | entity_binding_bob_not_david | 6 | 1.000 | 0.000 | 0.183 | 1.000 | 0.794 |
| evidence_gated_reflection | epidemic_other_violation | 6 | 1.000 | 0.000 | 0.450 | 1.000 | 0.848 |
| evidence_gated_reflection | fish_other_shift | 6 | 1.000 | 0.000 | 0.433 | 1.000 | 0.867 |
| evidence_gated_reflection | fish_world_anomaly_recovery | 6 | 1.000 | 0.000 | 0.650 | 0.500 | 0.894 |
| evidence_gated_reflection | fish_world_regime | 6 | 1.000 | 0.000 | 0.250 | 0.500 | 0.740 |
| evidence_gated_reflection | grid_bob_overuse | 6 | 1.000 | 0.000 | 0.533 | 1.000 | 0.879 |
| evidence_gated_reflection | long_history_late_world_shift | 6 | 1.000 | 0.000 | 0.200 | 0.667 | 0.733 |
| evidence_gated_reflection | public_goods_david_free_rider | 6 | 1.000 | 0.000 | 0.400 | 0.833 | 0.800 |
| evidence_gated_reflection | public_goods_world_multiplier | 6 | 1.000 | 0.000 | 0.233 | 1.000 | 0.779 |
| evidence_gated_reflection | salience_other_storm_named | 6 | 1.000 | 0.000 | 0.617 | 1.000 | 0.910 |
| evidence_gated_reflection | team_self_capability_drop | 6 | 0.333 | 0.028 | 0.050 | 1.000 | 0.805 |
| evidence_gated_reflection | traffic_world_lane_closure | 6 | 1.000 | 0.000 | 0.167 | 0.333 | 0.688 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| evidence_gated_reflection | entity_binding | 6 | 1.000 | 0.000 | 1.000 | 1.000 |
| evidence_gated_reflection | history_pressure | 6 | 1.000 | 0.000 | 1.000 | 0.667 |
| evidence_gated_reflection | salience_misdirection | 6 | 1.000 | 0.000 | 1.000 | 1.000 |
| evidence_gated_reflection | self_vs_world | 6 | 0.333 | 0.028 | 1.000 | 1.000 |
| evidence_gated_reflection | source_attribution | 30 | 0.833 | 0.000 | 1.000 | 0.800 |
| evidence_gated_reflection | world_vs_other | 30 | 1.000 | 0.000 | 1.000 | 0.833 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
