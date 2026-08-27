# Four-component baseline and leave-one-out ablation

## Definition

The four-component baseline removes both `CONSOLIDATED MODELS` and `OPEN HYPOTHESES` from the original six-section evidence-gated memory. Its remaining sections are:

1. `STABLE PERSONA`;
2. `CURRENT SELF STATE`;
3. `RECENT OBSERVED EPISODES`;
4. `ACTION POLICY`.

Four leave-one-out variants then remove one of these remaining sections. The experiment uses the same frozen eight-scenario held-out suite, DeepSeek Chat, temperature 0.2, seed 20260826, three repeats, action bounds, and scoring as the six-section ablation. The four-component baseline is newly sampled in the same randomized batch as its four ablations; neither earlier five-section result is reused as the control.

The live run is `runs/four-component-ablation-heldout-20260827`. All 120 trials completed, producing 48 checkpoint records for each condition and 240 records in total, with no failed trials. All 240 memory snapshots retained every required heading and never recreated an excluded heading.

## Results

| Condition | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability |
|---|---:|---:|---:|---:|---:|
| Four-component baseline | **97.9%** | 0.0014 | 95.8% | **97.9%** | 100% |
| Without stable persona | 91.7% | 0.0049 | 93.8% | 91.7% | 100% |
| Without current self state | 97.9% | 0.0007 | 97.9% | 95.8% | 100% |
| Without recent observed episodes | 97.9% | 0.0014 | 97.9% | 91.7% | 100% |
| Without action policy | 100.0% | 0.0014 | 100.0% | **81.3%** | 100% |

Paired descriptive comparisons use identical `(scenario, repeat, checkpoint)` cells:

| Removed section | Scope: control better / ablation better | Scope p | Action: control better / ablation better | Action p |
|---|---:|---:|---:|---:|
| Stable persona | 4 / 1 | 0.375 | 3 / 0 | 0.250 |
| Current self state | 1 / 1 | 1.000 | 2 / 1 | 1.000 |
| Recent observed episodes | 1 / 1 | 1.000 | 4 / 1 | 0.375 |
| Action policy | 0 / 1 | 1.000 | **9 / 1** | **0.0215** |

The p-values are two-sided exact McNemar tests and remain descriptive because observations are clustered within only eight scenarios.

## Interpretation

The four-component baseline retains the measured performance of the larger method on this small explicit held-out suite. This supports using it as a simpler candidate architecture, but does not prove that consolidated models and open hypotheses are unnecessary in longer or more ambiguous environments.

`ACTION POLICY` again has the clearest independent contribution. Removing it leaves causal scope intact but lowers action accuracy by 16.7 percentage points. All action errors occur in persistent world-change scenarios: persistent-change action accuracy falls from 95.8% to 62.5%, while recovery/conditional-event action accuracy remains 100%.

The logs again show both under-response and over-response without action policy: some agents retain the old withdrawal or batch after a verified capacity loss, while others jump to maximum irrigation. Thus the section primarily converts a correct current belief into a proportionate response rather than improving attribution.

The other three sections do not have firm independent necessity evidence here:

- removing stable persona storage lowers scope and action by 6.2 points, but persona remains supplied in the decision header and the paired differences are not significant;
- removing recent episodes lowers action by 6.2 points, again without reliable paired evidence;
- removing current self state changes little because the held-out suite contains no targeted self-state intervention.

The defensible current claim is that a compact four-part architecture is sufficient on this suite, with action policy demonstrably important. Targeted persona, self-state, long-history, and ambiguous-evidence scenarios are still required before claiming that all four remaining sections are independently necessary.
