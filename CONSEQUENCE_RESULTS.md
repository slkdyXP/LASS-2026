# DeepSeek closed-loop consequence results

## Status

The frozen formal matrix completed with **135/135 valid trajectories and no failed cells**:

- 3 domains × 3 conditions × 3 memory methods × 5 repeats;
- 12 decision rounds and 3 non-writing belief probes per trajectory;
- 3,105 real `deepseek-v4-flash` calls;
- 3,006,967 prompt tokens, 675,657 completion tokens, and 1,325,312 cache-hit tokens;
- all pilot runs and the earlier over-explicit stimulus are excluded from these estimates.

## Main conclusion

The deeper consequence claim is **partly supported, with the strongest evidence in the auction**.

Unconstrained Reflection produced more late cognitive overgeneralization and more persistent action deviation than both Full History and the scope-aware controller. The clearest mechanism was an explicit self/other identity error: the focal bidder was named Erin, but Reflection frequently reinterpreted its own historical `Erin=<bid>` settlement entry as a separate competitor and then escalated bids to “beat Erin.” This error directly increased bid expenditure.

The other domains show smaller consequences. In the fishery, Reflection sometimes stayed overcautious after a named fisher returned to normal, losing private harvest but not damaging the stock. In public goods, transient under-contribution caused a small reciprocal welfare loss but did not produce lasting cooperation collapse. No method produced action-bound extremes, and no persona drift was observed.

## Cognition and behavior

| Metric | Full History | Reflection | Scope-aware memory |
|---|---:|---:|---:|
| Mean late overgeneralization | 0.000 | **0.119** | 0.009 |
| Mean oracle-normalized post-recovery action error | 0.00093 | **0.02227** | 0.00139 |
| Mean last-three-round action deviation | 0.111 | **1.422** | 0.104 |
| Explicit group generalization at final probe | 0/45 | **3/45** | 0/45 |
| Explicit persona drift | 0/45 | 0/45 | 0/45 |
| Action-bound extreme rounds | 0 | 0 | 0 |

Paired across matching `(domain, condition, repeat)` cells:

- Reflection − Full History late-overgeneralization difference: 0.119, bootstrap 95% CI [0.049, 0.195], descriptive Wilcoxon p=0.00275.
- Reflection − scope-aware late-overgeneralization difference: 0.109, CI [0.041, 0.187], p=0.0271.
- Reflection − Full History normalized action-error difference: 0.0213, CI [0.0136, 0.0302], p=4.21×10⁻⁶.
- Reflection − scope-aware normalized action-error difference: 0.0209, CI [0.0131, 0.0294], p=8.08×10⁻⁶.

These p values are descriptive because trajectories are clustered within only three domains.

Across 90 matched shock-minus-control cells, cognitive change was positively associated with persistent action change (Spearman ρ=0.341, p=0.000992). This is an association, not a mediation proof.

## Explicit self/other confusion in the auction

The strict text rule counts only post-event action reasons/messages that describe Erin—the focal agent's own assigned identity—as a third-person bidder to beat, tie, or anticipate.

| Method | Explicit confusion | Mean unnecessary post-recovery bid expenditure | Missed allocations |
|---|---:|---:|---:|
| Full History | 0/15 | 2.67, 95% CI [0.00, 8.00] | 0.00 |
| Reflection | **8/15** | **36.60, CI [25.07, 52.80]** | 0.27 |
| Scope-aware memory | 0/15 | 3.20, CI [0.00, 8.53] | 0.00 |

Reflection versus Full History identity-confusion rate: two-sided Fisher exact p=0.00220. The raw logs contain statements such as “I need to bid strictly above Erin,” even though the speaker itself is Erin. This is direct textual evidence rather than an evaluator inference.

## Domain consequences

### Fishery

Under the named-other transient condition, Reflection lost a mean 4.8 harvest units after recovery (2/5 trajectories; bootstrap CI [0.0, 10.4]); Full History and the scope-aware method lost 0. The stock nevertheless returned to and stayed at 100, so the supported consequence is **overcautious private-yield loss**, not environmental collapse.

One Reflection trajectory generalized David's one-time overharvest to the full group, stayed at 8 for five rounds, and wrote that the others were “self-interested maximum extractors.”

### Water auction

This is the strongest consequence domain. Reflection spent 36.6 unnecessary bid units per trajectory after recovery, versus 2.67 for Full History and 3.20 for the scope-aware method. One Reflection world-shock trajectory missed four post-recovery allocations. The mechanism is repeated invention and consolidation of hidden tie-breaking, identity priority, and a separate “Erin” competitor.

### Public goods

After a named participant's one-round zero contribution, Reflection produced post-recovery welfare loss in 3/5 trajectories: mean 8.0 units, bootstrap CI [2.0, 14.0]. Full History and the scope-aware method lost 0. All partner contributions returned to 10 by the final round, so this is a **temporary welfare reduction**, not persistent cooperation collapse.

## What the experiment does not support

- No action reached the predefined extreme zones near either action bound.
- No fish-stock collapse or lasting environmental damage occurred.
- No lasting public-goods cooperation collapse occurred.
- No persona drift occurred.
- The controller is not perfect: isolated auction overbids occurred, although far less often than under Reflection.
- Rule-based partners establish causal isolation but do not replace a later fully endogenous multi-LLM-group validation.

The defensible claim is therefore:

> Unconstrained reflection can turn ordinary settlement history into persistent self/other and world-model errors. These errors reliably alter actions and can impose measurable economic and social-welfare costs, but the present controlled experiment does not show action-bound extremism, ecological collapse, or durable group breakdown.

## Artifacts

- Formal raw trajectories: `runs/deepseek-consequence-formal-20260830/episodes.jsonl`
- API usage: `runs/deepseek-consequence-formal-20260830/usage.jsonl`
- Analysis JSON and CSV tables: `runs/deepseek-consequence-formal-20260830/analysis/`
- Mechanically selected raw-log audit: `analysis/audit_samples.md`
- Main figure: `analysis/consequence_main.{pdf,svg,png}`
- Trajectory figure: `analysis/consequence_trajectories.{pdf,svg,png}`
- Identity-confusion figure: `analysis/consequence_identity_confusion.{pdf,svg,png}`
