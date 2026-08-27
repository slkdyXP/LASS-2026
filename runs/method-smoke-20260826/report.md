# ScopeProbe diagnostic report

> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.

## Overall baseline results

| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| evidence_gated_reflection | 8 | 0.875 | 0.050 | 0.625 | 0.875 | 1.000 | 0.823 |
| guarded_reflection | 8 | 0.875 | 0.050 | 0.625 | 0.875 | 1.000 | 0.823 |

## Per-scenario results

| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |
|---|---|---:|---:|---:|---:|---:|---:|
| evidence_gated_reflection | auction_bob_conditional | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.912 |
| evidence_gated_reflection | epidemic_other_violation | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.850 |
| evidence_gated_reflection | fish_world_anomaly_recovery | 2 | 0.500 | 0.050 | 0.450 | 0.500 | 0.806 |
| evidence_gated_reflection | grid_bob_overuse | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.725 |
| guarded_reflection | auction_bob_conditional | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.912 |
| guarded_reflection | epidemic_other_violation | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.850 |
| guarded_reflection | fish_world_anomaly_recovery | 2 | 0.500 | 0.050 | 0.450 | 0.500 | 0.806 |
| guarded_reflection | grid_bob_overuse | 2 | 1.000 | 0.050 | 0.800 | 1.000 | 0.725 |

## Results by experimental axis

| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |
|---|---|---:|---:|---:|---:|---:|
| evidence_gated_reflection | source_attribution | 4 | 0.750 | 0.050 | 0.750 | 0.750 |
| evidence_gated_reflection | world_vs_other | 4 | 1.000 | 0.050 | 0.500 | 1.000 |
| guarded_reflection | source_attribution | 4 | 0.750 | 0.050 | 0.750 | 0.750 |
| guarded_reflection | world_vs_other | 4 | 1.000 | 0.050 | 0.500 | 1.000 |

## Interpretation gate

Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.

Failed trials: 0
