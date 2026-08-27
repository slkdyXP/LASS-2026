# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| four_ablate_action_policy | 48 | 1.000 | 0.001 | 1.000 | 0.812 | 1.000 | 0.842 |
| four_ablate_current_self_state | 48 | 0.979 | 0.001 | 0.979 | 0.958 | 1.000 | 0.843 |
| four_ablate_recent_observed_episodes | 48 | 0.979 | 0.001 | 0.979 | 0.917 | 1.000 | 0.838 |
| four_ablate_stable_persona | 48 | 0.917 | 0.005 | 0.938 | 0.917 | 1.000 | 0.822 |
| four_component_memory | 48 | 0.979 | 0.001 | 0.958 | 0.979 | 1.000 | 0.841 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| four_ablate_action_policy | clinic_lee_emergency_withdrawal | 6 | 1.000 | 0.000 | 0.450 | 1.000 | 0.910 |
| four_ablate_action_policy | clinic_world_delivery_cut | 6 | 1.000 | 0.000 | 0.550 | 0.500 | 0.756 |
| four_ablate_action_policy | compute_alex_emergency_job | 6 | 1.000 | 0.000 | 0.250 | 1.000 | 0.906 |
| four_ablate_action_policy | compute_world_cooling_loss | 6 | 1.000 | 0.011 | 0.317 | 1.000 | 0.792 |
| four_ablate_action_policy | greenhouse_sensor_false_alarm_recovery | 6 | 1.000 | 0.000 | 0.633 | 1.000 | 0.954 |
| four_ablate_action_policy | greenhouse_world_drought | 6 | 1.000 | 0.000 | 0.367 | 0.167 | 0.692 |
| four_ablate_action_policy | logistics_priya_emergency_batch | 6 | 1.000 | 0.000 | 0.417 | 1.000 | 0.927 |
| four_ablate_action_policy | logistics_world_sorter_failure | 6 | 1.000 | 0.000 | 0.517 | 0.833 | 0.794 |
| four_ablate_current_self_state | clinic_lee_emergency_withdrawal | 6 | 0.833 | 0.006 | 0.167 | 1.000 | 0.856 |
| four_ablate_current_self_state | clinic_world_delivery_cut | 6 | 1.000 | 0.000 | 0.350 | 0.667 | 0.752 |
| four_ablate_current_self_state | compute_alex_emergency_job | 6 | 1.000 | 0.000 | 0.183 | 1.000 | 0.898 |
| four_ablate_current_self_state | compute_world_cooling_loss | 6 | 1.000 | 0.000 | 0.317 | 1.000 | 0.790 |
| four_ablate_current_self_state | greenhouse_sensor_false_alarm_recovery | 6 | 1.000 | 0.000 | 0.633 | 1.000 | 0.954 |
| four_ablate_current_self_state | greenhouse_world_drought | 6 | 1.000 | 0.000 | 0.333 | 1.000 | 0.792 |
| four_ablate_current_self_state | logistics_priya_emergency_batch | 6 | 1.000 | 0.000 | 0.233 | 1.000 | 0.883 |
| four_ablate_current_self_state | logistics_world_sorter_failure | 6 | 1.000 | 0.000 | 0.550 | 1.000 | 0.819 |
| four_ablate_recent_observed_episodes | clinic_lee_emergency_withdrawal | 6 | 0.833 | 0.011 | 0.083 | 1.000 | 0.847 |
| four_ablate_recent_observed_episodes | clinic_world_delivery_cut | 6 | 1.000 | 0.000 | 0.317 | 0.500 | 0.727 |
| four_ablate_recent_observed_episodes | compute_alex_emergency_job | 6 | 1.000 | 0.000 | 0.233 | 1.000 | 0.904 |
| four_ablate_recent_observed_episodes | compute_world_cooling_loss | 6 | 1.000 | 0.000 | 0.383 | 1.000 | 0.798 |
| four_ablate_recent_observed_episodes | greenhouse_sensor_false_alarm_recovery | 6 | 1.000 | 0.000 | 0.667 | 1.000 | 0.958 |
| four_ablate_recent_observed_episodes | greenhouse_world_drought | 6 | 1.000 | 0.000 | 0.233 | 1.000 | 0.779 |
| four_ablate_recent_observed_episodes | logistics_priya_emergency_batch | 6 | 1.000 | 0.000 | 0.233 | 1.000 | 0.904 |
| four_ablate_recent_observed_episodes | logistics_world_sorter_failure | 6 | 1.000 | 0.000 | 0.433 | 0.833 | 0.783 |
| four_ablate_stable_persona | clinic_lee_emergency_withdrawal | 6 | 0.833 | 0.011 | 0.117 | 1.000 | 0.851 |
| four_ablate_stable_persona | clinic_world_delivery_cut | 6 | 1.000 | 0.000 | 0.267 | 0.833 | 0.762 |
| four_ablate_stable_persona | compute_alex_emergency_job | 6 | 0.667 | 0.028 | 0.067 | 1.000 | 0.807 |
| four_ablate_stable_persona | compute_world_cooling_loss | 6 | 1.000 | 0.000 | 0.283 | 1.000 | 0.785 |
| four_ablate_stable_persona | greenhouse_sensor_false_alarm_recovery | 6 | 0.833 | 0.000 | 0.633 | 1.000 | 0.933 |
| four_ablate_stable_persona | greenhouse_world_drought | 6 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| four_ablate_stable_persona | logistics_priya_emergency_batch | 6 | 1.000 | 0.000 | 0.250 | 0.833 | 0.885 |
| four_ablate_stable_persona | logistics_world_sorter_failure | 6 | 1.000 | 0.000 | 0.483 | 0.667 | 0.769 |
| four_component_memory | clinic_lee_emergency_withdrawal | 6 | 0.833 | 0.011 | 0.133 | 1.000 | 0.853 |
| four_component_memory | clinic_world_delivery_cut | 6 | 1.000 | 0.000 | 0.400 | 1.000 | 0.779 |
| four_component_memory | compute_alex_emergency_job | 6 | 1.000 | 0.000 | 0.217 | 1.000 | 0.902 |
| four_component_memory | compute_world_cooling_loss | 6 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| four_component_memory | greenhouse_sensor_false_alarm_recovery | 6 | 1.000 | 0.000 | 0.583 | 1.000 | 0.948 |
| four_component_memory | greenhouse_world_drought | 6 | 1.000 | 0.000 | 0.200 | 1.000 | 0.775 |
| four_component_memory | logistics_priya_emergency_batch | 6 | 1.000 | 0.000 | 0.217 | 1.000 | 0.902 |
| four_component_memory | logistics_world_sorter_failure | 6 | 1.000 | 0.000 | 0.400 | 0.833 | 0.779 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| four_ablate_action_policy | temporary_vs_persistent | 12 | 1.000 | 0.000 | 1.000 | 0.583 |
| four_ablate_action_policy | world_vs_other | 36 | 1.000 | 0.002 | 1.000 | 0.889 |
| four_ablate_current_self_state | temporary_vs_persistent | 12 | 1.000 | 0.000 | 1.000 | 1.000 |
| four_ablate_current_self_state | world_vs_other | 36 | 0.972 | 0.001 | 0.972 | 0.944 |
| four_ablate_recent_observed_episodes | temporary_vs_persistent | 12 | 1.000 | 0.000 | 1.000 | 1.000 |
| four_ablate_recent_observed_episodes | world_vs_other | 36 | 0.972 | 0.002 | 0.972 | 0.889 |
| four_ablate_stable_persona | temporary_vs_persistent | 12 | 0.917 | 0.000 | 1.000 | 1.000 |
| four_ablate_stable_persona | world_vs_other | 36 | 0.917 | 0.006 | 0.917 | 0.889 |
| four_component_memory | temporary_vs_persistent | 12 | 1.000 | 0.000 | 1.000 | 1.000 |
| four_component_memory | world_vs_other | 36 | 0.972 | 0.002 | 0.944 | 0.972 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
