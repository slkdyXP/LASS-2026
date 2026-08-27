# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| direct | 8 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.877 |
| full_history | 8 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.889 |
| recent_window | 8 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.875 |
| reflection | 8 | 0.875 | 0.058 | 0.875 | 1.000 | 1.000 | 0.877 |
| retrieval | 8 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.919 |
| summary | 8 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.834 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| direct | grid_bob_overuse | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| direct | grid_world_cloud_cover | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| direct | team_carol_effort_drop | 2 | 1.000 | 0.000 | 0.600 | 1.000 | 0.950 |
| direct | team_world_complexity | 2 | 1.000 | 0.000 | 0.350 | 1.000 | 0.794 |
| full_history | grid_bob_overuse | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| full_history | grid_world_cloud_cover | 2 | 1.000 | 0.000 | 0.150 | 1.000 | 0.769 |
| full_history | team_carol_effort_drop | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| full_history | team_world_complexity | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.838 |
| recent_window | grid_bob_overuse | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| recent_window | grid_world_cloud_cover | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.775 |
| recent_window | team_carol_effort_drop | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.931 |
| recent_window | team_world_complexity | 2 | 1.000 | 0.000 | 0.550 | 1.000 | 0.819 |
| reflection | grid_bob_overuse | 2 | 0.500 | 0.200 | 0.050 | 1.000 | 0.794 |
| reflection | grid_world_cloud_cover | 2 | 1.000 | 0.000 | 0.350 | 1.000 | 0.856 |
| reflection | team_carol_effort_drop | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.963 |
| reflection | team_world_complexity | 2 | 1.000 | 0.033 | 0.600 | 1.000 | 0.896 |
| retrieval | grid_bob_overuse | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| retrieval | grid_world_cloud_cover | 2 | 1.000 | 0.000 | 0.500 | 1.000 | 0.812 |
| retrieval | team_carol_effort_drop | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| retrieval | team_world_complexity | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.912 |
| summary | grid_bob_overuse | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.838 |
| summary | grid_world_cloud_cover | 2 | 1.000 | 0.000 | 0.350 | 1.000 | 0.794 |
| summary | team_carol_effort_drop | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.900 |
| summary | team_world_complexity | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| direct | world_vs_other | 8 | 1.000 | 0.000 | 1.000 | 1.000 |
| full_history | world_vs_other | 8 | 1.000 | 0.000 | 1.000 | 1.000 |
| recent_window | world_vs_other | 8 | 1.000 | 0.000 | 1.000 | 1.000 |
| reflection | world_vs_other | 8 | 0.875 | 0.058 | 0.875 | 1.000 |
| retrieval | world_vs_other | 8 | 1.000 | 0.000 | 1.000 | 1.000 |
| summary | world_vs_other | 8 | 1.000 | 0.000 | 1.000 | 1.000 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
