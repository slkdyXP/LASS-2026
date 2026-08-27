# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| evidence_gated_reflection | 84 | 0.893 | 0.006 | 0.988 | 0.929 | 1.000 | 0.826 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| evidence_gated_reflection | auction_bob_conditional | 6 | 1.000 | 0.000 | 0.200 | 1.000 | 0.900 |
| evidence_gated_reflection | auction_self_need_shift | 6 | 0.167 | 0.000 | 0.050 | 1.000 | 0.777 |
| evidence_gated_reflection | entity_binding_bob_not_david | 6 | 1.000 | 0.000 | 0.333 | 1.000 | 0.833 |
| evidence_gated_reflection | epidemic_other_violation | 6 | 0.833 | 0.028 | 0.333 | 1.000 | 0.776 |
| evidence_gated_reflection | fish_other_shift | 6 | 1.000 | 0.000 | 0.450 | 1.000 | 0.848 |
| evidence_gated_reflection | fish_world_anomaly_recovery | 6 | 1.000 | 0.000 | 0.783 | 0.833 | 0.952 |
| evidence_gated_reflection | fish_world_regime | 6 | 1.000 | 0.000 | 0.450 | 0.667 | 0.806 |
| evidence_gated_reflection | grid_bob_overuse | 6 | 1.000 | 0.000 | 0.517 | 1.000 | 0.877 |
| evidence_gated_reflection | long_history_late_world_shift | 6 | 1.000 | 0.000 | 0.183 | 0.833 | 0.752 |
| evidence_gated_reflection | public_goods_david_free_rider | 6 | 1.000 | 0.000 | 0.383 | 1.000 | 0.819 |
| evidence_gated_reflection | public_goods_world_multiplier | 6 | 1.000 | 0.000 | 0.267 | 1.000 | 0.783 |
| evidence_gated_reflection | salience_other_storm_named | 6 | 1.000 | 0.000 | 0.500 | 1.000 | 0.875 |
| evidence_gated_reflection | team_self_capability_drop | 6 | 0.500 | 0.056 | 0.017 | 1.000 | 0.829 |
| evidence_gated_reflection | traffic_world_lane_closure | 6 | 1.000 | 0.000 | 0.250 | 0.667 | 0.740 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| evidence_gated_reflection | entity_binding | 6 | 1.000 | 0.000 | 1.000 | 1.000 |
| evidence_gated_reflection | history_pressure | 6 | 1.000 | 0.000 | 1.000 | 0.833 |
| evidence_gated_reflection | salience_misdirection | 6 | 1.000 | 0.000 | 1.000 | 1.000 |
| evidence_gated_reflection | self_vs_world | 6 | 0.500 | 0.056 | 1.000 | 1.000 |
| evidence_gated_reflection | source_attribution | 30 | 0.833 | 0.000 | 1.000 | 0.900 |
| evidence_gated_reflection | world_vs_other | 30 | 0.967 | 0.006 | 0.967 | 0.933 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
