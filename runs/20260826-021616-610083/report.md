# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| direct | 13 | 1.000 | 0.000 | 1.000 | 0.769 | 1.000 | 0.865 |
| full_history | 13 | 1.000 | 0.000 | 1.000 | 0.846 | 1.000 | 0.864 |
| recent_window | 13 | 1.000 | 0.000 | 1.000 | 0.923 | 1.000 | 0.902 |
| reflection | 13 | 0.692 | 0.072 | 1.000 | 0.692 | 1.000 | 0.824 |
| retrieval | 13 | 0.846 | 0.004 | 1.000 | 0.846 | 1.000 | 0.840 |
| summary | 13 | 0.846 | 0.000 | 1.000 | 0.846 | 1.000 | 0.856 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| direct | auction_bob_conditional | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.925 |
| direct | auction_self_need_shift | 2 | 1.000 | 0.000 | 0.500 | 1.000 | 0.938 |
| direct | auction_world_shortage | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| direct | fish_other_shift | 2 | 1.000 | 0.000 | 0.600 | 1.000 | 0.950 |
| direct | fish_persona_stress | 1 | 1.000 | 0.000 | 0.800 | 0.000 | 0.725 |
| direct | fish_world_anomaly_recovery | 2 | 1.000 | 0.000 | 0.900 | 0.500 | 0.925 |
| direct | fish_world_regime | 2 | 1.000 | 0.000 | 0.400 | 0.500 | 0.738 |
| full_history | auction_bob_conditional | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.912 |
| full_history | auction_self_need_shift | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.912 |
| full_history | auction_world_shortage | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| full_history | fish_other_shift | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.869 |
| full_history | fish_persona_stress | 1 | 1.000 | 0.000 | 0.600 | 1.000 | 0.950 |
| full_history | fish_world_anomaly_recovery | 2 | 1.000 | 0.000 | 0.750 | 0.500 | 0.906 |
| full_history | fish_world_regime | 2 | 1.000 | 0.000 | 0.550 | 0.500 | 0.756 |
| recent_window | auction_bob_conditional | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.931 |
| recent_window | auction_self_need_shift | 2 | 1.000 | 0.000 | 0.350 | 1.000 | 0.919 |
| recent_window | auction_world_shortage | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |
| recent_window | fish_other_shift | 2 | 1.000 | 0.000 | 0.600 | 1.000 | 0.950 |
| recent_window | fish_persona_stress | 1 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| recent_window | fish_world_anomaly_recovery | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| recent_window | fish_world_regime | 2 | 1.000 | 0.000 | 0.350 | 0.500 | 0.794 |
| reflection | auction_bob_conditional | 2 | 0.500 | 0.133 | -0.100 | 1.000 | 0.771 |
| reflection | auction_self_need_shift | 2 | 0.000 | 0.250 | -0.750 | 0.000 | 0.469 |
| reflection | auction_world_shortage | 2 | 1.000 | 0.025 | 0.750 | 1.000 | 0.909 |
| reflection | fish_other_shift | 2 | 1.000 | 0.033 | 0.600 | 1.000 | 0.958 |
| reflection | fish_persona_stress | 1 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| reflection | fish_world_anomaly_recovery | 2 | 0.500 | 0.025 | 0.700 | 0.500 | 0.847 |
| reflection | fish_world_regime | 2 | 1.000 | 0.000 | 0.800 | 0.500 | 0.912 |
| retrieval | auction_bob_conditional | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.906 |
| retrieval | auction_self_need_shift | 2 | 0.500 | 0.000 | 0.100 | 1.000 | 0.825 |
| retrieval | auction_world_shortage | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| retrieval | fish_other_shift | 2 | 1.000 | 0.000 | 0.600 | 1.000 | 0.887 |
| retrieval | fish_persona_stress | 1 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| retrieval | fish_world_anomaly_recovery | 2 | 0.500 | 0.025 | 0.550 | 0.500 | 0.828 |
| retrieval | fish_world_regime | 2 | 1.000 | 0.000 | 0.400 | 0.500 | 0.738 |
| summary | auction_bob_conditional | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.925 |
| summary | auction_self_need_shift | 2 | 0.000 | 0.000 | 0.000 | 1.000 | 0.750 |
| summary | auction_world_shortage | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| summary | fish_other_shift | 2 | 1.000 | 0.000 | 0.650 | 1.000 | 0.894 |
| summary | fish_persona_stress | 1 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| summary | fish_world_anomaly_recovery | 2 | 1.000 | 0.000 | 0.800 | 0.500 | 0.912 |
| summary | fish_world_regime | 2 | 1.000 | 0.000 | 0.500 | 0.500 | 0.812 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| direct | source_attribution | 13 | 1.000 | 0.000 | 1.000 | 0.769 |
| full_history | source_attribution | 13 | 1.000 | 0.000 | 1.000 | 0.846 |
| recent_window | source_attribution | 13 | 1.000 | 0.000 | 1.000 | 0.923 |
| reflection | source_attribution | 13 | 0.692 | 0.072 | 1.000 | 0.692 |
| retrieval | source_attribution | 13 | 0.846 | 0.004 | 1.000 | 0.846 |
| summary | source_attribution | 13 | 0.846 | 0.000 | 1.000 | 0.846 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
