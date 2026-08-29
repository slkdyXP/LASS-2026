# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| hscm_external_controller | 2 | 1.000 | 0.000 | 1.000 | 0.500 | 1.000 | 0.750 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| hscm_external_controller | long_history_late_world_shift | 2 | 1.000 | 0.000 | 0.500 | 0.500 | 0.750 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| hscm_external_controller | history_pressure | 2 | 1.000 | 0.000 | 1.000 | 0.500 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
