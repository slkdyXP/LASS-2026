# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| hscm_external_controller | 4 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.791 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| hscm_external_controller | compute_world_cooling_loss | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.800 |
| hscm_external_controller | long_history_late_world_shift | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| hscm_external_controller | history_pressure | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| hscm_external_controller | world_vs_other | 2 | 1.000 | 0.000 | 1.000 | 1.000 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
