# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| evidence_gated_reflection | 24 | 1.000 | 0.000 | 1.000 | 0.583 | 1.000 | 0.787 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| evidence_gated_reflection | fish_world_anomaly_recovery | 6 | 1.000 | 0.000 | 0.733 | 0.833 | 0.946 |
| evidence_gated_reflection | fish_world_regime | 6 | 1.000 | 0.000 | 0.367 | 0.667 | 0.796 |
| evidence_gated_reflection | long_history_late_world_shift | 6 | 1.000 | 0.000 | 0.167 | 0.500 | 0.708 |
| evidence_gated_reflection | traffic_world_lane_closure | 6 | 1.000 | 0.000 | 0.267 | 0.333 | 0.700 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| evidence_gated_reflection | history_pressure | 6 | 1.000 | 0.000 | 1.000 | 0.500 |
| evidence_gated_reflection | source_attribution | 12 | 1.000 | 0.000 | 1.000 | 0.750 |
| evidence_gated_reflection | world_vs_other | 6 | 1.000 | 0.000 | 1.000 | 0.333 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
