# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| evidence_gated_reflection | 24 | 1.000 | 0.004 | 1.000 | 0.875 | 1.000 | 0.877 |
| guarded_reflection | 24 | 0.875 | 0.025 | 0.917 | 0.875 | 1.000 | 0.831 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| evidence_gated_reflection | auction_bob_conditional | 6 | 1.000 | 0.017 | 0.233 | 1.000 | 0.906 |
| evidence_gated_reflection | epidemic_other_violation | 6 | 1.000 | 0.000 | 0.400 | 1.000 | 0.842 |
| evidence_gated_reflection | fish_world_anomaly_recovery | 6 | 1.000 | 0.000 | 0.667 | 0.500 | 0.896 |
| evidence_gated_reflection | grid_bob_overuse | 6 | 1.000 | 0.000 | 0.417 | 1.000 | 0.865 |
| guarded_reflection | auction_bob_conditional | 6 | 0.833 | 0.050 | 0.133 | 1.000 | 0.879 |
| guarded_reflection | epidemic_other_violation | 6 | 1.000 | 0.000 | 0.233 | 1.000 | 0.779 |
| guarded_reflection | fish_world_anomaly_recovery | 6 | 1.000 | 0.000 | 0.817 | 0.500 | 0.915 |
| guarded_reflection | grid_bob_overuse | 6 | 0.667 | 0.050 | 0.233 | 1.000 | 0.750 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| evidence_gated_reflection | source_attribution | 12 | 1.000 | 0.008 | 1.000 | 0.750 |
| evidence_gated_reflection | world_vs_other | 12 | 1.000 | 0.000 | 1.000 | 1.000 |
| guarded_reflection | source_attribution | 12 | 0.917 | 0.025 | 1.000 | 0.750 |
| guarded_reflection | world_vs_other | 12 | 0.833 | 0.025 | 0.833 | 1.000 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
