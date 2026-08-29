# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| evidence_gated_memory_only | 92 | 0.837 | 0.004 | 0.837 | 0.848 | 1.000 | 0.780 |
| four_component_memory | 84 | 0.869 | 0.000 | 0.869 | 0.774 | 1.000 | 0.749 |
| full_history | 92 | 1.000 | 0.000 | 1.000 | 0.870 | 1.000 | 0.820 |
| hscm_external_controller | 108 | 0.935 | 0.000 | 0.935 | 0.602 | 1.000 | 0.777 |
| reflection | 88 | 0.648 | 0.026 | 0.739 | 0.693 | 1.000 | 0.721 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| evidence_gated_memory_only | long_alympics_100r_12a_other | 8 | 0.375 | 0.000 | 0.275 | 1.000 | 0.628 |
| evidence_gated_memory_only | long_alympics_100r_5a_other | 4 | 0.250 | 0.000 | 0.250 | 1.000 | 0.594 |
| evidence_gated_memory_only | long_alympics_100r_5a_world | 4 | 1.000 | 0.000 | 0.625 | 0.250 | 0.766 |
| evidence_gated_memory_only | long_alympics_50r_12a_other | 4 | 0.250 | 0.000 | 0.250 | 1.000 | 0.594 |
| evidence_gated_memory_only | long_alympics_50r_12a_world | 8 | 1.000 | 0.000 | 0.463 | 0.250 | 0.745 |
| evidence_gated_memory_only | long_alympics_50r_5a_other | 8 | 0.500 | 0.000 | 0.300 | 0.750 | 0.631 |
| evidence_gated_memory_only | long_alympics_50r_5a_world | 4 | 1.000 | 0.000 | 0.475 | 0.250 | 0.716 |
| evidence_gated_memory_only | long_govsim_100r_12a_other | 12 | 1.000 | 0.017 | 0.525 | 1.000 | 0.841 |
| evidence_gated_memory_only | long_govsim_100r_12a_world | 12 | 1.000 | 0.000 | 0.583 | 1.000 | 0.896 |
| evidence_gated_memory_only | long_govsim_100r_5a_world | 8 | 1.000 | 0.000 | 0.475 | 1.000 | 0.841 |
| evidence_gated_memory_only | long_govsim_50r_12a_other | 12 | 1.000 | 0.017 | 0.608 | 1.000 | 0.882 |
| evidence_gated_memory_only | long_govsim_50r_5a_other | 4 | 1.000 | 0.000 | 0.575 | 1.000 | 0.853 |
| evidence_gated_memory_only | long_govsim_50r_5a_world | 4 | 1.000 | 0.000 | 0.400 | 1.000 | 0.863 |
| four_component_memory | long_alympics_100r_12a_other | 4 | 0.250 | 0.000 | 0.250 | 1.000 | 0.594 |
| four_component_memory | long_alympics_100r_12a_world | 4 | 1.000 | 0.000 | 0.600 | 0.250 | 0.731 |
| four_component_memory | long_alympics_100r_5a_world | 4 | 1.000 | 0.000 | 0.475 | 1.000 | 0.809 |
| four_component_memory | long_alympics_50r_12a_world | 12 | 1.000 | 0.000 | 0.417 | 0.250 | 0.708 |
| four_component_memory | long_alympics_50r_5a_other | 12 | 0.333 | 0.000 | 0.258 | 0.667 | 0.574 |
| four_component_memory | long_alympics_50r_5a_world | 4 | 1.000 | 0.000 | 0.475 | 0.250 | 0.716 |
| four_component_memory | long_govsim_100r_12a_other | 8 | 1.000 | 0.000 | 0.575 | 1.000 | 0.838 |
| four_component_memory | long_govsim_100r_12a_world | 4 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |
| four_component_memory | long_govsim_100r_5a_other | 8 | 1.000 | 0.000 | 0.550 | 1.000 | 0.819 |
| four_component_memory | long_govsim_100r_5a_world | 4 | 1.000 | 0.000 | 0.475 | 1.000 | 0.809 |
| four_component_memory | long_govsim_50r_12a_other | 4 | 1.000 | 0.000 | 0.525 | 1.000 | 0.816 |
| four_component_memory | long_govsim_50r_12a_world | 12 | 1.000 | 0.000 | 0.592 | 1.000 | 0.824 |
| four_component_memory | long_govsim_50r_5a_world | 4 | 1.000 | 0.000 | 0.500 | 1.000 | 0.812 |
| full_history | long_alympics_100r_12a_other | 8 | 1.000 | 0.000 | 0.412 | 1.000 | 0.802 |
| full_history | long_alympics_100r_12a_world | 8 | 1.000 | 0.000 | 0.613 | 0.250 | 0.733 |
| full_history | long_alympics_100r_5a_world | 8 | 1.000 | 0.000 | 0.675 | 1.000 | 0.834 |
| full_history | long_alympics_50r_12a_other | 8 | 1.000 | 0.000 | 0.438 | 1.000 | 0.805 |
| full_history | long_alympics_50r_12a_world | 8 | 1.000 | 0.000 | 0.600 | 0.250 | 0.731 |
| full_history | long_alympics_50r_5a_other | 8 | 1.000 | 0.000 | 0.425 | 1.000 | 0.803 |
| full_history | long_govsim_100r_12a_other | 4 | 1.000 | 0.000 | 0.500 | 1.000 | 0.812 |
| full_history | long_govsim_100r_12a_world | 8 | 1.000 | 0.000 | 0.700 | 1.000 | 0.853 |
| full_history | long_govsim_100r_5a_other | 4 | 1.000 | 0.000 | 0.750 | 1.000 | 0.906 |
| full_history | long_govsim_100r_5a_world | 4 | 1.000 | 0.000 | 0.700 | 1.000 | 0.869 |
| full_history | long_govsim_50r_12a_other | 8 | 1.000 | 0.000 | 0.725 | 1.000 | 0.856 |
| full_history | long_govsim_50r_12a_world | 4 | 1.000 | 0.000 | 0.700 | 1.000 | 0.869 |
| full_history | long_govsim_50r_5a_other | 8 | 1.000 | 0.000 | 0.700 | 1.000 | 0.869 |
| full_history | long_govsim_50r_5a_world | 4 | 1.000 | 0.000 | 0.650 | 1.000 | 0.831 |
| hscm_external_controller | long_alympics_100r_12a_other | 4 | 0.500 | 0.000 | 0.300 | 1.000 | 0.662 |
| hscm_external_controller | long_alympics_100r_12a_world | 4 | 1.000 | 0.000 | 0.525 | 0.250 | 0.784 |
| hscm_external_controller | long_alympics_100r_5a_other | 8 | 0.875 | 0.000 | 0.362 | 1.000 | 0.764 |
| hscm_external_controller | long_alympics_100r_5a_world | 8 | 1.000 | 0.000 | 0.438 | 0.250 | 0.742 |
| hscm_external_controller | long_alympics_50r_12a_other | 4 | 0.500 | 0.000 | 0.300 | 1.000 | 0.662 |
| hscm_external_controller | long_alympics_50r_12a_world | 12 | 1.000 | 0.000 | 0.525 | 0.250 | 0.774 |
| hscm_external_controller | long_alympics_50r_5a_other | 8 | 0.750 | 0.000 | 0.325 | 1.000 | 0.728 |
| hscm_external_controller | long_alympics_50r_5a_world | 8 | 1.000 | 0.000 | 0.475 | 0.250 | 0.794 |
| hscm_external_controller | long_govsim_100r_12a_other | 4 | 1.000 | 0.000 | 0.425 | 1.000 | 0.834 |
| hscm_external_controller | long_govsim_100r_12a_world | 8 | 1.000 | 0.000 | 0.550 | 0.250 | 0.787 |
| hscm_external_controller | long_govsim_100r_5a_other | 4 | 1.000 | 0.000 | 0.550 | 1.000 | 0.850 |
| hscm_external_controller | long_govsim_100r_5a_world | 8 | 1.000 | 0.000 | 0.438 | 0.250 | 0.758 |
| hscm_external_controller | long_govsim_50r_12a_other | 8 | 1.000 | 0.000 | 0.500 | 1.000 | 0.844 |
| hscm_external_controller | long_govsim_50r_12a_world | 8 | 1.000 | 0.000 | 0.425 | 0.250 | 0.741 |
| hscm_external_controller | long_govsim_50r_5a_other | 8 | 1.000 | 0.000 | 0.438 | 1.000 | 0.836 |
| hscm_external_controller | long_govsim_50r_5a_world | 4 | 1.000 | 0.000 | 0.575 | 0.750 | 0.884 |
| reflection | long_alympics_100r_12a_other | 8 | 0.375 | 0.008 | 0.250 | 0.500 | 0.565 |
| reflection | long_alympics_100r_12a_world | 8 | 0.500 | 0.000 | 0.287 | 0.250 | 0.630 |
| reflection | long_alympics_100r_5a_other | 4 | 0.250 | 0.042 | 0.125 | 1.000 | 0.589 |
| reflection | long_alympics_50r_12a_other | 8 | 0.250 | 0.075 | 0.025 | 1.000 | 0.616 |
| reflection | long_alympics_50r_12a_world | 12 | 0.917 | 0.006 | 0.542 | 0.333 | 0.757 |
| reflection | long_alympics_50r_5a_other | 8 | 0.125 | 0.077 | -0.075 | 0.625 | 0.543 |
| reflection | long_alympics_50r_5a_world | 4 | 0.500 | 0.013 | 0.250 | 0.250 | 0.630 |
| reflection | long_govsim_100r_12a_other | 4 | 0.750 | 0.017 | 0.550 | 1.000 | 0.823 |
| reflection | long_govsim_100r_12a_world | 4 | 1.000 | 0.000 | 0.700 | 0.250 | 0.806 |
| reflection | long_govsim_100r_5a_world | 4 | 1.000 | 0.000 | 0.600 | 1.000 | 0.887 |
| reflection | long_govsim_50r_12a_other | 8 | 1.000 | 0.013 | 0.738 | 1.000 | 0.908 |
| reflection | long_govsim_50r_12a_world | 4 | 0.750 | 0.067 | 0.200 | 1.000 | 0.760 |
| reflection | long_govsim_50r_5a_other | 4 | 0.750 | 0.058 | 0.350 | 1.000 | 0.777 |
| reflection | long_govsim_50r_5a_world | 8 | 1.000 | 0.013 | 0.688 | 1.000 | 0.900 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| evidence_gated_memory_only | length_population_source | 92 | 0.837 | 0.004 | 0.837 | 0.848 |
| four_component_memory | length_population_source | 84 | 0.869 | 0.000 | 0.869 | 0.774 |
| full_history | length_population_source | 92 | 1.000 | 0.000 | 1.000 | 0.870 |
| hscm_external_controller | length_population_source | 108 | 0.935 | 0.000 | 0.935 | 0.602 |
| reflection | length_population_source | 88 | 0.648 | 0.026 | 0.739 | 0.693 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 124
