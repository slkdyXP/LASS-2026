# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| hscm_external_controller | 4 | 0.750 | 0.042 | 0.750 | 1.000 | 1.000 | 0.760 |
| reflection | 4 | 0.750 | 0.083 | 0.750 | 1.000 | 1.000 | 0.811 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| hscm_external_controller | qwen32k_fish_other_crowding_no_truncation | 2 | 0.500 | 0.083 | 0.000 | 1.000 | 0.646 |
| hscm_external_controller | qwen32k_fish_world_crowding_no_truncation | 2 | 1.000 | 0.000 | 0.500 | 1.000 | 0.875 |
| reflection | qwen32k_fish_other_crowding_no_truncation | 2 | 1.000 | 0.000 | 0.500 | 1.000 | 0.875 |
| reflection | qwen32k_fish_world_crowding_no_truncation | 2 | 0.500 | 0.167 | 0.150 | 1.000 | 0.748 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| hscm_external_controller | early_evidence_under_irrelevant_load | 4 | 0.750 | 0.042 | 0.750 | 1.000 |
| reflection | early_evidence_under_irrelevant_load | 4 | 0.750 | 0.083 | 0.750 | 1.000 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 2
