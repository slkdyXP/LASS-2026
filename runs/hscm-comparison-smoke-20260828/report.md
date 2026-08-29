# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| evidence_gated_memory_only | 16 | 0.062 | 0.050 | 0.625 | 0.500 | 1.000 | 0.593 |
| hscm_six_module | 16 | 0.062 | 0.050 | 0.625 | 0.500 | 1.000 | 0.593 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| evidence_gated_memory_only | clinic_lee_emergency_withdrawal | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| evidence_gated_memory_only | clinic_world_delivery_cut | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| evidence_gated_memory_only | compute_alex_emergency_job | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.500 |
| evidence_gated_memory_only | compute_world_cooling_loss | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| evidence_gated_memory_only | greenhouse_sensor_false_alarm_recovery | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| evidence_gated_memory_only | greenhouse_world_drought | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| evidence_gated_memory_only | logistics_priya_emergency_batch | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.500 |
| evidence_gated_memory_only | logistics_world_sorter_failure | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| hscm_six_module | clinic_lee_emergency_withdrawal | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| hscm_six_module | clinic_world_delivery_cut | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| hscm_six_module | compute_alex_emergency_job | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.500 |
| hscm_six_module | compute_world_cooling_loss | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| hscm_six_module | greenhouse_sensor_false_alarm_recovery | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| hscm_six_module | greenhouse_world_drought | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| hscm_six_module | logistics_priya_emergency_batch | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.500 |
| hscm_six_module | logistics_world_sorter_failure | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| evidence_gated_memory_only | temporary_vs_persistent | 4 | 0.250 | 0.050 | 1.000 | 0.500 |
| evidence_gated_memory_only | world_vs_other | 12 | 0.000 | 0.050 | 0.500 | 0.500 |
| hscm_six_module | temporary_vs_persistent | 4 | 0.250 | 0.050 | 1.000 | 0.500 |
| hscm_six_module | world_vs_other | 12 | 0.000 | 0.050 | 0.500 | 0.500 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
