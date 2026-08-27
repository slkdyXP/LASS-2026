# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| direct | 42 | 0.905 | 0.003 | 1.000 | 0.857 | 1.000 | 0.842 |
| full_history | 42 | 0.881 | 0.002 | 1.000 | 0.881 | 1.000 | 0.864 |
| reflection | 40 | 0.775 | 0.072 | 1.000 | 0.800 | 1.000 | 0.844 |
| summary | 42 | 0.857 | 0.021 | 1.000 | 0.833 | 1.000 | 0.853 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| direct | auction_bob_conditional | 6 | 1.000 | 0.000 | 0.383 | 1.000 | 0.902 |
| direct | entity_binding_bob_not_david | 6 | 1.000 | 0.000 | 0.467 | 1.000 | 0.871 |
| direct | fish_other_shift | 6 | 1.000 | 0.000 | 0.517 | 1.000 | 0.877 |
| direct | fish_world_regime | 6 | 1.000 | 0.000 | 0.317 | 0.500 | 0.748 |
| direct | long_history_late_world_shift | 6 | 1.000 | 0.000 | 0.317 | 0.833 | 0.769 |
| direct | salience_other_storm_named | 6 | 1.000 | 0.000 | 0.800 | 0.833 | 0.954 |
| direct | team_self_capability_drop | 6 | 0.333 | 0.022 | -0.033 | 0.833 | 0.772 |
| full_history | auction_bob_conditional | 6 | 1.000 | 0.000 | 0.333 | 1.000 | 0.917 |
| full_history | entity_binding_bob_not_david | 6 | 1.000 | 0.000 | 0.650 | 1.000 | 0.956 |
| full_history | fish_other_shift | 6 | 1.000 | 0.000 | 0.583 | 1.000 | 0.885 |
| full_history | fish_world_regime | 6 | 1.000 | 0.000 | 0.617 | 0.500 | 0.765 |
| full_history | long_history_late_world_shift | 6 | 1.000 | 0.000 | 0.633 | 0.667 | 0.787 |
| full_history | salience_other_storm_named | 6 | 1.000 | 0.000 | 0.733 | 1.000 | 0.967 |
| full_history | team_self_capability_drop | 6 | 0.167 | 0.011 | -0.033 | 1.000 | 0.769 |
| reflection | auction_bob_conditional | 6 | 0.500 | 0.161 | -0.217 | 0.833 | 0.732 |
| reflection | entity_binding_bob_not_david | 6 | 1.000 | 0.011 | 0.367 | 1.000 | 0.861 |
| reflection | fish_other_shift | 6 | 1.000 | 0.072 | 0.583 | 0.833 | 0.941 |
| reflection | fish_world_regime | 6 | 1.000 | 0.011 | 0.750 | 0.500 | 0.867 |
| reflection | long_history_late_world_shift | 4 | 1.000 | 0.067 | 0.650 | 0.750 | 0.870 |
| reflection | salience_other_storm_named | 6 | 1.000 | 0.000 | 0.817 | 0.667 | 0.935 |
| reflection | team_self_capability_drop | 6 | 0.000 | 0.183 | -0.517 | 1.000 | 0.710 |
| summary | auction_bob_conditional | 6 | 1.000 | 0.011 | 0.300 | 1.000 | 0.915 |
| summary | entity_binding_bob_not_david | 6 | 1.000 | 0.000 | 0.417 | 1.000 | 0.906 |
| summary | fish_other_shift | 6 | 1.000 | 0.000 | 0.667 | 1.000 | 0.896 |
| summary | fish_world_regime | 6 | 1.000 | 0.000 | 0.750 | 0.500 | 0.885 |
| summary | long_history_late_world_shift | 6 | 1.000 | 0.000 | 0.200 | 0.667 | 0.733 |
| summary | salience_other_storm_named | 6 | 1.000 | 0.000 | 0.733 | 0.667 | 0.904 |
| summary | team_self_capability_drop | 6 | 0.000 | 0.133 | -0.400 | 1.000 | 0.733 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| direct | entity_binding | 6 | 1.000 | 0.000 | 1.000 | 1.000 |
| direct | history_pressure | 6 | 1.000 | 0.000 | 1.000 | 0.833 |
| direct | salience_misdirection | 6 | 1.000 | 0.000 | 1.000 | 0.833 |
| direct | self_vs_world | 6 | 0.333 | 0.022 | 1.000 | 0.833 |
| direct | source_attribution | 18 | 1.000 | 0.000 | 1.000 | 0.833 |
| full_history | entity_binding | 6 | 1.000 | 0.000 | 1.000 | 1.000 |
| full_history | history_pressure | 6 | 1.000 | 0.000 | 1.000 | 0.667 |
| full_history | salience_misdirection | 6 | 1.000 | 0.000 | 1.000 | 1.000 |
| full_history | self_vs_world | 6 | 0.167 | 0.011 | 1.000 | 1.000 |
| full_history | source_attribution | 18 | 1.000 | 0.000 | 1.000 | 0.833 |
| reflection | entity_binding | 6 | 1.000 | 0.011 | 1.000 | 1.000 |
| reflection | history_pressure | 4 | 1.000 | 0.067 | 1.000 | 0.750 |
| reflection | salience_misdirection | 6 | 1.000 | 0.000 | 1.000 | 0.667 |
| reflection | self_vs_world | 6 | 0.000 | 0.183 | 1.000 | 1.000 |
| reflection | source_attribution | 18 | 0.833 | 0.082 | 1.000 | 0.722 |
| summary | entity_binding | 6 | 1.000 | 0.000 | 1.000 | 1.000 |
| summary | history_pressure | 6 | 1.000 | 0.000 | 1.000 | 0.667 |
| summary | salience_misdirection | 6 | 1.000 | 0.000 | 1.000 | 0.667 |
| summary | self_vs_world | 6 | 0.000 | 0.133 | 1.000 | 1.000 |
| summary | source_attribution | 18 | 1.000 | 0.004 | 1.000 | 0.833 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 1
