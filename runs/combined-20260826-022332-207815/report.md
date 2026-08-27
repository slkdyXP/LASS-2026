# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| direct | 57 | 0.965 | 0.000 | 0.965 | 0.912 | 1.000 | 0.837 |
| full_history | 57 | 0.983 | 0.000 | 0.983 | 0.965 | 1.000 | 0.852 |
| recent_window | 57 | 0.965 | 0.002 | 1.000 | 0.930 | 1.000 | 0.856 |
| reflection | 57 | 0.842 | 0.059 | 0.965 | 0.825 | 1.000 | 0.847 |
| retrieval | 57 | 0.965 | 0.002 | 1.000 | 0.912 | 1.000 | 0.851 |
| summary | 57 | 0.912 | 0.003 | 1.000 | 0.912 | 1.000 | 0.846 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| direct | auction_bob_conditional | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.925 |
| direct | auction_other_inferential | 2 | 0.500 | 0.000 | 0.300 | 1.000 | 0.600 |
| direct | auction_self_need_shift | 2 | 1.000 | 0.000 | 0.500 | 1.000 | 0.938 |
| direct | auction_world_inferential | 2 | 1.000 | 0.000 | 0.800 | 0.500 | 0.912 |
| direct | auction_world_shortage | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| direct | entity_binding_bob_not_david | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.863 |
| direct | epidemic_other_violation | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |
| direct | epidemic_world_variant | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.838 |
| direct | fish_other_inferential | 2 | 1.000 | 0.000 | 0.350 | 1.000 | 0.794 |
| direct | fish_other_shift | 2 | 1.000 | 0.000 | 0.600 | 1.000 | 0.950 |
| direct | fish_persona_stress | 1 | 1.000 | 0.000 | 0.800 | 0.000 | 0.725 |
| direct | fish_world_anomaly_recovery | 2 | 1.000 | 0.000 | 0.900 | 0.500 | 0.925 |
| direct | fish_world_inferential | 2 | 1.000 | 0.000 | 0.350 | 1.000 | 0.794 |
| direct | fish_world_regime | 2 | 1.000 | 0.000 | 0.400 | 0.500 | 0.738 |
| direct | grid_bob_overuse | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| direct | grid_world_cloud_cover | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| direct | long_history_late_world_shift | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |
| direct | newcomer_no_group_generalization | 2 | 1.000 | 0.000 | 0.550 | 1.000 | 0.881 |
| direct | public_goods_david_free_rider | 2 | 1.000 | 0.000 | 0.550 | 1.000 | 0.881 |
| direct | public_goods_world_multiplier | 2 | 1.000 | 0.000 | 0.150 | 1.000 | 0.769 |
| direct | salience_other_storm_named | 2 | 1.000 | 0.000 | 0.550 | 1.000 | 0.881 |
| direct | salience_world_david_named | 2 | 1.000 | 0.000 | 0.100 | 1.000 | 0.762 |
| direct | supply_sam_withholding | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.963 |
| direct | supply_world_port_delay | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.719 |
| direct | team_carol_effort_drop | 2 | 1.000 | 0.000 | 0.600 | 1.000 | 0.950 |
| direct | team_self_capability_drop | 2 | 0.500 | 0.000 | 0.100 | 1.000 | 0.825 |
| direct | team_world_complexity | 2 | 1.000 | 0.000 | 0.350 | 1.000 | 0.794 |
| direct | traffic_david_blockage | 2 | 1.000 | 0.000 | 0.550 | 0.500 | 0.819 |
| direct | traffic_world_lane_closure | 2 | 1.000 | 0.000 | 0.500 | 1.000 | 0.812 |
| full_history | auction_bob_conditional | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.912 |
| full_history | auction_other_inferential | 2 | 0.500 | 0.000 | 0.150 | 1.000 | 0.769 |
| full_history | auction_self_need_shift | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.912 |
| full_history | auction_world_inferential | 2 | 1.000 | 0.000 | 0.600 | 1.000 | 0.825 |
| full_history | auction_world_shortage | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| full_history | entity_binding_bob_not_david | 2 | 1.000 | 0.000 | 0.550 | 1.000 | 0.881 |
| full_history | epidemic_other_violation | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.850 |
| full_history | epidemic_world_variant | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.800 |
| full_history | fish_other_inferential | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.963 |
| full_history | fish_other_shift | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.869 |
| full_history | fish_persona_stress | 1 | 1.000 | 0.000 | 0.600 | 1.000 | 0.950 |
| full_history | fish_world_anomaly_recovery | 2 | 1.000 | 0.000 | 0.750 | 0.500 | 0.906 |
| full_history | fish_world_inferential | 2 | 1.000 | 0.000 | 0.350 | 1.000 | 0.794 |
| full_history | fish_world_regime | 2 | 1.000 | 0.000 | 0.550 | 0.500 | 0.756 |
| full_history | grid_bob_overuse | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| full_history | grid_world_cloud_cover | 2 | 1.000 | 0.000 | 0.150 | 1.000 | 0.769 |
| full_history | long_history_late_world_shift | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.775 |
| full_history | newcomer_no_group_generalization | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |
| full_history | public_goods_david_free_rider | 2 | 1.000 | 0.000 | 0.650 | 1.000 | 0.894 |
| full_history | public_goods_world_multiplier | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.775 |
| full_history | salience_other_storm_named | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| full_history | salience_world_david_named | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.775 |
| full_history | supply_sam_withholding | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| full_history | supply_world_port_delay | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.725 |
| full_history | team_carol_effort_drop | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| full_history | team_self_capability_drop | 2 | 1.000 | 0.000 | 0.150 | 1.000 | 0.894 |
| full_history | team_world_complexity | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.838 |
| full_history | traffic_david_blockage | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.850 |
| full_history | traffic_world_lane_closure | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| recent_window | auction_bob_conditional | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.931 |
| recent_window | auction_other_inferential | 2 | 0.500 | 0.050 | -0.050 | 1.000 | 0.819 |
| recent_window | auction_self_need_shift | 2 | 1.000 | 0.000 | 0.350 | 1.000 | 0.919 |
| recent_window | auction_world_inferential | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.838 |
| recent_window | auction_world_shortage | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |
| recent_window | entity_binding_bob_not_david | 2 | 1.000 | 0.000 | 0.600 | 1.000 | 0.950 |
| recent_window | epidemic_other_violation | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.912 |
| recent_window | epidemic_world_variant | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| recent_window | fish_other_inferential | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.963 |
| recent_window | fish_other_shift | 2 | 1.000 | 0.000 | 0.600 | 1.000 | 0.950 |
| recent_window | fish_persona_stress | 1 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| recent_window | fish_world_anomaly_recovery | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| recent_window | fish_world_inferential | 2 | 1.000 | 0.000 | 0.550 | 1.000 | 0.819 |
| recent_window | fish_world_regime | 2 | 1.000 | 0.000 | 0.350 | 0.500 | 0.794 |
| recent_window | grid_bob_overuse | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| recent_window | grid_world_cloud_cover | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.775 |
| recent_window | long_history_late_world_shift | 2 | 1.000 | 0.000 | 0.450 | 0.500 | 0.744 |
| recent_window | newcomer_no_group_generalization | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.800 |
| recent_window | public_goods_david_free_rider | 2 | 1.000 | 0.000 | 0.600 | 1.000 | 0.887 |
| recent_window | public_goods_world_multiplier | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| recent_window | salience_other_storm_named | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| recent_window | salience_world_david_named | 2 | 1.000 | 0.000 | 0.100 | 1.000 | 0.762 |
| recent_window | supply_sam_withholding | 2 | 1.000 | 0.000 | 0.700 | 0.500 | 0.838 |
| recent_window | supply_world_port_delay | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| recent_window | team_carol_effort_drop | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.931 |
| recent_window | team_self_capability_drop | 2 | 0.500 | 0.000 | 0.100 | 1.000 | 0.825 |
| recent_window | team_world_complexity | 2 | 1.000 | 0.000 | 0.550 | 1.000 | 0.819 |
| recent_window | traffic_david_blockage | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |
| recent_window | traffic_world_lane_closure | 2 | 1.000 | 0.000 | 0.300 | 0.500 | 0.725 |
| reflection | auction_bob_conditional | 2 | 0.500 | 0.133 | -0.100 | 1.000 | 0.771 |
| reflection | auction_other_inferential | 2 | 0.000 | 0.200 | -0.300 | 1.000 | 0.613 |
| reflection | auction_self_need_shift | 2 | 0.000 | 0.250 | -0.750 | 0.000 | 0.469 |
| reflection | auction_world_inferential | 2 | 1.000 | 0.033 | 0.600 | 0.000 | 0.771 |
| reflection | auction_world_shortage | 2 | 1.000 | 0.025 | 0.750 | 1.000 | 0.909 |
| reflection | entity_binding_bob_not_david | 2 | 1.000 | 0.050 | 0.500 | 1.000 | 0.887 |
| reflection | epidemic_other_violation | 2 | 0.500 | 0.250 | 0.050 | 0.500 | 0.662 |
| reflection | epidemic_world_variant | 2 | 1.000 | 0.000 | 0.900 | 1.000 | 0.925 |
| reflection | fish_other_inferential | 2 | 1.000 | 0.033 | 0.700 | 1.000 | 0.971 |
| reflection | fish_other_shift | 2 | 1.000 | 0.033 | 0.600 | 1.000 | 0.958 |
| reflection | fish_persona_stress | 1 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| reflection | fish_world_anomaly_recovery | 2 | 0.500 | 0.025 | 0.700 | 0.500 | 0.847 |
| reflection | fish_world_inferential | 2 | 1.000 | 0.033 | 0.700 | 1.000 | 0.971 |
| reflection | fish_world_regime | 2 | 1.000 | 0.000 | 0.800 | 0.500 | 0.912 |
| reflection | grid_bob_overuse | 2 | 0.500 | 0.200 | 0.050 | 1.000 | 0.794 |
| reflection | grid_world_cloud_cover | 2 | 1.000 | 0.000 | 0.350 | 1.000 | 0.856 |
| reflection | long_history_late_world_shift | 2 | 1.000 | 0.000 | 0.600 | 0.500 | 0.825 |
| reflection | newcomer_no_group_generalization | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| reflection | public_goods_david_free_rider | 2 | 1.000 | 0.100 | 0.550 | 1.000 | 0.887 |
| reflection | public_goods_world_multiplier | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| reflection | salience_other_storm_named | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| reflection | salience_world_david_named | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.850 |
| reflection | supply_sam_withholding | 2 | 1.000 | 0.033 | 0.700 | 0.500 | 0.908 |
| reflection | supply_world_port_delay | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.850 |
| reflection | team_carol_effort_drop | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.963 |
| reflection | team_self_capability_drop | 2 | 1.000 | 0.033 | 0.600 | 1.000 | 0.833 |
| reflection | team_world_complexity | 2 | 1.000 | 0.033 | 0.600 | 1.000 | 0.896 |
| reflection | traffic_david_blockage | 2 | 1.000 | 0.033 | 0.450 | 1.000 | 0.877 |
| reflection | traffic_world_lane_closure | 2 | 0.500 | 0.183 | -0.050 | 0.500 | 0.715 |
| retrieval | auction_bob_conditional | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.906 |
| retrieval | auction_other_inferential | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.906 |
| retrieval | auction_self_need_shift | 2 | 0.500 | 0.000 | 0.100 | 1.000 | 0.825 |
| retrieval | auction_world_inferential | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.838 |
| retrieval | auction_world_shortage | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| retrieval | entity_binding_bob_not_david | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.963 |
| retrieval | epidemic_other_violation | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.900 |
| retrieval | epidemic_world_variant | 2 | 1.000 | 0.000 | 0.000 | 1.000 | 0.750 |
| retrieval | fish_other_inferential | 2 | 1.000 | 0.033 | 0.500 | 1.000 | 0.946 |
| retrieval | fish_other_shift | 2 | 1.000 | 0.000 | 0.600 | 1.000 | 0.887 |
| retrieval | fish_persona_stress | 1 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| retrieval | fish_world_anomaly_recovery | 2 | 0.500 | 0.025 | 0.550 | 0.500 | 0.828 |
| retrieval | fish_world_inferential | 2 | 1.000 | 0.000 | 0.550 | 1.000 | 0.819 |
| retrieval | fish_world_regime | 2 | 1.000 | 0.000 | 0.400 | 0.500 | 0.738 |
| retrieval | grid_bob_overuse | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| retrieval | grid_world_cloud_cover | 2 | 1.000 | 0.000 | 0.500 | 1.000 | 0.812 |
| retrieval | long_history_late_world_shift | 2 | 1.000 | 0.000 | 0.550 | 0.500 | 0.756 |
| retrieval | newcomer_no_group_generalization | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.775 |
| retrieval | public_goods_david_free_rider | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.800 |
| retrieval | public_goods_world_multiplier | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| retrieval | salience_other_storm_named | 2 | 1.000 | 0.000 | 0.900 | 0.000 | 0.863 |
| retrieval | salience_world_david_named | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.800 |
| retrieval | supply_sam_withholding | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| retrieval | supply_world_port_delay | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.719 |
| retrieval | team_carol_effort_drop | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| retrieval | team_self_capability_drop | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.925 |
| retrieval | team_world_complexity | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.912 |
| retrieval | traffic_david_blockage | 2 | 1.000 | 0.000 | 0.600 | 1.000 | 0.825 |
| retrieval | traffic_world_lane_closure | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.775 |
| summary | auction_bob_conditional | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.925 |
| summary | auction_other_inferential | 2 | 0.500 | 0.050 | -0.050 | 1.000 | 0.819 |
| summary | auction_self_need_shift | 2 | 0.000 | 0.000 | 0.000 | 1.000 | 0.750 |
| summary | auction_world_inferential | 2 | 1.000 | 0.000 | 0.650 | 1.000 | 0.956 |
| summary | auction_world_shortage | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| summary | entity_binding_bob_not_david | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.863 |
| summary | epidemic_other_violation | 2 | 1.000 | 0.000 | 0.600 | 1.000 | 0.950 |
| summary | epidemic_world_variant | 2 | 1.000 | 0.000 | 0.150 | 1.000 | 0.769 |
| summary | fish_other_inferential | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.963 |
| summary | fish_other_shift | 2 | 1.000 | 0.000 | 0.650 | 1.000 | 0.894 |
| summary | fish_persona_stress | 1 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| summary | fish_world_anomaly_recovery | 2 | 1.000 | 0.000 | 0.800 | 0.500 | 0.912 |
| summary | fish_world_inferential | 2 | 1.000 | 0.000 | 0.750 | 0.500 | 0.906 |
| summary | fish_world_regime | 2 | 1.000 | 0.000 | 0.500 | 0.500 | 0.812 |
| summary | grid_bob_overuse | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.838 |
| summary | grid_world_cloud_cover | 2 | 1.000 | 0.000 | 0.350 | 1.000 | 0.794 |
| summary | long_history_late_world_shift | 2 | 1.000 | 0.000 | 0.150 | 0.500 | 0.706 |
| summary | newcomer_no_group_generalization | 2 | 1.000 | 0.000 | 0.100 | 1.000 | 0.825 |
| summary | public_goods_david_free_rider | 2 | 1.000 | 0.000 | 0.650 | 1.000 | 0.894 |
| summary | public_goods_world_multiplier | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| summary | salience_other_storm_named | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.963 |
| summary | salience_world_david_named | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| summary | supply_sam_withholding | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.900 |
| summary | supply_world_port_delay | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| summary | team_carol_effort_drop | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.900 |
| summary | team_self_capability_drop | 2 | 0.000 | 0.033 | -0.100 | 1.000 | 0.746 |
| summary | team_world_complexity | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |
| summary | traffic_david_blockage | 2 | 1.000 | 0.000 | 0.550 | 1.000 | 0.881 |
| summary | traffic_world_lane_closure | 2 | 1.000 | 0.000 | 0.200 | 0.500 | 0.713 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| direct | conditional_other | 2 | 0.500 | 0.000 | 0.000 | 1.000 |
| direct | entity_binding | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| direct | group_generalization | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| direct | history_pressure | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| direct | salience_misdirection | 4 | 1.000 | 0.000 | 1.000 | 1.000 |
| direct | self_vs_world | 2 | 0.500 | 0.000 | 1.000 | 1.000 |
| direct | source_attribution | 13 | 1.000 | 0.000 | 1.000 | 0.769 |
| direct | world_vs_other | 30 | 1.000 | 0.000 | 1.000 | 0.933 |
| full_history | conditional_other | 2 | 0.500 | 0.000 | 0.500 | 1.000 |
| full_history | entity_binding | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| full_history | group_generalization | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| full_history | history_pressure | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| full_history | salience_misdirection | 4 | 1.000 | 0.000 | 1.000 | 1.000 |
| full_history | self_vs_world | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| full_history | source_attribution | 13 | 1.000 | 0.000 | 1.000 | 0.846 |
| full_history | world_vs_other | 30 | 1.000 | 0.000 | 1.000 | 1.000 |
| recent_window | conditional_other | 2 | 0.500 | 0.050 | 1.000 | 1.000 |
| recent_window | entity_binding | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| recent_window | group_generalization | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| recent_window | history_pressure | 2 | 1.000 | 0.000 | 1.000 | 0.500 |
| recent_window | salience_misdirection | 4 | 1.000 | 0.000 | 1.000 | 1.000 |
| recent_window | self_vs_world | 2 | 0.500 | 0.000 | 1.000 | 1.000 |
| recent_window | source_attribution | 13 | 1.000 | 0.000 | 1.000 | 0.923 |
| recent_window | world_vs_other | 30 | 1.000 | 0.000 | 1.000 | 0.933 |
| reflection | conditional_other | 2 | 0.000 | 0.200 | 0.500 | 1.000 |
| reflection | entity_binding | 2 | 1.000 | 0.050 | 1.000 | 1.000 |
| reflection | group_generalization | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| reflection | history_pressure | 2 | 1.000 | 0.000 | 1.000 | 0.500 |
| reflection | salience_misdirection | 4 | 1.000 | 0.000 | 1.000 | 1.000 |
| reflection | self_vs_world | 2 | 1.000 | 0.033 | 1.000 | 1.000 |
| reflection | source_attribution | 13 | 0.692 | 0.072 | 1.000 | 0.692 |
| reflection | world_vs_other | 30 | 0.900 | 0.062 | 0.967 | 0.833 |
| retrieval | conditional_other | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| retrieval | entity_binding | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| retrieval | group_generalization | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| retrieval | history_pressure | 2 | 1.000 | 0.000 | 1.000 | 0.500 |
| retrieval | salience_misdirection | 4 | 1.000 | 0.000 | 1.000 | 0.500 |
| retrieval | self_vs_world | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| retrieval | source_attribution | 13 | 0.846 | 0.004 | 1.000 | 0.846 |
| retrieval | world_vs_other | 30 | 1.000 | 0.002 | 1.000 | 1.000 |
| summary | conditional_other | 2 | 0.500 | 0.050 | 1.000 | 1.000 |
| summary | entity_binding | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| summary | group_generalization | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| summary | history_pressure | 2 | 1.000 | 0.000 | 1.000 | 0.500 |
| summary | salience_misdirection | 4 | 1.000 | 0.000 | 1.000 | 1.000 |
| summary | self_vs_world | 2 | 0.000 | 0.033 | 1.000 | 1.000 |
| summary | source_attribution | 13 | 0.846 | 0.000 | 1.000 | 0.846 |
| summary | world_vs_other | 30 | 1.000 | 0.000 | 1.000 | 0.933 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
