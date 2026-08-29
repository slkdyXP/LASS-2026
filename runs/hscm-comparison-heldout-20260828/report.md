# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| evidence_gated_memory_only | 48 | 0.979 | 0.001 | 0.958 | 0.938 | 1.000 | 0.844 |
| hscm_six_module | 48 | 0.938 | 0.000 | 0.917 | 0.938 | 1.000 | 0.828 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| evidence_gated_memory_only | clinic_lee_emergency_withdrawal | 6 | 1.000 | 0.000 | 0.200 | 1.000 | 0.900 |
| evidence_gated_memory_only | clinic_world_delivery_cut | 6 | 1.000 | 0.000 | 0.433 | 0.833 | 0.742 |
| evidence_gated_memory_only | compute_alex_emergency_job | 6 | 1.000 | 0.000 | 0.183 | 1.000 | 0.898 |
| evidence_gated_memory_only | compute_world_cooling_loss | 6 | 1.000 | 0.000 | 0.283 | 1.000 | 0.785 |
| evidence_gated_memory_only | greenhouse_sensor_false_alarm_recovery | 6 | 0.833 | 0.000 | 0.617 | 1.000 | 0.931 |
| evidence_gated_memory_only | greenhouse_world_drought | 6 | 1.000 | 0.000 | 0.317 | 1.000 | 0.810 |
| evidence_gated_memory_only | logistics_priya_emergency_batch | 6 | 1.000 | 0.000 | 0.217 | 0.833 | 0.881 |
| evidence_gated_memory_only | logistics_world_sorter_failure | 6 | 1.000 | 0.011 | 0.600 | 0.833 | 0.807 |
| hscm_six_module | clinic_lee_emergency_withdrawal | 6 | 1.000 | 0.000 | 0.167 | 1.000 | 0.896 |
| hscm_six_module | clinic_world_delivery_cut | 6 | 1.000 | 0.000 | 0.450 | 0.500 | 0.702 |
| hscm_six_module | compute_alex_emergency_job | 6 | 0.667 | 0.000 | 0.133 | 1.000 | 0.808 |
| hscm_six_module | compute_world_cooling_loss | 6 | 1.000 | 0.000 | 0.367 | 1.000 | 0.796 |
| hscm_six_module | greenhouse_sensor_false_alarm_recovery | 6 | 0.833 | 0.000 | 0.533 | 1.000 | 0.921 |
| hscm_six_module | greenhouse_world_drought | 6 | 1.000 | 0.000 | 0.233 | 1.000 | 0.779 |
| hscm_six_module | logistics_priya_emergency_batch | 6 | 1.000 | 0.000 | 0.167 | 1.000 | 0.896 |
| hscm_six_module | logistics_world_sorter_failure | 6 | 1.000 | 0.000 | 0.617 | 1.000 | 0.827 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| evidence_gated_memory_only | temporary_vs_persistent | 12 | 0.917 | 0.000 | 1.000 | 1.000 |
| evidence_gated_memory_only | world_vs_other | 36 | 1.000 | 0.002 | 0.944 | 0.917 |
| hscm_six_module | temporary_vs_persistent | 12 | 0.917 | 0.000 | 1.000 | 1.000 |
| hscm_six_module | world_vs_other | 36 | 0.944 | 0.000 | 0.889 | 0.917 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
