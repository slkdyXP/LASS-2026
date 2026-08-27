# Six-component leave-one-out ablation

## Design

The frozen held-out suite was rerun with six leave-one-section-out variants of `evidence_gated_memory_only`:

1. without `STABLE PERSONA`;
2. without `CURRENT SELF STATE`;
3. without `CONSOLIDATED MODELS`;
4. without `OPEN HYPOTHESES`;
5. without `RECENT OBSERVED EPISODES`;
6. without `ACTION POLICY`.

All other available sections and their applicable update rules were retained. Persona, observations, action interface, DeepSeek Chat, temperature 0.2, seed, three repeats, and scoring were unchanged. The eight held-out scenarios produced 48 checkpoint records per condition. The frozen full six-section results from `runs/heldout-final-20260826` serve as the control.

The live ablation run is `runs/ablation-heldout-20260827`; the combined report is `runs/ablation-combined-20260827`. All 144 trials completed, producing 288 ablation checkpoint records with no failed trials. Across all snapshots, every variant retained its required five headings and never recreated the excluded heading.

## Results

| Condition | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability |
|---|---:|---:|---:|---:|---:|
| Full six-section control | 95.8% | 0.0028 | 95.8% | 95.8% | 100% |
| Without stable persona | 95.8% | 0.0042 | 97.9% | 100.0% | 100% |
| Without current self state | 93.8% | 0.0000 | 95.8% | 95.8% | 100% |
| Without consolidated models | 100.0% | 0.0035 | 100.0% | 97.9% | 100% |
| Without open hypotheses | 100.0% | 0.0000 | 89.6% | 97.9% | 100% |
| Without recent observed episodes | 95.8% | 0.0014 | 100.0% | 87.5% | 100% |
| Without action policy | 95.8% | 0.0000 | 100.0% | **72.9%** | 100% |

Paired descriptive comparisons against the frozen control use matching `(scenario, repeat, checkpoint)` cells. Removing `ACTION POLICY` caused 11 action regressions and 0 improvements (two-sided exact McNemar p=0.00098). Removing `RECENT OBSERVED EPISODES` caused 4 action regressions and 0 improvements (p=0.125). No other removal produced a reliable decrease on scope or action in this sample.

## Log-grounded interpretation

`ACTION POLICY` is the only component with strong necessity evidence for behavior in this held-out suite. Its removal left scope attribution unchanged but sharply reduced action accuracy, entirely on persistent world-change cases: persistent-change action accuracy fell from 91.7% to 45.8%, while recovery/conditional-event action accuracy remained 100%.

The raw reasons show two repeated failure modes without the policy:

- failure to respond immediately to a verified capacity loss, such as retaining withdrawal 5 after a documented supply cut or retaining batch 10 after sorter capacity halved;
- disproportionate response, such as jumping to maximum irrigation 20 when the registered proportional range was 12–16.

This matches the intended role of the section: translate verified beliefs into a proportional, reversible decision with rollback conditions. It does not appear necessary for correct causal scope attribution itself.

`RECENT OBSERVED EPISODES` has weaker, directional behavioral evidence. Without it, some agents waited for repeated evidence before responding to a directly documented current hazard, while others overreacted to a named participant's one-off emergency. The sample is too small for a firm necessity claim.

The experiment does **not** demonstrate that all six sections are independently necessary. In particular:

- the held-out suite contains no direct self-state intervention, so it has little power to test `CURRENT SELF STATE`;
- persona is supplied separately in every decision header and no scenario directly pressures identity change, so stable persona storage is not isolated strongly;
- explicit short scenarios allow hypotheses, episodes, and consolidated facts to substitute for one another, limiting power to separate those three storage components;
- the exact p-values are descriptive because checkpoints are clustered within only eight scenarios and the control was collected in an earlier run.

The supported claim is therefore narrow: the six-way decomposition is a useful implementation, but this ablation presently identifies `ACTION POLICY` as essential for converting correct cognition into proportionate behavior; it does not yet justify claiming that every memory section contributes independently.
