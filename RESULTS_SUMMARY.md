# ScopeProbe live experiment summary

## Status

Completed on DeepSeek with the frozen confirmation plan.

- Discovery: 29 scenarios, 6 baselines, 174 trials, 342 checkpoint records.
- Confirmation: 14 preregistered scenarios, 4 baselines, 3 repeats, 168 trials, 336 checkpoint records.
- One confirmation attempt produced an out-of-range reflection action (`12` with bound `[0,10]`); the attempt is retained in the error log and the missing combination was rerun successfully.
- Smoke and mock outputs are excluded from the reported discovery and confirmation aggregates.

## Main result

The broad claim “shared textual memory generally causes cross-scope interference” is not supported. The narrower claim “unconstrained textual consolidation, especially reflection, causes cross-scope interference in particular temporal and self/other attribution settings” is supported by the current controlled vignettes.

### Confirmation aggregate

| Baseline | Checkpoints | Scope accuracy | Protected leakage | Action accuracy | Explicit persona stability |
|---|---:|---:|---:|---:|---:|
| Direct | 84 | 91.7% | 0.004 | 89.3% | 100% |
| Full history | 84 | 94.0% | 0.001 | 90.5% | 100% |
| Summary | 84 | 86.9% | 0.015 | 83.3% | 100% |
| Reflection | 84 | 77.4% | 0.059 | 76.2% | 100% |

High leakage (`protected_leakage >= 0.2`) occurred in 10/84 reflection checkpoints, 3/84 summary checkpoints, and 0/84 direct/full-history checkpoints.

### Paired descriptive tests

Conditions were paired by scenario, repeat, and checkpoint.

- Scope, full-history vs reflection: 14 pairs were correct only under full-history and 0 only under reflection; exact McNemar p=0.000122.
- Scope, full-history vs summary: 6 vs 0; p=0.03125.
- Action, full-history vs reflection: 12 vs 0; p=0.000488.
- Action, full-history vs summary: 7 vs 1; p=0.070312.

These p-values are descriptive rather than paper-ready inferential statistics because checkpoints are clustered within scenarios and action thresholds are provisional.

## Where the phenomenon appeared

Reflection errors repeatedly appeared in:

- conditional-other behavior being rewritten as a world/market regime;
- own health/need changes being rewritten as market/world changes;
- specific-agent violations producing unsupported system-level mechanisms;
- one-off environmental shocks remaining in the world model after recovery;
- aggressive reflective prose inventing hidden leakage, collusion, automation, enforcement failure, or adversarial mechanisms not present in observations.

The repeated high-signal confirmation cases were `auction_bob_conditional`, `auction_self_need_shift`, `epidemic_other_violation`, `fish_world_anomaly_recovery`, `grid_bob_overuse`, and `team_self_capability_drop`.

Negative controls also matter: public-goods world/other pairs, entity binding, the original persistent fishery world/other pair, and the salient-storm distractor were usually scoped correctly. Full-history was especially robust in these tests.

## Sensitivity to an ontology ambiguity

`team_self_capability_drop` describes failure of the participant's own machine. The registered label treats this as `self` because it changes the participant's current capability, but a model can reasonably call hardware an external `world` object. Excluding this six-checkpoint scenario:

| Baseline | Scope accuracy | Mean leakage |
|---|---:|---:|
| Full history | 100.0% | 0.000 |
| Summary | 93.6% | 0.006 |
| Reflection | 83.3% | 0.049 |

The central consolidation result therefore survives, but the scope ontology needs a precise operational definition in the paper.

## What was not found

- No explicit persona drift under the structured probe metric.
- No general failure of full-history memory.
- No strong entity-binding or one-person-to-whole-group generalization effect in the confirmation sample.
- The model-based evaluator produced many false negatives and should not be used as the primary judge.

## Valid claim at this stage

The evidence supports a paper centered on **reflection/consolidation-induced scope interference**, not a claim that all textual memory is intrinsically defective. A defensible framing is:

> Unconstrained reflection can convert local or temporary evidence into persistent cross-scope beliefs, whereas retaining the same evidence as full history is substantially more reliable in controlled social-agent interventions.

## Remaining validity limits

- These are synthetic controlled vignettes inspired by GovSim/ALYMPICS, not yet closed-loop benchmark runs.
- Belief probes are self-reports, though raw persistent memory and actions are retained for audit.
- Some action correctness intervals encode provisional policy judgments.
- DeepSeek is the only tested model in this run.
- Scenario-level clustered confidence intervals and human annotation of raw memory errors are still needed for a publication claim.

