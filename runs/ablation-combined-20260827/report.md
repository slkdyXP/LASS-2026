# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| ablate_action_policy | 48 | 0.958 | 0.000 | 1.000 | 0.729 | 1.000 | 0.829 |
| ablate_consolidated_models | 48 | 1.000 | 0.004 | 1.000 | 0.979 | 1.000 | 0.846 |
| ablate_current_self_state | 48 | 0.938 | 0.000 | 0.958 | 0.958 | 1.000 | 0.835 |
| ablate_open_hypotheses | 48 | 1.000 | 0.000 | 0.896 | 0.979 | 1.000 | 0.845 |
| ablate_recent_observed_episodes | 48 | 0.958 | 0.001 | 1.000 | 0.875 | 1.000 | 0.855 |
| ablate_stable_persona | 48 | 0.958 | 0.004 | 0.979 | 1.000 | 1.000 | 0.837 |
| evidence_gated_memory_only | 48 | 0.958 | 0.003 | 0.958 | 0.958 | 1.000 | 0.838 |
| evidence_gated_reflection | 48 | 1.000 | 0.001 | 0.958 | 0.938 | 1.000 | 0.852 |
| guarded_reflection | 48 | 0.917 | 0.003 | 0.917 | 0.750 | 1.000 | 0.801 |
| reflection | 48 | 0.729 | 0.098 | 0.875 | 0.729 | 1.000 | 0.795 |
| structured_reflection | 48 | 0.917 | 0.040 | 0.979 | 0.875 | 1.000 | 0.837 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| ablate_action_policy | clinic_lee_emergency_withdrawal | 6 | 1.000 | 0.000 | 0.250 | 1.000 | 0.906 |
| ablate_action_policy | clinic_world_delivery_cut | 6 | 1.000 | 0.000 | 0.650 | 0.500 | 0.873 |
| ablate_action_policy | compute_alex_emergency_job | 6 | 1.000 | 0.000 | 0.200 | 1.000 | 0.900 |
| ablate_action_policy | compute_world_cooling_loss | 6 | 1.000 | 0.000 | 0.367 | 0.833 | 0.796 |
| ablate_action_policy | greenhouse_sensor_false_alarm_recovery | 6 | 0.833 | 0.000 | 0.683 | 1.000 | 0.940 |
| ablate_action_policy | greenhouse_world_drought | 6 | 0.833 | 0.000 | 0.133 | 0.000 | 0.621 |
| ablate_action_policy | logistics_priya_emergency_batch | 6 | 1.000 | 0.000 | 0.217 | 1.000 | 0.881 |
| ablate_action_policy | logistics_world_sorter_failure | 6 | 1.000 | 0.000 | 0.217 | 0.500 | 0.715 |
| ablate_consolidated_models | clinic_lee_emergency_withdrawal | 6 | 1.000 | 0.000 | 0.117 | 1.000 | 0.890 |
| ablate_consolidated_models | clinic_world_delivery_cut | 6 | 1.000 | 0.000 | 0.383 | 1.000 | 0.798 |
| ablate_consolidated_models | compute_alex_emergency_job | 6 | 1.000 | 0.000 | 0.150 | 1.000 | 0.894 |
| ablate_consolidated_models | compute_world_cooling_loss | 6 | 1.000 | 0.028 | 0.283 | 1.000 | 0.790 |
| ablate_consolidated_models | greenhouse_sensor_false_alarm_recovery | 6 | 1.000 | 0.000 | 0.733 | 1.000 | 0.967 |
| ablate_consolidated_models | greenhouse_world_drought | 6 | 1.000 | 0.000 | 0.183 | 1.000 | 0.773 |
| ablate_consolidated_models | logistics_priya_emergency_batch | 6 | 1.000 | 0.000 | 0.200 | 1.000 | 0.879 |
| ablate_consolidated_models | logistics_world_sorter_failure | 6 | 1.000 | 0.000 | 0.383 | 0.833 | 0.777 |
| ablate_current_self_state | clinic_lee_emergency_withdrawal | 6 | 1.000 | 0.000 | 0.183 | 1.000 | 0.898 |
| ablate_current_self_state | clinic_world_delivery_cut | 6 | 1.000 | 0.000 | 0.533 | 0.833 | 0.838 |
| ablate_current_self_state | compute_alex_emergency_job | 6 | 0.833 | 0.000 | 0.167 | 1.000 | 0.854 |
| ablate_current_self_state | compute_world_cooling_loss | 6 | 1.000 | 0.000 | 0.350 | 0.833 | 0.773 |
| ablate_current_self_state | greenhouse_sensor_false_alarm_recovery | 6 | 0.667 | 0.000 | 0.517 | 1.000 | 0.898 |
| ablate_current_self_state | greenhouse_world_drought | 6 | 1.000 | 0.000 | 0.167 | 1.000 | 0.771 |
| ablate_current_self_state | logistics_priya_emergency_batch | 6 | 1.000 | 0.000 | 0.167 | 1.000 | 0.875 |
| ablate_current_self_state | logistics_world_sorter_failure | 6 | 1.000 | 0.000 | 0.367 | 1.000 | 0.775 |
| ablate_open_hypotheses | clinic_lee_emergency_withdrawal | 6 | 1.000 | 0.000 | 0.167 | 1.000 | 0.875 |
| ablate_open_hypotheses | clinic_world_delivery_cut | 6 | 1.000 | 0.000 | 0.500 | 1.000 | 0.750 |
| ablate_open_hypotheses | compute_alex_emergency_job | 6 | 1.000 | 0.000 | 0.167 | 1.000 | 0.896 |
| ablate_open_hypotheses | compute_world_cooling_loss | 6 | 1.000 | 0.000 | 0.400 | 1.000 | 0.800 |
| ablate_open_hypotheses | greenhouse_sensor_false_alarm_recovery | 6 | 1.000 | 0.000 | 0.733 | 1.000 | 0.967 |
| ablate_open_hypotheses | greenhouse_world_drought | 6 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| ablate_open_hypotheses | logistics_priya_emergency_batch | 6 | 1.000 | 0.000 | 0.250 | 1.000 | 0.906 |
| ablate_open_hypotheses | logistics_world_sorter_failure | 6 | 1.000 | 0.000 | 0.417 | 0.833 | 0.781 |
| ablate_recent_observed_episodes | clinic_lee_emergency_withdrawal | 6 | 1.000 | 0.000 | 0.200 | 0.833 | 0.879 |
| ablate_recent_observed_episodes | clinic_world_delivery_cut | 6 | 1.000 | 0.000 | 0.433 | 0.500 | 0.783 |
| ablate_recent_observed_episodes | compute_alex_emergency_job | 6 | 1.000 | 0.000 | 0.183 | 1.000 | 0.898 |
| ablate_recent_observed_episodes | compute_world_cooling_loss | 6 | 1.000 | 0.000 | 0.617 | 1.000 | 0.848 |
| ablate_recent_observed_episodes | greenhouse_sensor_false_alarm_recovery | 6 | 0.667 | 0.000 | 0.517 | 1.000 | 0.898 |
| ablate_recent_observed_episodes | greenhouse_world_drought | 6 | 1.000 | 0.000 | 0.333 | 1.000 | 0.792 |
| ablate_recent_observed_episodes | logistics_priya_emergency_batch | 6 | 1.000 | 0.000 | 0.200 | 0.667 | 0.858 |
| ablate_recent_observed_episodes | logistics_world_sorter_failure | 6 | 1.000 | 0.011 | 0.700 | 1.000 | 0.882 |
| ablate_stable_persona | clinic_lee_emergency_withdrawal | 6 | 1.000 | 0.011 | 0.167 | 1.000 | 0.899 |
| ablate_stable_persona | clinic_world_delivery_cut | 6 | 1.000 | 0.000 | 0.250 | 1.000 | 0.760 |
| ablate_stable_persona | compute_alex_emergency_job | 6 | 1.000 | 0.011 | 0.183 | 1.000 | 0.899 |
| ablate_stable_persona | compute_world_cooling_loss | 6 | 1.000 | 0.011 | 0.383 | 1.000 | 0.801 |
| ablate_stable_persona | greenhouse_sensor_false_alarm_recovery | 6 | 0.667 | 0.000 | 0.533 | 1.000 | 0.900 |
| ablate_stable_persona | greenhouse_world_drought | 6 | 1.000 | 0.000 | 0.183 | 1.000 | 0.773 |
| ablate_stable_persona | logistics_priya_emergency_batch | 6 | 1.000 | 0.000 | 0.150 | 1.000 | 0.873 |
| ablate_stable_persona | logistics_world_sorter_failure | 6 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
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
| ablate_action_policy | temporary_vs_persistent | 12 | 0.833 | 0.000 | 1.000 | 0.500 |
| ablate_action_policy | world_vs_other | 36 | 1.000 | 0.000 | 1.000 | 0.806 |
| ablate_consolidated_models | temporary_vs_persistent | 12 | 1.000 | 0.000 | 1.000 | 1.000 |
| ablate_consolidated_models | world_vs_other | 36 | 1.000 | 0.005 | 1.000 | 0.972 |
| ablate_current_self_state | temporary_vs_persistent | 12 | 0.833 | 0.000 | 1.000 | 1.000 |
| ablate_current_self_state | world_vs_other | 36 | 0.972 | 0.000 | 0.944 | 0.944 |
| ablate_open_hypotheses | temporary_vs_persistent | 12 | 1.000 | 0.000 | 1.000 | 1.000 |
| ablate_open_hypotheses | world_vs_other | 36 | 1.000 | 0.000 | 0.861 | 0.972 |
| ablate_recent_observed_episodes | temporary_vs_persistent | 12 | 0.833 | 0.000 | 1.000 | 1.000 |
| ablate_recent_observed_episodes | world_vs_other | 36 | 1.000 | 0.002 | 1.000 | 0.833 |
| ablate_stable_persona | temporary_vs_persistent | 12 | 0.833 | 0.000 | 1.000 | 1.000 |
| ablate_stable_persona | world_vs_other | 36 | 1.000 | 0.006 | 0.972 | 1.000 |
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
