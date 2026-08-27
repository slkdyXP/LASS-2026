# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| direct | 45 | 0.289 | 0.078 | 0.822 | 0.667 | 1.000 | 0.723 |
| full_history | 45 | 0.422 | 0.062 | 0.733 | 0.667 | 1.000 | 0.736 |
| recent_window | 45 | 0.378 | 0.062 | 0.778 | 0.667 | 1.000 | 0.737 |
| reflection | 45 | 0.422 | 0.062 | 0.756 | 0.667 | 1.000 | 0.739 |
| retrieval | 45 | 0.422 | 0.062 | 0.733 | 0.667 | 1.000 | 0.739 |
| summary | 45 | 0.422 | 0.062 | 0.756 | 0.667 | 1.000 | 0.739 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| direct | auction_bob_conditional | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| direct | auction_self_need_shift | 2 | 0.500 | 0.183 | 0.000 | 1.000 | 0.846 |
| direct | auction_world_shortage | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.850 |
| direct | entity_binding_bob_not_david | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| direct | epidemic_other_violation | 2 | 0.500 | 0.050 | 0.400 | 1.000 | 0.738 |
| direct | epidemic_world_variant | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| direct | fish_other_shift | 2 | 0.500 | 0.183 | 0.000 | 1.000 | 0.846 |
| direct | fish_persona_stress | 1 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| direct | fish_world_anomaly_recovery | 2 | 0.500 | 0.150 | 0.050 | 0.500 | 0.731 |
| direct | fish_world_regime | 2 | 0.500 | 0.050 | 0.400 | 0.000 | 0.738 |
| direct | grid_bob_overuse | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| direct | grid_world_cloud_cover | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| direct | long_history_late_world_shift | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| direct | newcomer_no_group_generalization | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| direct | public_goods_david_free_rider | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.750 |
| direct | public_goods_world_multiplier | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.750 |
| direct | supply_sam_withholding | 2 | 0.000 | 0.317 | -0.800 | 1.000 | 0.592 |
| direct | supply_world_port_delay | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| direct | team_carol_effort_drop | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| direct | team_self_capability_drop | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| direct | team_world_complexity | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| direct | traffic_david_blockage | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| direct | traffic_world_lane_closure | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.750 |
| full_history | auction_bob_conditional | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| full_history | auction_self_need_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| full_history | auction_world_shortage | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.850 |
| full_history | entity_binding_bob_not_david | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| full_history | epidemic_other_violation | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.850 |
| full_history | epidemic_world_variant | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| full_history | fish_other_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| full_history | fish_persona_stress | 1 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| full_history | fish_world_anomaly_recovery | 2 | 0.500 | 0.050 | 0.450 | 0.500 | 0.806 |
| full_history | fish_world_regime | 2 | 1.000 | 0.050 | 0.800 | 0.000 | 0.850 |
| full_history | grid_bob_overuse | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.725 |
| full_history | grid_world_cloud_cover | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| full_history | long_history_late_world_shift | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| full_history | newcomer_no_group_generalization | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| full_history | public_goods_david_free_rider | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.750 |
| full_history | public_goods_world_multiplier | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| full_history | supply_sam_withholding | 2 | 0.000 | 0.317 | -0.800 | 1.000 | 0.592 |
| full_history | supply_world_port_delay | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| full_history | team_carol_effort_drop | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| full_history | team_self_capability_drop | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| full_history | team_world_complexity | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| full_history | traffic_david_blockage | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| full_history | traffic_world_lane_closure | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.750 |
| recent_window | auction_bob_conditional | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| recent_window | auction_self_need_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| recent_window | auction_world_shortage | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.850 |
| recent_window | entity_binding_bob_not_david | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| recent_window | epidemic_other_violation | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.850 |
| recent_window | epidemic_world_variant | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| recent_window | fish_other_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| recent_window | fish_persona_stress | 1 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| recent_window | fish_world_anomaly_recovery | 2 | 0.500 | 0.050 | 0.450 | 0.500 | 0.806 |
| recent_window | fish_world_regime | 2 | 0.500 | 0.050 | 0.400 | 0.000 | 0.738 |
| recent_window | grid_bob_overuse | 2 | 0.500 | 0.050 | 0.400 | 1.000 | 0.675 |
| recent_window | grid_world_cloud_cover | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.562 |
| recent_window | long_history_late_world_shift | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| recent_window | newcomer_no_group_generalization | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| recent_window | public_goods_david_free_rider | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.750 |
| recent_window | public_goods_world_multiplier | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| recent_window | supply_sam_withholding | 2 | 0.000 | 0.317 | -0.800 | 1.000 | 0.592 |
| recent_window | supply_world_port_delay | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| recent_window | team_carol_effort_drop | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| recent_window | team_self_capability_drop | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| recent_window | team_world_complexity | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| recent_window | traffic_david_blockage | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| recent_window | traffic_world_lane_closure | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.750 |
| reflection | auction_bob_conditional | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| reflection | auction_self_need_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| reflection | auction_world_shortage | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.850 |
| reflection | entity_binding_bob_not_david | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| reflection | epidemic_other_violation | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.850 |
| reflection | epidemic_world_variant | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| reflection | fish_other_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| reflection | fish_persona_stress | 1 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| reflection | fish_world_anomaly_recovery | 2 | 0.500 | 0.050 | 0.450 | 0.500 | 0.806 |
| reflection | fish_world_regime | 2 | 1.000 | 0.050 | 0.800 | 0.000 | 0.850 |
| reflection | grid_bob_overuse | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.725 |
| reflection | grid_world_cloud_cover | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| reflection | long_history_late_world_shift | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.562 |
| reflection | newcomer_no_group_generalization | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| reflection | public_goods_david_free_rider | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.750 |
| reflection | public_goods_world_multiplier | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| reflection | supply_sam_withholding | 2 | 0.000 | 0.317 | -0.800 | 1.000 | 0.592 |
| reflection | supply_world_port_delay | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| reflection | team_carol_effort_drop | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| reflection | team_self_capability_drop | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| reflection | team_world_complexity | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| reflection | traffic_david_blockage | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| reflection | traffic_world_lane_closure | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.750 |
| retrieval | auction_bob_conditional | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| retrieval | auction_self_need_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| retrieval | auction_world_shortage | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.850 |
| retrieval | entity_binding_bob_not_david | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| retrieval | epidemic_other_violation | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.850 |
| retrieval | epidemic_world_variant | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| retrieval | fish_other_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| retrieval | fish_persona_stress | 1 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| retrieval | fish_world_anomaly_recovery | 2 | 0.500 | 0.050 | 0.450 | 0.500 | 0.806 |
| retrieval | fish_world_regime | 2 | 1.000 | 0.050 | 0.800 | 0.000 | 0.850 |
| retrieval | grid_bob_overuse | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.725 |
| retrieval | grid_world_cloud_cover | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.562 |
| retrieval | long_history_late_world_shift | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| retrieval | newcomer_no_group_generalization | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| retrieval | public_goods_david_free_rider | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.750 |
| retrieval | public_goods_world_multiplier | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| retrieval | supply_sam_withholding | 2 | 0.000 | 0.317 | -0.800 | 1.000 | 0.592 |
| retrieval | supply_world_port_delay | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| retrieval | team_carol_effort_drop | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| retrieval | team_self_capability_drop | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| retrieval | team_world_complexity | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| retrieval | traffic_david_blockage | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| retrieval | traffic_world_lane_closure | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.750 |
| summary | auction_bob_conditional | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| summary | auction_self_need_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| summary | auction_world_shortage | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.850 |
| summary | entity_binding_bob_not_david | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| summary | epidemic_other_violation | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.850 |
| summary | epidemic_world_variant | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| summary | fish_other_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| summary | fish_persona_stress | 1 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| summary | fish_world_anomaly_recovery | 2 | 0.500 | 0.050 | 0.450 | 0.500 | 0.806 |
| summary | fish_world_regime | 2 | 1.000 | 0.050 | 0.800 | 0.000 | 0.850 |
| summary | grid_bob_overuse | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.725 |
| summary | grid_world_cloud_cover | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| summary | long_history_late_world_shift | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.562 |
| summary | newcomer_no_group_generalization | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| summary | public_goods_david_free_rider | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.750 |
| summary | public_goods_world_multiplier | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| summary | supply_sam_withholding | 2 | 0.000 | 0.317 | -0.800 | 1.000 | 0.592 |
| summary | supply_world_port_delay | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| summary | team_carol_effort_drop | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.500 |
| summary | team_self_capability_drop | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.625 |
| summary | team_world_complexity | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| summary | traffic_david_blockage | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| summary | traffic_world_lane_closure | 2 | 0.000 | 0.050 | 0.000 | 1.000 | 0.750 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| direct | entity_binding | 2 | 0.000 | 0.050 | 0.000 | 1.000 |
| direct | group_generalization | 2 | 1.000 | 0.050 | 1.000 | 1.000 |
| direct | history_pressure | 2 | 0.000 | 0.050 | 1.000 | 0.000 |
| direct | self_vs_world | 2 | 0.000 | 0.050 | 1.000 | 1.000 |
| direct | source_attribution | 13 | 0.615 | 0.106 | 1.000 | 0.769 |
| direct | world_vs_other | 24 | 0.125 | 0.072 | 0.750 | 0.583 |
| full_history | entity_binding | 2 | 0.000 | 0.050 | 0.000 | 1.000 |
| full_history | group_generalization | 2 | 1.000 | 0.050 | 1.000 | 1.000 |
| full_history | history_pressure | 2 | 0.000 | 0.050 | 0.000 | 0.000 |
| full_history | self_vs_world | 2 | 0.000 | 0.050 | 1.000 | 1.000 |
| full_history | source_attribution | 13 | 0.846 | 0.050 | 1.000 | 0.769 |
| full_history | world_vs_other | 24 | 0.250 | 0.072 | 0.667 | 0.583 |
| recent_window | entity_binding | 2 | 0.000 | 0.050 | 0.000 | 1.000 |
| recent_window | group_generalization | 2 | 1.000 | 0.050 | 1.000 | 1.000 |
| recent_window | history_pressure | 2 | 0.000 | 0.050 | 1.000 | 0.000 |
| recent_window | self_vs_world | 2 | 0.000 | 0.050 | 1.000 | 1.000 |
| recent_window | source_attribution | 13 | 0.769 | 0.050 | 1.000 | 0.769 |
| recent_window | world_vs_other | 24 | 0.208 | 0.072 | 0.667 | 0.583 |
| reflection | entity_binding | 2 | 0.000 | 0.050 | 0.000 | 1.000 |
| reflection | group_generalization | 2 | 1.000 | 0.050 | 1.000 | 1.000 |
| reflection | history_pressure | 2 | 0.000 | 0.050 | 0.500 | 0.000 |
| reflection | self_vs_world | 2 | 0.000 | 0.050 | 1.000 | 1.000 |
| reflection | source_attribution | 13 | 0.846 | 0.050 | 1.000 | 0.769 |
| reflection | world_vs_other | 24 | 0.250 | 0.072 | 0.667 | 0.583 |
| retrieval | entity_binding | 2 | 0.000 | 0.050 | 0.000 | 1.000 |
| retrieval | group_generalization | 2 | 1.000 | 0.050 | 1.000 | 1.000 |
| retrieval | history_pressure | 2 | 0.000 | 0.050 | 0.000 | 0.000 |
| retrieval | self_vs_world | 2 | 0.000 | 0.050 | 1.000 | 1.000 |
| retrieval | source_attribution | 13 | 0.846 | 0.050 | 1.000 | 0.769 |
| retrieval | world_vs_other | 24 | 0.250 | 0.072 | 0.667 | 0.583 |
| summary | entity_binding | 2 | 0.000 | 0.050 | 0.000 | 1.000 |
| summary | group_generalization | 2 | 1.000 | 0.050 | 1.000 | 1.000 |
| summary | history_pressure | 2 | 0.000 | 0.050 | 0.500 | 0.000 |
| summary | self_vs_world | 2 | 0.000 | 0.050 | 1.000 | 1.000 |
| summary | source_attribution | 13 | 0.846 | 0.050 | 1.000 | 0.769 |
| summary | world_vs_other | 24 | 0.250 | 0.072 | 0.667 | 0.583 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
