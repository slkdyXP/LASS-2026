# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| evidence_gated_memory_only | 48 | 0.958 | 0.003 | 0.958 | 0.958 | 1.000 | 0.838 |
| evidence_gated_reflection | 48 | 1.000 | 0.001 | 0.958 | 0.938 | 1.000 | 0.852 |
| guarded_reflection | 48 | 0.917 | 0.003 | 0.917 | 0.750 | 1.000 | 0.801 |
| reflection | 48 | 0.729 | 0.098 | 0.875 | 0.729 | 1.000 | 0.795 |
| structured_reflection | 48 | 0.917 | 0.040 | 0.979 | 0.875 | 1.000 | 0.837 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| evidence_gated_memory_only | clinic_lee_emergency_withdrawal | 6 | 1.000 | 0.000 | 0.167 | 1.000 | 0.896 |
| evidence_gated_memory_only | clinic_world_delivery_cut | 6 | 1.000 | 0.011 | 0.167 | 0.667 | 0.711 |
| evidence_gated_memory_only | compute_alex_emergency_job | 6 | 0.833 | 0.000 | 0.150 | 1.000 | 0.852 |
| evidence_gated_memory_only | compute_world_cooling_loss | 6 | 1.000 | 0.000 | 0.633 | 1.000 | 0.829 |
| evidence_gated_memory_only | greenhouse_sensor_false_alarm_recovery | 6 | 1.000 | 0.000 | 0.750 | 1.000 | 0.969 |
| evidence_gated_memory_only | greenhouse_world_drought | 6 | 0.833 | 0.011 | 0.233 | 1.000 | 0.761 |
| evidence_gated_memory_only | logistics_priya_emergency_batch | 6 | 1.000 | 0.000 | 0.183 | 1.000 | 0.877 |
| evidence_gated_memory_only | logistics_world_sorter_failure | 6 | 1.000 | 0.000 | 0.467 | 1.000 | 0.808 |
| evidence_gated_reflection | clinic_lee_emergency_withdrawal | 6 | 1.000 | 0.000 | 0.133 | 1.000 | 0.892 |
| evidence_gated_reflection | clinic_world_delivery_cut | 6 | 1.000 | 0.011 | 0.533 | 1.000 | 0.840 |
| evidence_gated_reflection | compute_alex_emergency_job | 6 | 1.000 | 0.000 | 0.200 | 1.000 | 0.900 |
| evidence_gated_reflection | compute_world_cooling_loss | 6 | 1.000 | 0.000 | 0.367 | 1.000 | 0.796 |
| evidence_gated_reflection | greenhouse_sensor_false_alarm_recovery | 6 | 1.000 | 0.000 | 0.700 | 1.000 | 0.963 |
| evidence_gated_reflection | greenhouse_world_drought | 6 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| evidence_gated_reflection | logistics_priya_emergency_batch | 6 | 1.000 | 0.000 | 0.183 | 0.833 | 0.877 |
| evidence_gated_reflection | logistics_world_sorter_failure | 6 | 1.000 | 0.000 | 0.483 | 0.667 | 0.769 |
| guarded_reflection | clinic_lee_emergency_withdrawal | 6 | 0.833 | 0.000 | 0.167 | 1.000 | 0.854 |
| guarded_reflection | clinic_world_delivery_cut | 6 | 1.000 | 0.000 | 0.333 | 0.500 | 0.750 |
| guarded_reflection | compute_alex_emergency_job | 6 | 0.500 | 0.000 | 0.100 | 1.000 | 0.742 |
| guarded_reflection | compute_world_cooling_loss | 6 | 1.000 | 0.011 | 0.317 | 0.667 | 0.751 |
| guarded_reflection | greenhouse_sensor_false_alarm_recovery | 6 | 1.000 | 0.000 | 0.700 | 1.000 | 0.963 |
| guarded_reflection | greenhouse_world_drought | 6 | 1.000 | 0.000 | 0.150 | 0.000 | 0.644 |
| guarded_reflection | logistics_priya_emergency_batch | 6 | 1.000 | 0.000 | 0.200 | 1.000 | 0.900 |
| guarded_reflection | logistics_world_sorter_failure | 6 | 1.000 | 0.011 | 0.400 | 0.833 | 0.803 |
| reflection | clinic_lee_emergency_withdrawal | 6 | 0.667 | 0.117 | 0.017 | 1.000 | 0.812 |
| reflection | clinic_world_delivery_cut | 6 | 1.000 | 0.044 | 0.633 | 0.500 | 0.838 |
| reflection | compute_alex_emergency_job | 6 | 0.500 | 0.100 | -0.133 | 0.667 | 0.654 |
| reflection | compute_world_cooling_loss | 6 | 1.000 | 0.133 | 0.417 | 0.500 | 0.835 |
| reflection | greenhouse_sensor_false_alarm_recovery | 6 | 0.500 | 0.000 | 0.500 | 1.000 | 0.875 |
| reflection | greenhouse_world_drought | 6 | 0.667 | 0.122 | 0.267 | 0.500 | 0.758 |
| reflection | logistics_priya_emergency_batch | 6 | 0.500 | 0.161 | -0.150 | 0.833 | 0.695 |
| reflection | logistics_world_sorter_failure | 6 | 1.000 | 0.106 | 0.567 | 0.833 | 0.895 |
| structured_reflection | clinic_lee_emergency_withdrawal | 6 | 1.000 | 0.039 | 0.267 | 1.000 | 0.914 |
| structured_reflection | clinic_world_delivery_cut | 6 | 1.000 | 0.044 | 0.350 | 1.000 | 0.801 |
| structured_reflection | compute_alex_emergency_job | 6 | 0.833 | 0.044 | 0.117 | 1.000 | 0.855 |
| structured_reflection | compute_world_cooling_loss | 6 | 1.000 | 0.044 | 0.483 | 0.833 | 0.838 |
| structured_reflection | greenhouse_sensor_false_alarm_recovery | 6 | 0.500 | 0.029 | 0.467 | 1.000 | 0.861 |
| structured_reflection | greenhouse_world_drought | 6 | 1.000 | 0.011 | 0.467 | 0.667 | 0.769 |
| structured_reflection | logistics_priya_emergency_batch | 6 | 1.000 | 0.056 | 0.283 | 0.833 | 0.895 |
| structured_reflection | logistics_world_sorter_failure | 6 | 1.000 | 0.050 | 0.533 | 0.667 | 0.762 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| evidence_gated_memory_only | temporary_vs_persistent | 12 | 0.917 | 0.006 | 1.000 | 1.000 |
| evidence_gated_memory_only | world_vs_other | 36 | 0.972 | 0.002 | 0.944 | 0.944 |
| evidence_gated_reflection | temporary_vs_persistent | 12 | 1.000 | 0.000 | 1.000 | 1.000 |
| evidence_gated_reflection | world_vs_other | 36 | 1.000 | 0.002 | 0.944 | 0.917 |
| guarded_reflection | temporary_vs_persistent | 12 | 1.000 | 0.000 | 1.000 | 0.500 |
| guarded_reflection | world_vs_other | 36 | 0.889 | 0.004 | 0.889 | 0.833 |
| reflection | temporary_vs_persistent | 12 | 0.583 | 0.061 | 1.000 | 0.750 |
| reflection | world_vs_other | 36 | 0.778 | 0.110 | 0.833 | 0.722 |
| structured_reflection | temporary_vs_persistent | 12 | 0.750 | 0.020 | 1.000 | 0.833 |
| structured_reflection | world_vs_other | 36 | 0.972 | 0.046 | 0.972 | 0.889 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
