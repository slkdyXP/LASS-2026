# Evidence-Gated Reflection: preliminary confirmation results

## Method

`evidence_gated_reflection` separates six memory components:

1. stable persona;
2. current self state;
3. consolidated models;
4. open hypotheses;
5. recent observed episodes;
6. action policy.

A single unusual event can create an episode or explicitly uncertain hypothesis, but not a persistent causal rule. Consolidation requires at least two independent consistent observations or an explicitly documented cause/persistent state. Recovery evidence weakens or removes hypotheses. Current verified hazards can still trigger the smallest reasonable reversible response; evidence gating applies to long-term claims rather than blocking first response.

`guarded_reflection` is the prompt-only ablation. It retains free-form text but asks the model not to invent hidden causes, not to generalize one event, and to respond proportionally.

## Runs

- Original confirmation: `runs/combined-20260826-101634-645291`
- Guarded-reflection confirmation: `runs/method-confirmation-combined-20260826`
- Final evidence-gated confirmation: `runs/method-final-v2-20260826`

All comparisons below use DeepSeek Chat, temperature 0.2, three repeats, 14 scenarios, and 84 checkpoints per baseline. The final method run completed without failed trials.

## Main descriptive results

| Baseline | Scope accuracy | Protected leakage | Action accuracy |
|---|---:|---:|---:|
| Reflection | 77.4% | 0.0589 | 76.2% |
| Guarded reflection | 83.3% | 0.0139 | 85.7% |
| Evidence-gated reflection | 89.3% | 0.0060 | 92.9% |

The full aggregate includes the ambiguous `team_self_capability_drop` ontology and self-state probe false negatives. Excluding only the ambiguous team/hardware scenario:

| Baseline | Scope accuracy | Protected leakage | Action accuracy |
|---|---:|---:|---:|
| Reflection | 83.3% | 0.0494 | 74.4% |
| Guarded reflection | 89.7% | 0.0085 | 84.6% |
| Evidence-gated reflection | 92.3% | 0.0021 | 92.3% |

## Overgeneralization-target scenarios

This subset contains Bob's conditional emergency bid, Bob's grid overuse, David's epidemic violation, and the one-off fish contamination/recovery.

| Baseline | Scope accuracy | Protected leakage | Action accuracy |
|---|---:|---:|---:|
| Reflection | 54.2% | 0.1021 | 79.2% |
| Guarded reflection | 87.5% | 0.0250 | 87.5% |
| Evidence-gated reflection | 95.8% | 0.0069 | 95.8% |

Paired descriptive comparison between Reflection and evidence-gated Reflection:

- scope: 11 checkpoints improved and 1 regressed; exact McNemar p=0.00635;
- action: 4 improved and 0 regressed; exact McNemar p=0.125.

The scope result supports reduced overgeneralization. The action result is directionally positive but underpowered.

## Persistent-world sensitivity

On true persistent world changes (fish regeneration decline, public-project multiplier failure, lane closure, and late inverter failure):

| Baseline | Scope accuracy | Protected leakage | Action accuracy |
|---|---:|---:|---:|
| Reflection | 100.0% | 0.0306 | 62.5% |
| Guarded reflection | 95.8% | 0.0000 | 62.5% |
| Evidence-gated reflection | 100.0% | 0.0000 | 79.2% |

Thus the final evidence gate did not remove recognition of real persistent world changes in this set.

## Validity limits

- Scenarios were selected after discovery; p-values are descriptive, not confirmatory.
- Checkpoints within a scenario are clustered.
- Action ranges are provisional; several fish and traffic thresholds are debatable.
- The self-state probe sometimes reports `none` despite the structured memory explicitly recording the changed need and taking the correct action.
- `team_self_capability_drop` is ontologically ambiguous because a fault in one's own machine can reasonably be labeled either self capability, episodic event, or world state.
- These synthetic diagnostics do not yet establish improvements in GovSim or ALYMPICS closed-loop group outcomes.
