# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| full_history | 6 | 0.833 | 0.028 | 0.833 | 1.000 | 1.000 | 0.771 |
| hscm_external_controller | 6 | 0.667 | 0.056 | 0.667 | 0.500 | 1.000 | 0.701 |
| reflection | 6 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.948 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| full_history | qwen32k_fish_other_saturation | 3 | 0.667 | 0.056 | 0.167 | 1.000 | 0.701 |
| full_history | qwen32k_fish_world_saturation | 3 | 1.000 | 0.000 | 0.400 | 1.000 | 0.842 |
| hscm_external_controller | qwen32k_fish_other_saturation | 3 | 0.333 | 0.111 | -0.267 | 1.000 | 0.620 |
| hscm_external_controller | qwen32k_fish_world_saturation | 3 | 1.000 | 0.000 | 0.600 | 0.000 | 0.783 |
| reflection | qwen32k_fish_other_saturation | 3 | 1.000 | 0.000 | 0.500 | 1.000 | 0.938 |
| reflection | qwen32k_fish_world_saturation | 3 | 1.000 | 0.000 | 0.667 | 1.000 | 0.958 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| full_history | early_evidence_under_irrelevant_load | 6 | 0.833 | 0.028 | 0.833 | 1.000 |
| hscm_external_controller | early_evidence_under_irrelevant_load | 6 | 0.667 | 0.056 | 0.667 | 0.500 |
| reflection | early_evidence_under_irrelevant_load | 6 | 1.000 | 0.000 | 1.000 | 1.000 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
