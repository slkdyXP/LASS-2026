# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| evidence_gated_memory_only | 57 | 0.912 | 0.003 | 0.983 | 0.947 | 1.000 | 0.808 |
| four_component_memory | 57 | 0.965 | 0.002 | 1.000 | 0.930 | 1.000 | 0.800 |
| full_history | 57 | 1.000 | 0.000 | 0.983 | 0.947 | 1.000 | 0.863 |
| hscm_external_controller | 57 | 0.965 | 0.001 | 1.000 | 0.912 | 1.000 | 0.811 |
| reflection | 57 | 0.965 | 0.034 | 0.983 | 0.789 | 1.000 | 0.860 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| evidence_gated_memory_only | auction_bob_conditional | 2 | 1.000 | 0.000 | 0.100 | 1.000 | 0.887 |
| evidence_gated_memory_only | auction_other_inferential | 2 | 0.500 | 0.017 | 0.050 | 1.000 | 0.823 |
| evidence_gated_memory_only | auction_self_need_shift | 2 | 0.000 | 0.000 | 0.000 | 1.000 | 0.750 |
| evidence_gated_memory_only | auction_world_inferential | 2 | 1.000 | 0.000 | 0.350 | 1.000 | 0.856 |
| evidence_gated_memory_only | auction_world_shortage | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.850 |
| evidence_gated_memory_only | entity_binding_bob_not_david | 2 | 1.000 | 0.000 | 0.250 | 0.500 | 0.719 |
| evidence_gated_memory_only | epidemic_other_violation | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.800 |
| evidence_gated_memory_only | epidemic_world_variant | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.775 |
| evidence_gated_memory_only | fish_other_inferential | 2 | 0.500 | 0.017 | 0.100 | 1.000 | 0.642 |
| evidence_gated_memory_only | fish_other_shift | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.863 |
| evidence_gated_memory_only | fish_persona_stress | 1 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| evidence_gated_memory_only | fish_world_anomaly_recovery | 2 | 1.000 | 0.000 | 0.750 | 0.500 | 0.906 |
| evidence_gated_memory_only | fish_world_inferential | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| evidence_gated_memory_only | fish_world_regime | 2 | 1.000 | 0.000 | 0.350 | 0.500 | 0.731 |
| evidence_gated_memory_only | grid_bob_overuse | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.863 |
| evidence_gated_memory_only | grid_world_cloud_cover | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.775 |
| evidence_gated_memory_only | long_history_late_world_shift | 2 | 1.000 | 0.033 | 0.150 | 1.000 | 0.777 |
| evidence_gated_memory_only | newcomer_no_group_generalization | 2 | 1.000 | 0.000 | 0.550 | 1.000 | 0.881 |
| evidence_gated_memory_only | public_goods_david_free_rider | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| evidence_gated_memory_only | public_goods_world_multiplier | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| evidence_gated_memory_only | salience_other_storm_named | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.863 |
| evidence_gated_memory_only | salience_world_david_named | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.869 |
| evidence_gated_memory_only | supply_sam_withholding | 2 | 1.000 | 0.000 | 0.550 | 1.000 | 0.881 |
| evidence_gated_memory_only | supply_world_port_delay | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.744 |
| evidence_gated_memory_only | team_carol_effort_drop | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| evidence_gated_memory_only | team_self_capability_drop | 2 | 0.500 | 0.017 | 0.250 | 1.000 | 0.848 |
| evidence_gated_memory_only | team_world_complexity | 2 | 1.000 | 0.000 | 0.350 | 1.000 | 0.794 |
| evidence_gated_memory_only | traffic_david_blockage | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.800 |
| evidence_gated_memory_only | traffic_world_lane_closure | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |
| four_component_memory | auction_bob_conditional | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.900 |
| four_component_memory | auction_other_inferential | 2 | 0.500 | 0.033 | 0.050 | 1.000 | 0.827 |
| four_component_memory | auction_self_need_shift | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.906 |
| four_component_memory | auction_world_inferential | 2 | 1.000 | 0.000 | 0.300 | 0.500 | 0.725 |
| four_component_memory | auction_world_shortage | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| four_component_memory | entity_binding_bob_not_david | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |
| four_component_memory | epidemic_other_violation | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| four_component_memory | epidemic_world_variant | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |
| four_component_memory | fish_other_inferential | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.800 |
| four_component_memory | fish_other_shift | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |
| four_component_memory | fish_persona_stress | 1 | 1.000 | 0.067 | 0.600 | 1.000 | 0.967 |
| four_component_memory | fish_world_anomaly_recovery | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| four_component_memory | fish_world_inferential | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| four_component_memory | fish_world_regime | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| four_component_memory | grid_bob_overuse | 2 | 1.000 | 0.000 | 0.350 | 1.000 | 0.794 |
| four_component_memory | grid_world_cloud_cover | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.775 |
| four_component_memory | long_history_late_world_shift | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |
| four_component_memory | newcomer_no_group_generalization | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| four_component_memory | public_goods_david_free_rider | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| four_component_memory | public_goods_world_multiplier | 2 | 1.000 | 0.000 | 0.150 | 1.000 | 0.769 |
| four_component_memory | salience_other_storm_named | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |
| four_component_memory | salience_world_david_named | 2 | 1.000 | 0.000 | 0.150 | 1.000 | 0.769 |
| four_component_memory | supply_sam_withholding | 2 | 1.000 | 0.000 | 0.450 | 0.000 | 0.681 |
| four_component_memory | supply_world_port_delay | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.738 |
| four_component_memory | team_carol_effort_drop | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.775 |
| four_component_memory | team_self_capability_drop | 2 | 1.000 | 0.000 | 0.350 | 1.000 | 0.919 |
| four_component_memory | team_world_complexity | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.775 |
| four_component_memory | traffic_david_blockage | 2 | 0.500 | 0.000 | 0.100 | 1.000 | 0.700 |
| four_component_memory | traffic_world_lane_closure | 2 | 1.000 | 0.000 | 0.500 | 0.500 | 0.750 |
| full_history | auction_bob_conditional | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.912 |
| full_history | auction_other_inferential | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.863 |
| full_history | auction_self_need_shift | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.912 |
| full_history | auction_world_inferential | 2 | 1.000 | 0.000 | 0.600 | 1.000 | 0.825 |
| full_history | auction_world_shortage | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |
| full_history | entity_binding_bob_not_david | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.863 |
| full_history | epidemic_other_violation | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.838 |
| full_history | epidemic_world_variant | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.869 |
| full_history | fish_other_inferential | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.963 |
| full_history | fish_other_shift | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.963 |
| full_history | fish_persona_stress | 1 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| full_history | fish_world_anomaly_recovery | 2 | 1.000 | 0.000 | 0.800 | 0.500 | 0.912 |
| full_history | fish_world_inferential | 2 | 1.000 | 0.000 | 0.600 | 0.500 | 0.762 |
| full_history | fish_world_regime | 2 | 1.000 | 0.000 | 0.650 | 0.500 | 0.769 |
| full_history | grid_bob_overuse | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| full_history | grid_world_cloud_cover | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |
| full_history | long_history_late_world_shift | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |
| full_history | newcomer_no_group_generalization | 2 | 1.000 | 0.000 | 0.550 | 1.000 | 0.881 |
| full_history | public_goods_david_free_rider | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.912 |
| full_history | public_goods_world_multiplier | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| full_history | salience_other_storm_named | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.850 |
| full_history | salience_world_david_named | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| full_history | supply_sam_withholding | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| full_history | supply_world_port_delay | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| full_history | team_carol_effort_drop | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.912 |
| full_history | team_self_capability_drop | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.912 |
| full_history | team_world_complexity | 2 | 1.000 | 0.000 | 0.500 | 1.000 | 0.812 |
| full_history | traffic_david_blockage | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.838 |
| full_history | traffic_world_lane_closure | 2 | 1.000 | 0.000 | 0.550 | 1.000 | 0.819 |
| hscm_external_controller | auction_bob_conditional | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.900 |
| hscm_external_controller | auction_other_inferential | 2 | 0.500 | 0.033 | 0.000 | 1.000 | 0.821 |
| hscm_external_controller | auction_self_need_shift | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.900 |
| hscm_external_controller | auction_world_inferential | 2 | 1.000 | 0.000 | 0.350 | 1.000 | 0.856 |
| hscm_external_controller | auction_world_shortage | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| hscm_external_controller | entity_binding_bob_not_david | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.844 |
| hscm_external_controller | epidemic_other_violation | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |
| hscm_external_controller | epidemic_world_variant | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.775 |
| hscm_external_controller | fish_other_inferential | 2 | 1.000 | 0.000 | 0.350 | 1.000 | 0.794 |
| hscm_external_controller | fish_other_shift | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.869 |
| hscm_external_controller | fish_persona_stress | 1 | 1.000 | 0.000 | 0.600 | 1.000 | 0.950 |
| hscm_external_controller | fish_world_anomaly_recovery | 2 | 1.000 | 0.000 | 0.600 | 0.500 | 0.887 |
| hscm_external_controller | fish_world_inferential | 2 | 1.000 | 0.000 | 0.250 | 0.500 | 0.719 |
| hscm_external_controller | fish_world_regime | 2 | 0.500 | 0.000 | 0.100 | 0.500 | 0.637 |
| hscm_external_controller | grid_bob_overuse | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.800 |
| hscm_external_controller | grid_world_cloud_cover | 2 | 1.000 | 0.000 | 0.350 | 0.500 | 0.731 |
| hscm_external_controller | long_history_late_world_shift | 2 | 1.000 | 0.000 | 0.350 | 1.000 | 0.856 |
| hscm_external_controller | newcomer_no_group_generalization | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| hscm_external_controller | public_goods_david_free_rider | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| hscm_external_controller | public_goods_world_multiplier | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| hscm_external_controller | salience_other_storm_named | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |
| hscm_external_controller | salience_world_david_named | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.775 |
| hscm_external_controller | supply_sam_withholding | 2 | 1.000 | 0.000 | 0.500 | 1.000 | 0.812 |
| hscm_external_controller | supply_world_port_delay | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| hscm_external_controller | team_carol_effort_drop | 2 | 1.000 | 0.000 | 0.650 | 1.000 | 0.831 |
| hscm_external_controller | team_self_capability_drop | 2 | 1.000 | 0.000 | 0.500 | 1.000 | 0.938 |
| hscm_external_controller | team_world_complexity | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| hscm_external_controller | traffic_david_blockage | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.863 |
| hscm_external_controller | traffic_world_lane_closure | 2 | 1.000 | 0.000 | 0.200 | 0.500 | 0.713 |
| reflection | auction_bob_conditional | 2 | 1.000 | 0.033 | 0.450 | 1.000 | 0.877 |
| reflection | auction_other_inferential | 2 | 0.500 | 0.100 | 0.000 | 0.500 | 0.713 |
| reflection | auction_self_need_shift | 2 | 1.000 | 0.000 | 0.400 | 0.000 | 0.800 |
| reflection | auction_world_inferential | 2 | 1.000 | 0.000 | 0.800 | 0.000 | 0.850 |
| reflection | auction_world_shortage | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.900 |
| reflection | entity_binding_bob_not_david | 2 | 1.000 | 0.000 | 0.750 | 1.000 | 0.969 |
| reflection | epidemic_other_violation | 2 | 1.000 | 0.067 | 0.600 | 0.500 | 0.842 |
| reflection | epidemic_world_variant | 2 | 1.000 | 0.067 | 0.400 | 0.500 | 0.754 |
| reflection | fish_other_inferential | 2 | 1.000 | 0.050 | 0.700 | 1.000 | 0.906 |
| reflection | fish_other_shift | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.963 |
| reflection | fish_persona_stress | 1 | 1.000 | 0.000 | 0.900 | 1.000 | 0.988 |
| reflection | fish_world_anomaly_recovery | 2 | 1.000 | 0.000 | 0.750 | 0.500 | 0.906 |
| reflection | fish_world_inferential | 2 | 1.000 | 0.117 | 0.450 | 0.500 | 0.823 |
| reflection | fish_world_regime | 2 | 1.000 | 0.050 | 0.700 | 0.500 | 0.906 |
| reflection | grid_bob_overuse | 2 | 1.000 | 0.067 | 0.600 | 1.000 | 0.967 |
| reflection | grid_world_cloud_cover | 2 | 1.000 | 0.033 | 0.350 | 1.000 | 0.802 |
| reflection | long_history_late_world_shift | 2 | 1.000 | 0.117 | 0.650 | 1.000 | 0.898 |
| reflection | newcomer_no_group_generalization | 2 | 1.000 | 0.000 | 0.500 | 1.000 | 0.875 |
| reflection | public_goods_david_free_rider | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| reflection | public_goods_world_multiplier | 2 | 1.000 | 0.000 | 0.150 | 1.000 | 0.769 |
| reflection | salience_other_storm_named | 2 | 1.000 | 0.000 | 0.900 | 1.000 | 0.988 |
| reflection | salience_world_david_named | 2 | 1.000 | 0.000 | 0.750 | 1.000 | 0.906 |
| reflection | supply_sam_withholding | 2 | 1.000 | 0.033 | 0.700 | 0.500 | 0.908 |
| reflection | supply_world_port_delay | 2 | 1.000 | 0.033 | 0.500 | 1.000 | 0.758 |
| reflection | team_carol_effort_drop | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| reflection | team_self_capability_drop | 2 | 1.000 | 0.000 | 0.550 | 1.000 | 0.881 |
| reflection | team_world_complexity | 2 | 1.000 | 0.000 | 0.150 | 1.000 | 0.769 |
| reflection | traffic_david_blockage | 2 | 0.500 | 0.033 | 0.200 | 1.000 | 0.721 |
| reflection | traffic_world_lane_closure | 2 | 1.000 | 0.167 | 0.450 | 0.500 | 0.817 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| evidence_gated_memory_only | conditional_other | 2 | 0.500 | 0.017 | 1.000 | 1.000 |
| evidence_gated_memory_only | entity_binding | 2 | 1.000 | 0.000 | 1.000 | 0.500 |
| evidence_gated_memory_only | group_generalization | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| evidence_gated_memory_only | history_pressure | 2 | 1.000 | 0.033 | 1.000 | 1.000 |
| evidence_gated_memory_only | salience_misdirection | 4 | 1.000 | 0.000 | 1.000 | 1.000 |
| evidence_gated_memory_only | self_vs_world | 2 | 0.500 | 0.017 | 1.000 | 1.000 |
| evidence_gated_memory_only | source_attribution | 13 | 0.846 | 0.000 | 1.000 | 0.846 |
| evidence_gated_memory_only | world_vs_other | 30 | 0.967 | 0.001 | 0.967 | 1.000 |
| four_component_memory | conditional_other | 2 | 0.500 | 0.033 | 1.000 | 1.000 |
| four_component_memory | entity_binding | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| four_component_memory | group_generalization | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| four_component_memory | history_pressure | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| four_component_memory | salience_misdirection | 4 | 1.000 | 0.000 | 1.000 | 1.000 |
| four_component_memory | self_vs_world | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| four_component_memory | source_attribution | 13 | 1.000 | 0.005 | 1.000 | 1.000 |
| four_component_memory | world_vs_other | 30 | 0.967 | 0.000 | 1.000 | 0.867 |
| full_history | conditional_other | 2 | 1.000 | 0.000 | 0.500 | 1.000 |
| full_history | entity_binding | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| full_history | group_generalization | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| full_history | history_pressure | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| full_history | salience_misdirection | 4 | 1.000 | 0.000 | 1.000 | 1.000 |
| full_history | self_vs_world | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| full_history | source_attribution | 13 | 1.000 | 0.000 | 1.000 | 0.846 |
| full_history | world_vs_other | 30 | 1.000 | 0.000 | 1.000 | 0.967 |
| hscm_external_controller | conditional_other | 2 | 0.500 | 0.033 | 1.000 | 1.000 |
| hscm_external_controller | entity_binding | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| hscm_external_controller | group_generalization | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| hscm_external_controller | history_pressure | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| hscm_external_controller | salience_misdirection | 4 | 1.000 | 0.000 | 1.000 | 1.000 |
| hscm_external_controller | self_vs_world | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| hscm_external_controller | source_attribution | 13 | 0.923 | 0.000 | 1.000 | 0.846 |
| hscm_external_controller | world_vs_other | 30 | 1.000 | 0.000 | 1.000 | 0.900 |
| reflection | conditional_other | 2 | 0.500 | 0.100 | 1.000 | 0.500 |
| reflection | entity_binding | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| reflection | group_generalization | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| reflection | history_pressure | 2 | 1.000 | 0.117 | 1.000 | 1.000 |
| reflection | salience_misdirection | 4 | 1.000 | 0.000 | 1.000 | 1.000 |
| reflection | self_vs_world | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| reflection | source_attribution | 13 | 1.000 | 0.013 | 1.000 | 0.692 |
| reflection | world_vs_other | 30 | 0.967 | 0.044 | 0.967 | 0.767 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
