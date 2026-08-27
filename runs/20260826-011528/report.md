# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|
| direct | 13 | 0.615 | 0.106 | 1.000 | 1.000 | 0.806 |
| full_history | 13 | 0.846 | 0.050 | 1.000 | 1.000 | 0.897 |
| reflection | 13 | 0.846 | 0.050 | 1.000 | 1.000 | 0.897 |
| summary | 13 | 0.846 | 0.050 | 1.000 | 1.000 | 0.897 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| direct | auction_bob_conditional | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.825 |
| direct | auction_self_need_shift | 2 | 0.500 | 0.183 | 0.000 | 1.000 | 0.794 |
| direct | auction_world_shortage | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.800 |
| direct | fish_other_shift | 2 | 0.500 | 0.183 | 0.000 | 1.000 | 0.794 |
| direct | fish_persona_stress | 1 | 1.000 | 0.050 | 0.800 | 1.000 | 0.967 |
| direct | fish_world_anomaly_recovery | 2 | 0.500 | 0.150 | 0.050 | 1.000 | 0.725 |
| direct | fish_world_regime | 2 | 0.500 | 0.050 | 0.400 | 1.000 | 0.817 |
| full_history | auction_bob_conditional | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.825 |
| full_history | auction_self_need_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.967 |
| full_history | auction_world_shortage | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.800 |
| full_history | fish_other_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.967 |
| full_history | fish_persona_stress | 1 | 1.000 | 0.050 | 0.800 | 1.000 | 0.967 |
| full_history | fish_world_anomaly_recovery | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.825 |
| full_history | fish_world_regime | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.967 |
| reflection | auction_bob_conditional | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.825 |
| reflection | auction_self_need_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.967 |
| reflection | auction_world_shortage | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.800 |
| reflection | fish_other_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.967 |
| reflection | fish_persona_stress | 1 | 1.000 | 0.050 | 0.800 | 1.000 | 0.967 |
| reflection | fish_world_anomaly_recovery | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.825 |
| reflection | fish_world_regime | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.967 |
| summary | auction_bob_conditional | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.825 |
| summary | auction_self_need_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.967 |
| summary | auction_world_shortage | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.800 |
| summary | fish_other_shift | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.967 |
| summary | fish_persona_stress | 1 | 1.000 | 0.050 | 0.800 | 1.000 | 0.967 |
| summary | fish_world_anomaly_recovery | 2 | 0.500 | 0.050 | 0.450 | 1.000 | 0.825 |
| summary | fish_world_regime | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.967 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
