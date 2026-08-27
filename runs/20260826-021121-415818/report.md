# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| direct | 8 | 1.000 | 0.000 | 0.875 | 0.875 | 1.000 | 0.822 |
| full_history | 8 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.884 |
| recent_window | 8 | 0.750 | 0.013 | 0.875 | 1.000 | 1.000 | 0.838 |
| reflection | 8 | 0.875 | 0.075 | 1.000 | 0.750 | 1.000 | 0.878 |
| retrieval | 8 | 0.875 | 0.008 | 0.875 | 1.000 | 1.000 | 0.855 |
| summary | 8 | 0.750 | 0.013 | 0.875 | 0.875 | 1.000 | 0.889 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| direct | auction_other_inferential | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.787 |
| direct | auction_world_inferential | 2 | 1.000 | 0.000 | 0.800 | 0.500 | 0.912 |
| direct | fish_other_inferential | 2 | 1.000 | 0.000 | 0.350 | 1.000 | 0.794 |
| direct | fish_world_inferential | 2 | 1.000 | 0.000 | 0.350 | 1.000 | 0.794 |
| full_history | auction_other_inferential | 2 | 1.000 | 0.000 | 0.650 | 1.000 | 0.956 |
| full_history | auction_world_inferential | 2 | 1.000 | 0.000 | 0.600 | 1.000 | 0.825 |
| full_history | fish_other_inferential | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.963 |
| full_history | fish_world_inferential | 2 | 1.000 | 0.000 | 0.350 | 1.000 | 0.794 |
| recent_window | auction_other_inferential | 2 | 0.000 | 0.050 | 0.250 | 1.000 | 0.731 |
| recent_window | auction_world_inferential | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.838 |
| recent_window | fish_other_inferential | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.963 |
| recent_window | fish_world_inferential | 2 | 1.000 | 0.000 | 0.550 | 1.000 | 0.819 |
| reflection | auction_other_inferential | 2 | 0.500 | 0.200 | 0.200 | 1.000 | 0.800 |
| reflection | auction_world_inferential | 2 | 1.000 | 0.033 | 0.600 | 0.000 | 0.771 |
| reflection | fish_other_inferential | 2 | 1.000 | 0.033 | 0.700 | 1.000 | 0.971 |
| reflection | fish_world_inferential | 2 | 1.000 | 0.033 | 0.700 | 1.000 | 0.971 |
| retrieval | auction_other_inferential | 2 | 0.500 | 0.000 | 0.550 | 1.000 | 0.819 |
| retrieval | auction_world_inferential | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.838 |
| retrieval | fish_other_inferential | 2 | 1.000 | 0.033 | 0.500 | 1.000 | 0.946 |
| retrieval | fish_world_inferential | 2 | 1.000 | 0.000 | 0.550 | 1.000 | 0.819 |
| summary | auction_other_inferential | 2 | 0.000 | 0.050 | 0.250 | 1.000 | 0.731 |
| summary | auction_world_inferential | 2 | 1.000 | 0.000 | 0.650 | 1.000 | 0.956 |
| summary | fish_other_inferential | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.963 |
| summary | fish_world_inferential | 2 | 1.000 | 0.000 | 0.750 | 0.500 | 0.906 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| direct | conditional_other | 2 | 1.000 | 0.000 | 0.500 | 1.000 |
| direct | world_vs_other | 6 | 1.000 | 0.000 | 1.000 | 0.833 |
| full_history | conditional_other | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| full_history | world_vs_other | 6 | 1.000 | 0.000 | 1.000 | 1.000 |
| recent_window | conditional_other | 2 | 0.000 | 0.050 | 0.500 | 1.000 |
| recent_window | world_vs_other | 6 | 1.000 | 0.000 | 1.000 | 1.000 |
| reflection | conditional_other | 2 | 0.500 | 0.200 | 1.000 | 1.000 |
| reflection | world_vs_other | 6 | 1.000 | 0.033 | 1.000 | 0.667 |
| retrieval | conditional_other | 2 | 0.500 | 0.000 | 0.500 | 1.000 |
| retrieval | world_vs_other | 6 | 1.000 | 0.011 | 1.000 | 1.000 |
| summary | conditional_other | 2 | 0.000 | 0.050 | 0.500 | 1.000 |
| summary | world_vs_other | 6 | 1.000 | 0.000 | 1.000 | 0.833 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
