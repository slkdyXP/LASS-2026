# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| evidence_gated_memory_only | 2 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.775 |
| four_component_memory | 2 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.775 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| evidence_gated_memory_only | long_history_late_world_shift | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.775 |
| four_component_memory | long_history_late_world_shift | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.775 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| evidence_gated_memory_only | history_pressure | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| four_component_memory | history_pressure | 2 | 1.000 | 0.000 | 1.000 | 1.000 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
