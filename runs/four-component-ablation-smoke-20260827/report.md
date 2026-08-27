# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| four_ablate_action_policy | 16 | 0.062 | 0.050 | 0.625 | 0.500 | 1.000 | 0.593 |
| four_ablate_current_self_state | 16 | 0.062 | 0.050 | 0.625 | 0.500 | 1.000 | 0.593 |
| four_ablate_recent_observed_episodes | 16 | 0.062 | 0.050 | 0.625 | 0.500 | 1.000 | 0.593 |
| four_ablate_stable_persona | 16 | 0.062 | 0.050 | 0.625 | 0.500 | 1.000 | 0.593 |
| four_component_memory | 16 | 0.062 | 0.050 | 0.625 | 0.500 | 1.000 | 0.593 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| four_ablate_action_policy | clinic_lee_emergency_withdrawal | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| four_ablate_action_policy | clinic_world_delivery_cut | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| four_ablate_action_policy | compute_alex_emergency_job | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.500 |
| four_ablate_action_policy | compute_world_cooling_loss | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| four_ablate_action_policy | greenhouse_sensor_false_alarm_recovery | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| four_ablate_action_policy | greenhouse_world_drought | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| four_ablate_action_policy | logistics_priya_emergency_batch | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.500 |
| four_ablate_action_policy | logistics_world_sorter_failure | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| four_ablate_current_self_state | clinic_lee_emergency_withdrawal | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| four_ablate_current_self_state | clinic_world_delivery_cut | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| four_ablate_current_self_state | compute_alex_emergency_job | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.500 |
| four_ablate_current_self_state | compute_world_cooling_loss | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| four_ablate_current_self_state | greenhouse_sensor_false_alarm_recovery | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| four_ablate_current_self_state | greenhouse_world_drought | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| four_ablate_current_self_state | logistics_priya_emergency_batch | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.500 |
| four_ablate_current_self_state | logistics_world_sorter_failure | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| four_ablate_recent_observed_episodes | clinic_lee_emergency_withdrawal | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| four_ablate_recent_observed_episodes | clinic_world_delivery_cut | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| four_ablate_recent_observed_episodes | compute_alex_emergency_job | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.500 |
| four_ablate_recent_observed_episodes | compute_world_cooling_loss | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| four_ablate_recent_observed_episodes | greenhouse_sensor_false_alarm_recovery | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| four_ablate_recent_observed_episodes | greenhouse_world_drought | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| four_ablate_recent_observed_episodes | logistics_priya_emergency_batch | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.500 |
| four_ablate_recent_observed_episodes | logistics_world_sorter_failure | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| four_ablate_stable_persona | clinic_lee_emergency_withdrawal | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| four_ablate_stable_persona | clinic_world_delivery_cut | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| four_ablate_stable_persona | compute_alex_emergency_job | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.500 |
| four_ablate_stable_persona | compute_world_cooling_loss | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| four_ablate_stable_persona | greenhouse_sensor_false_alarm_recovery | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| four_ablate_stable_persona | greenhouse_world_drought | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| four_ablate_stable_persona | logistics_priya_emergency_batch | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.500 |
| four_ablate_stable_persona | logistics_world_sorter_failure | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| four_component_memory | clinic_lee_emergency_withdrawal | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| four_component_memory | clinic_world_delivery_cut | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| four_component_memory | compute_alex_emergency_job | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.500 |
| four_component_memory | compute_world_cooling_loss | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| four_component_memory | greenhouse_sensor_false_alarm_recovery | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| four_component_memory | greenhouse_world_drought | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| four_component_memory | logistics_priya_emergency_batch | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.500 |
| four_component_memory | logistics_world_sorter_failure | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| four_ablate_action_policy | temporary_vs_persistent | 4 | 0.250 | 0.050 | 1.000 | 0.500 |
| four_ablate_action_policy | world_vs_other | 12 | 0.000 | 0.050 | 0.500 | 0.500 |
| four_ablate_current_self_state | temporary_vs_persistent | 4 | 0.250 | 0.050 | 1.000 | 0.500 |
| four_ablate_current_self_state | world_vs_other | 12 | 0.000 | 0.050 | 0.500 | 0.500 |
| four_ablate_recent_observed_episodes | temporary_vs_persistent | 4 | 0.250 | 0.050 | 1.000 | 0.500 |
| four_ablate_recent_observed_episodes | world_vs_other | 12 | 0.000 | 0.050 | 0.500 | 0.500 |
| four_ablate_stable_persona | temporary_vs_persistent | 4 | 0.250 | 0.050 | 1.000 | 0.500 |
| four_ablate_stable_persona | world_vs_other | 12 | 0.000 | 0.050 | 0.500 | 0.500 |
| four_component_memory | temporary_vs_persistent | 4 | 0.250 | 0.050 | 1.000 | 0.500 |
| four_component_memory | world_vs_other | 12 | 0.000 | 0.050 | 0.500 | 0.500 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
