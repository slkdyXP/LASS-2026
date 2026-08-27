# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| direct | 12 | 0.917 | 0.000 | 1.000 | 1.000 | 1.000 | 0.837 |
| full_history | 12 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.851 |
| recent_window | 12 | 0.917 | 0.000 | 1.000 | 0.917 | 1.000 | 0.843 |
| reflection | 12 | 1.000 | 0.014 | 1.000 | 0.917 | 1.000 | 0.891 |
| retrieval | 12 | 1.000 | 0.000 | 1.000 | 0.750 | 1.000 | 0.847 |
| summary | 12 | 0.833 | 0.006 | 1.000 | 0.917 | 1.000 | 0.815 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| direct | entity_binding_bob_not_david | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.863 |
| direct | long_history_late_world_shift | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |
| direct | newcomer_no_group_generalization | 2 | 1.000 | 0.000 | 0.550 | 1.000 | 0.881 |
| direct | salience_other_storm_named | 2 | 1.000 | 0.000 | 0.550 | 1.000 | 0.881 |
| direct | salience_world_david_named | 2 | 1.000 | 0.000 | 0.100 | 1.000 | 0.762 |
| direct | team_self_capability_drop | 2 | 0.500 | 0.000 | 0.100 | 1.000 | 0.825 |
| full_history | entity_binding_bob_not_david | 2 | 1.000 | 0.000 | 0.550 | 1.000 | 0.881 |
| full_history | long_history_late_world_shift | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.775 |
| full_history | newcomer_no_group_generalization | 2 | 1.000 | 0.000 | 0.450 | 1.000 | 0.806 |
| full_history | salience_other_storm_named | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| full_history | salience_world_david_named | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.775 |
| full_history | team_self_capability_drop | 2 | 1.000 | 0.000 | 0.150 | 1.000 | 0.894 |
| recent_window | entity_binding_bob_not_david | 2 | 1.000 | 0.000 | 0.600 | 1.000 | 0.950 |
| recent_window | long_history_late_world_shift | 2 | 1.000 | 0.000 | 0.450 | 0.500 | 0.744 |
| recent_window | newcomer_no_group_generalization | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.800 |
| recent_window | salience_other_storm_named | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| recent_window | salience_world_david_named | 2 | 1.000 | 0.000 | 0.100 | 1.000 | 0.762 |
| recent_window | team_self_capability_drop | 2 | 0.500 | 0.000 | 0.100 | 1.000 | 0.825 |
| reflection | entity_binding_bob_not_david | 2 | 1.000 | 0.050 | 0.500 | 1.000 | 0.887 |
| reflection | long_history_late_world_shift | 2 | 1.000 | 0.000 | 0.600 | 0.500 | 0.825 |
| reflection | newcomer_no_group_generalization | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| reflection | salience_other_storm_named | 2 | 1.000 | 0.000 | 0.800 | 1.000 | 0.975 |
| reflection | salience_world_david_named | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.850 |
| reflection | team_self_capability_drop | 2 | 1.000 | 0.033 | 0.600 | 1.000 | 0.833 |
| retrieval | entity_binding_bob_not_david | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.963 |
| retrieval | long_history_late_world_shift | 2 | 1.000 | 0.000 | 0.550 | 0.500 | 0.756 |
| retrieval | newcomer_no_group_generalization | 2 | 1.000 | 0.000 | 0.200 | 1.000 | 0.775 |
| retrieval | salience_other_storm_named | 2 | 1.000 | 0.000 | 0.900 | 0.000 | 0.863 |
| retrieval | salience_world_david_named | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.800 |
| retrieval | team_self_capability_drop | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.925 |
| summary | entity_binding_bob_not_david | 2 | 1.000 | 0.000 | 0.400 | 1.000 | 0.863 |
| summary | long_history_late_world_shift | 2 | 1.000 | 0.000 | 0.150 | 0.500 | 0.706 |
| summary | newcomer_no_group_generalization | 2 | 1.000 | 0.000 | 0.100 | 1.000 | 0.825 |
| summary | salience_other_storm_named | 2 | 1.000 | 0.000 | 0.700 | 1.000 | 0.963 |
| summary | salience_world_david_named | 2 | 1.000 | 0.000 | 0.300 | 1.000 | 0.787 |
| summary | team_self_capability_drop | 2 | 0.000 | 0.033 | -0.100 | 1.000 | 0.746 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| direct | entity_binding | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| direct | group_generalization | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| direct | history_pressure | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| direct | salience_misdirection | 4 | 1.000 | 0.000 | 1.000 | 1.000 |
| direct | self_vs_world | 2 | 0.500 | 0.000 | 1.000 | 1.000 |
| full_history | entity_binding | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| full_history | group_generalization | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| full_history | history_pressure | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| full_history | salience_misdirection | 4 | 1.000 | 0.000 | 1.000 | 1.000 |
| full_history | self_vs_world | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| recent_window | entity_binding | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| recent_window | group_generalization | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| recent_window | history_pressure | 2 | 1.000 | 0.000 | 1.000 | 0.500 |
| recent_window | salience_misdirection | 4 | 1.000 | 0.000 | 1.000 | 1.000 |
| recent_window | self_vs_world | 2 | 0.500 | 0.000 | 1.000 | 1.000 |
| reflection | entity_binding | 2 | 1.000 | 0.050 | 1.000 | 1.000 |
| reflection | group_generalization | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| reflection | history_pressure | 2 | 1.000 | 0.000 | 1.000 | 0.500 |
| reflection | salience_misdirection | 4 | 1.000 | 0.000 | 1.000 | 1.000 |
| reflection | self_vs_world | 2 | 1.000 | 0.033 | 1.000 | 1.000 |
| retrieval | entity_binding | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| retrieval | group_generalization | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| retrieval | history_pressure | 2 | 1.000 | 0.000 | 1.000 | 0.500 |
| retrieval | salience_misdirection | 4 | 1.000 | 0.000 | 1.000 | 0.500 |
| retrieval | self_vs_world | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| summary | entity_binding | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| summary | group_generalization | 2 | 1.000 | 0.000 | 1.000 | 1.000 |
| summary | history_pressure | 2 | 1.000 | 0.000 | 1.000 | 0.500 |
| summary | salience_misdirection | 4 | 1.000 | 0.000 | 1.000 | 1.000 |
| summary | self_vs_world | 2 | 0.000 | 0.033 | 1.000 | 1.000 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
