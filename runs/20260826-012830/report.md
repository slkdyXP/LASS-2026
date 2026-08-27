# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| direct | 23 | 0.522 | 0.105 | 0.913 | 0.826 | 1.000 | 0.813 |
| full_history | 23 | 0.652 | 0.073 | 0.913 | 0.826 | 1.000 | 0.852 |
| recent_window | 23 | 0.609 | 0.073 | 0.913 | 0.826 | 1.000 | 0.842 |
| reflection | 23 | 0.652 | 0.073 | 0.913 | 0.826 | 1.000 | 0.852 |
| retrieval | 23 | 0.652 | 0.073 | 0.913 | 0.826 | 1.000 | 0.852 |
| summary | 23 | 0.652 | 0.073 | 0.913 | 0.826 | 1.000 | 0.852 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| direct | auction_bob_conditional | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| direct | auction_self_need_shift | 2 | 0.500 | 0.183 | 0.000 | 1.000 | 0.846 |
| direct | auction_world_shortage | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.850 |
| direct | fish_other_shift | 2 | 0.500 | 0.183 | 0.000 | 1.000 | 0.846 |
| direct | fish_persona_stress | 1 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| direct | fish_world_anomaly_recovery | 2 | 0.500 | 0.150 | 0.050 | 1.000 | 0.794 |
| direct | fish_world_regime | 2 | 0.500 | 0.050 | 0.400 | 1.000 | 0.863 |
| direct | newcomer_no_group_generalization | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| direct | supply_sam_withholding | 2 | 0.000 | 0.317 | -0.800 | 1.000 | 0.592 |
| direct | supply_world_port_delay | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| direct | traffic_david_blockage | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| direct | traffic_world_lane_closure | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| full_history | auction_bob_conditional | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| full_history | auction_self_need_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| full_history | auction_world_shortage | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.850 |
| full_history | fish_other_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| full_history | fish_persona_stress | 1 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| full_history | fish_world_anomaly_recovery | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| full_history | fish_world_regime | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| full_history | newcomer_no_group_generalization | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| full_history | supply_sam_withholding | 2 | 0.000 | 0.317 | -0.800 | 1.000 | 0.592 |
| full_history | supply_world_port_delay | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| full_history | traffic_david_blockage | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| full_history | traffic_world_lane_closure | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| recent_window | auction_bob_conditional | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| recent_window | auction_self_need_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| recent_window | auction_world_shortage | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.850 |
| recent_window | fish_other_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| recent_window | fish_persona_stress | 1 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| recent_window | fish_world_anomaly_recovery | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| recent_window | fish_world_regime | 2 | 0.500 | 0.050 | 0.400 | 1.000 | 0.863 |
| recent_window | newcomer_no_group_generalization | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| recent_window | supply_sam_withholding | 2 | 0.000 | 0.317 | -0.800 | 1.000 | 0.592 |
| recent_window | supply_world_port_delay | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| recent_window | traffic_david_blockage | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| recent_window | traffic_world_lane_closure | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| reflection | auction_bob_conditional | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| reflection | auction_self_need_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| reflection | auction_world_shortage | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.850 |
| reflection | fish_other_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| reflection | fish_persona_stress | 1 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| reflection | fish_world_anomaly_recovery | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| reflection | fish_world_regime | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| reflection | newcomer_no_group_generalization | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| reflection | supply_sam_withholding | 2 | 0.000 | 0.317 | -0.800 | 1.000 | 0.592 |
| reflection | supply_world_port_delay | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| reflection | traffic_david_blockage | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| reflection | traffic_world_lane_closure | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| retrieval | auction_bob_conditional | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| retrieval | auction_self_need_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| retrieval | auction_world_shortage | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.850 |
| retrieval | fish_other_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| retrieval | fish_persona_stress | 1 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| retrieval | fish_world_anomaly_recovery | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| retrieval | fish_world_regime | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| retrieval | newcomer_no_group_generalization | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| retrieval | supply_sam_withholding | 2 | 0.000 | 0.317 | -0.800 | 1.000 | 0.592 |
| retrieval | supply_world_port_delay | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| retrieval | traffic_david_blockage | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| retrieval | traffic_world_lane_closure | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| summary | auction_bob_conditional | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| summary | auction_self_need_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| summary | auction_world_shortage | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.850 |
| summary | fish_other_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| summary | fish_persona_stress | 1 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| summary | fish_world_anomaly_recovery | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.869 |
| summary | fish_world_regime | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| summary | newcomer_no_group_generalization | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| summary | supply_sam_withholding | 2 | 0.000 | 0.317 | -0.800 | 1.000 | 0.592 |
| summary | supply_world_port_delay | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.975 |
| summary | traffic_david_blockage | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |
| summary | traffic_world_lane_closure | 2 | 0.000 | 0.050 | 0.000 | 0.000 | 0.625 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| direct | group_generalization | 2 | 1.000 | 0.050 | 1.000 | 1.000 |
| direct | source_attribution | 13 | 0.615 | 0.106 | 1.000 | 1.000 |
| direct | world_vs_other | 8 | 0.250 | 0.117 | 0.750 | 0.500 |
| full_history | group_generalization | 2 | 1.000 | 0.050 | 1.000 | 1.000 |
| full_history | source_attribution | 13 | 0.846 | 0.050 | 1.000 | 1.000 |
| full_history | world_vs_other | 8 | 0.250 | 0.117 | 0.750 | 0.500 |
| recent_window | group_generalization | 2 | 1.000 | 0.050 | 1.000 | 1.000 |
| recent_window | source_attribution | 13 | 0.769 | 0.050 | 1.000 | 1.000 |
| recent_window | world_vs_other | 8 | 0.250 | 0.117 | 0.750 | 0.500 |
| reflection | group_generalization | 2 | 1.000 | 0.050 | 1.000 | 1.000 |
| reflection | source_attribution | 13 | 0.846 | 0.050 | 1.000 | 1.000 |
| reflection | world_vs_other | 8 | 0.250 | 0.117 | 0.750 | 0.500 |
| retrieval | group_generalization | 2 | 1.000 | 0.050 | 1.000 | 1.000 |
| retrieval | source_attribution | 13 | 0.846 | 0.050 | 1.000 | 1.000 |
| retrieval | world_vs_other | 8 | 0.250 | 0.117 | 0.750 | 0.500 |
| summary | group_generalization | 2 | 1.000 | 0.050 | 1.000 | 1.000 |
| summary | source_attribution | 13 | 0.846 | 0.050 | 1.000 | 1.000 |
| summary | world_vs_other | 8 | 0.250 | 0.117 | 0.750 | 0.500 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 66
