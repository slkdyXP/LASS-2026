# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| direct | 8 | 1.000 | 0.000 | 1.000 | 0.875 | 1.000 | 0.828 |
| full_history | 8 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.833 |
| recent_window | 8 | 1.000 | 0.000 | 1.000 | 0.750 | 1.000 | 0.787 |
| reflection | 8 | 0.875 | 0.062 | 1.000 | 0.750 | 1.000 | 0.838 |
| retrieval | 8 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.823 |
| summary | 8 | 1.000 | 0.000 | 1.000 | 0.875 | 1.000 | 0.819 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| direct | supply_sam_withholding | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.963 |
| direct | supply_world_port_delay | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.719 |
| direct | traffic_david_blockage | 2 | 1.000 | 0.000 | 0.550 | 0.500 | 0.819 |
| direct | traffic_world_lane_closure | 2 | 1.000 | 0.000 | 0.500 | 1.000 | 0.812 |
| full_history | supply_sam_withholding | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| full_history | supply_world_port_delay | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.725 |
| full_history | traffic_david_blockage | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.850 |
| full_history | traffic_world_lane_closure | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| recent_window | supply_sam_withholding | 2 | 1.000 | 0.000 | 0.700 | 0.500 | 0.838 |
| recent_window | supply_world_port_delay | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| recent_window | traffic_david_blockage | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |
| recent_window | traffic_world_lane_closure | 2 | 1.000 | 0.000 | 0.300 | 0.500 | 0.725 |
| reflection | supply_sam_withholding | 2 | 1.000 | 0.033 | 0.700 | 0.500 | 0.908 |
| reflection | supply_world_port_delay | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.850 |
| reflection | traffic_david_blockage | 2 | 1.000 | 0.033 | 0.450 | 1.000 | 0.877 |
| reflection | traffic_world_lane_closure | 2 | 0.500 | 0.183 | -0.050 | 0.500 | 0.715 |
| retrieval | supply_sam_withholding | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| retrieval | supply_world_port_delay | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.719 |
| retrieval | traffic_david_blockage | 2 | 1.000 | 0.000 | 0.600 | 1.000 | 0.825 |
| retrieval | traffic_world_lane_closure | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.775 |
| summary | supply_sam_withholding | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.900 |
| summary | supply_world_port_delay | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| summary | traffic_david_blockage | 2 | 1.000 | 0.000 | 0.550 | 1.000 | 0.881 |
| summary | traffic_world_lane_closure | 2 | 1.000 | 0.000 | 0.200 | 0.500 | 0.713 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| direct | world_vs_other | 8 | 1.000 | 0.000 | 1.000 | 0.875 |
| full_history | world_vs_other | 8 | 1.000 | 0.000 | 1.000 | 1.000 |
| recent_window | world_vs_other | 8 | 1.000 | 0.000 | 1.000 | 0.750 |
| reflection | world_vs_other | 8 | 0.875 | 0.062 | 1.000 | 0.750 |
| retrieval | world_vs_other | 8 | 1.000 | 0.000 | 1.000 | 1.000 |
| summary | world_vs_other | 8 | 1.000 | 0.000 | 1.000 | 0.875 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
