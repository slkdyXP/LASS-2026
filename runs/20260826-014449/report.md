# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| full_history | 4 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.844 |
| summary | 4 | 1.000 | 0.017 | 1.000 | 1.000 | 1.000 | 0.879 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| full_history | public_goods_david_free_rider | 2 | 1.000 | 0.000 | 0.600 | 1.000 | 0.887 |
| full_history | public_goods_world_multiplier | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.800 |
| summary | public_goods_david_free_rider | 2 | 1.000 | 0.033 | 0.700 | 1.000 | 0.971 |
| summary | public_goods_world_multiplier | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| full_history | world_vs_other | 4 | 1.000 | 0.000 | 1.000 | 1.000 |
| summary | world_vs_other | 4 | 1.000 | 0.017 | 1.000 | 1.000 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
