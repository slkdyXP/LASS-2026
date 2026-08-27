# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| direct | 8 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.823 |
| full_history | 8 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.830 |
| recent_window | 8 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.844 |
| reflection | 8 | 0.875 | 0.087 | 1.000 | 0.875 | 1.000 | 0.814 |
| retrieval | 8 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.808 |
| summary | 8 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.850 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| direct | epidemic_other_violation | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |
| direct | epidemic_world_variant | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.838 |
| direct | public_goods_david_free_rider | 2 | 1.000 | 0.000 | 0.550 | 1.000 | 0.881 |
| direct | public_goods_world_multiplier | 2 | 1.000 | 0.000 | 0.150 | 1.000 | 0.769 |
| full_history | epidemic_other_violation | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.850 |
| full_history | epidemic_world_variant | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.800 |
| full_history | public_goods_david_free_rider | 2 | 1.000 | 0.000 | 0.650 | 1.000 | 0.894 |
| full_history | public_goods_world_multiplier | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.775 |
| recent_window | epidemic_other_violation | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.912 |
| recent_window | epidemic_world_variant | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| recent_window | public_goods_david_free_rider | 2 | 1.000 | 0.000 | 0.600 | 1.000 | 0.887 |
| recent_window | public_goods_world_multiplier | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| reflection | epidemic_other_violation | 2 | 0.500 | 0.250 | 0.050 | 0.500 | 0.662 |
| reflection | epidemic_world_variant | 2 | 1.000 | 0.000 | 0.900 | 1.000 | 0.925 |
| reflection | public_goods_david_free_rider | 2 | 1.000 | 0.100 | 0.550 | 1.000 | 0.887 |
| reflection | public_goods_world_multiplier | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| retrieval | epidemic_other_violation | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.900 |
| retrieval | epidemic_world_variant | 2 | 1.000 | 0.000 | 0.000 | 1.000 | 0.750 |
| retrieval | public_goods_david_free_rider | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.800 |
| retrieval | public_goods_world_multiplier | 2 | 1.000 | 0.000 | 0.250 | 1.000 | 0.781 |
| summary | epidemic_other_violation | 2 | 1.000 | 0.000 | 0.600 | 1.000 | 0.950 |
| summary | epidemic_world_variant | 2 | 1.000 | 0.000 | 0.150 | 1.000 | 0.769 |
| summary | public_goods_david_free_rider | 2 | 1.000 | 0.000 | 0.650 | 1.000 | 0.894 |
| summary | public_goods_world_multiplier | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| direct | world_vs_other | 8 | 1.000 | 0.000 | 1.000 | 1.000 |
| full_history | world_vs_other | 8 | 1.000 | 0.000 | 1.000 | 1.000 |
| recent_window | world_vs_other | 8 | 1.000 | 0.000 | 1.000 | 1.000 |
| reflection | world_vs_other | 8 | 0.875 | 0.087 | 1.000 | 0.875 |
| retrieval | world_vs_other | 8 | 1.000 | 0.000 | 1.000 | 1.000 |
| summary | world_vs_other | 8 | 1.000 | 0.000 | 1.000 | 1.000 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
