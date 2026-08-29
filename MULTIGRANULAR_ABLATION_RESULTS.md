# Multi-granular analysis of the six- and four-component ablations

## Scope and limits

This report re-analyzes the live DeepSeek held-out ablations at three granularities. The six-component table contains the frozen full method plus six leave-one-out variants; the four-component table contains the newly sampled four-component baseline plus four leave-one-out variants.

The existing runner saved only checkpoint rounds. Therefore, "round-level" below means the 48 saved checkpoint rounds per condition, not every environment round. A trajectory is one `(scenario, repeat)` unit containing two saved checkpoints, giving 24 trajectories per condition. Non-checkpoint adaptation lag, recovery lag, and full cumulative reward cannot be reconstructed from these logs.

Normalized action violation is the distance outside the registered acceptable interval divided by the scenario's full action range. Values inside the interval have zero violation. `Above` and `Below` mean numerically above or below the registered interval; they are not semantic labels for over- and under-reaction across every domain.

Claim measurements come from a new temperature-0 DeepSeek forensic audit of every memory snapshot against all source observations available through that checkpoint. All 576 required audits completed without failure: 48 full six-component control snapshots, 288 six-way ablation snapshots, and 240 four-way snapshots. This is model-assisted annotation using the same model family as the agents, not independent human ground truth. The auditor lists at most three unsupported claims and does not enumerate all supported claims, so `unsupported/snapshot` is a count, not a true claim error rate.

All positive audit cases were subsequently inspected. Several are debatable or likely false positives: the auditor sometimes treats the agent's supplied current action as absent from the evidence, and sometimes rejects a stable norm after three or more consistent observations despite its own rubric allowing consolidation after two independent consistent observations. Claim-level numbers are therefore exploratory diagnostics only; they must not be presented as validated publication results without independent human annotation.

## Six-component ablation

### Saved-round behavior and cognition

| Condition | n | Action acc. | Norm. violation ↓ | Above | Below | Scope acc. | Scope margin ↑ | Leakage ↓ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Full six components | 48 | 95.8% | 0.42% | 4.2% | 0.0% | 95.8% | 0.344 | 0.0028 |
| Without stable persona | 48 | 100.0% | 0.00% | 0.0% | 0.0% | 95.8% | 0.269 | 0.0042 |
| Without current self state | 48 | 95.8% | 0.42% | 4.2% | 0.0% | 93.8% | 0.306 | 0.0000 |
| Without consolidated models | 48 | 97.9% | 0.10% | 2.1% | 0.0% | 100.0% | 0.304 | 0.0035 |
| Without open hypotheses | 48 | 97.9% | 0.21% | 2.1% | 0.0% | 100.0% | **0.360** | 0.0000 |
| Without recent episodes | 48 | 87.5% | 1.46% | 6.2% | 6.2% | 95.8% | **0.398** | 0.0014 |
| Without action policy | 48 | **72.9%** | **4.27%** | **27.1%** | 0.0% | 95.8% | 0.340 | 0.0000 |

The continuous violation measure confirms that `ACTION POLICY` errors are not merely a binary-threshold artifact: removing it increases mean violation approximately tenfold relative to the full six-component control. Removing recent episodes also increases violation, with errors on both sides of the acceptable interval.

### Claim-level forensic audit

| Condition | Snapshots | Overgeneralization snapshots | Unsupported claims/snapshot | Stale-after-recovery | Action relies on unsupported claim |
|---|---:|---:|---:|---:|---:|
| Full six components | 48 | 0.0% | 0.000 | 0.0% | 0.0% |
| Without stable persona | 48 | 0.0% | 0.000 | 0.0% | 0.0% |
| Without current self state | 48 | 0.0% | 0.000 | 0.0% | 0.0% |
| Without consolidated models | 48 | 0.0% | 0.000 | 0.0% | 0.0% |
| Without open hypotheses | 48 | 4.2% | 0.083 | 0.0% | 4.2% |
| Without recent episodes | 48 | 0.0% | 0.000 | 0.0% | 0.0% |
| Without action policy | 48 | **8.3%** | 0.083 | 0.0% | **8.3%** |

The raw model audit finds a small signal that removing open hypotheses sometimes turns limited observations into stable norms or regimes. Removing action policy also receives unsupported action-guiding flags in four snapshots. Manual review found questionable flags in this set, and most cells remain zero, so this claim table is not reliable enough for a confirmatory comparison.

### Trajectory-level aggregation

| Condition | Trajectories | All actions correct | All scopes correct | Jointly clean trajectory | Mean cumulative norm. violation ↓ | Any audited overgeneralization |
|---|---:|---:|---:|---:|---:|---:|
| Full six components | 24 | 91.7% | 91.7% | 83.3% | 0.83% | 0.0% |
| Without stable persona | 24 | 100.0% | 91.7% | 91.7% | 0.00% | 0.0% |
| Without current self state | 24 | 91.7% | 87.5% | 79.2% | 0.83% | 0.0% |
| Without consolidated models | 24 | 95.8% | 100.0% | 95.8% | 0.21% | 0.0% |
| Without open hypotheses | 24 | 95.8% | 100.0% | 95.8% | 0.42% | 8.3% |
| Without recent episodes | 24 | 75.0% | 91.7% | 66.7% | 2.92% | 0.0% |
| Without action policy | 24 | **58.3%** | 91.7% | **54.2%** | **8.54%** | **12.5%** |

For persistent-change trajectories specifically, only 16.7% of trajectories remain action-correct at both checkpoints without action policy, compared with 83.3% for the full six-component control. Recovery trajectories remain 100% action-correct in both conditions. The main policy failure is therefore response to persistent verified changes rather than recovery from transient events.

## Four-component ablation

### Saved-round behavior and cognition

| Condition | n | Action acc. | Norm. violation ↓ | Above | Below | Scope acc. | Scope margin ↑ | Leakage ↓ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Four-component baseline | 48 | **97.9%** | **0.10%** | 2.1% | 0.0% | 97.9% | 0.306 | 0.0014 |
| Without stable persona | 48 | 91.7% | 0.83% | 6.2% | 2.1% | 91.7% | 0.294 | 0.0049 |
| Without current self state | 48 | 95.8% | 0.42% | 4.2% | 0.0% | 97.9% | **0.346** | 0.0007 |
| Without recent episodes | 48 | 91.7% | 0.73% | 8.3% | 0.0% | 97.9% | 0.323 | 0.0014 |
| Without action policy | 48 | **81.3%** | **3.02%** | **18.8%** | 0.0% | **100.0%** | **0.438** | 0.0014 |

Again, removing action policy improves the self-reported scope score and margin while substantially worsening continuous behavior. This is direct evidence that better probe cognition does not imply better action in this setup.

### Claim-level forensic audit

| Condition | Snapshots | Overgeneralization snapshots | Unsupported claims/snapshot | Stale-after-recovery | Action relies on unsupported claim |
|---|---:|---:|---:|---:|---:|
| Four-component baseline | 48 | 0.0% | 0.000 | 0.0% | 0.0% |
| Without stable persona | 48 | 2.1% | 0.042 | 0.0% | 2.1% |
| Without current self state | 48 | 0.0% | 0.000 | 0.0% | 0.0% |
| Without recent episodes | 48 | 0.0% | 0.000 | 0.0% | 0.0% |
| Without action policy | 48 | 0.0% | 0.000 | 0.0% | 0.0% |

The only positive four-component claim audit is one `without stable persona` snapshot containing two unsupported statements. In contrast, the no-policy condition has no audited unsupported beliefs despite many action errors. This supports a belief-to-action failure rather than cognitive overgeneralization for that condition.

### Trajectory-level aggregation

| Condition | Trajectories | All actions correct | All scopes correct | Jointly clean trajectory | Mean cumulative norm. violation ↓ | Any audited overgeneralization |
|---|---:|---:|---:|---:|---:|---:|
| Four-component baseline | 24 | **95.8%** | 95.8% | **91.7%** | **0.21%** | 0.0% |
| Without stable persona | 24 | 83.3% | 83.3% | 66.7% | 1.67% | 4.2% |
| Without current self state | 24 | 91.7% | 95.8% | 87.5% | 0.83% | 0.0% |
| Without recent episodes | 24 | 87.5% | 95.8% | 83.3% | 1.46% | 0.0% |
| Without action policy | 24 | **70.8%** | **100.0%** | **70.8%** | **6.04%** | 0.0% |

On persistent-change trajectories, all-actions-correct falls from 91.7% for the four-component baseline to 41.7% without action policy. Recovery trajectories remain 100% action-correct. Removing recent episodes reduces persistent all-actions-correct to 75.0%; removing stable persona reduces it to 75.0% and also harms recovery scope, although neither effect was reliable in the earlier checkpoint-level significance tests.

## Cross-granularity conclusion

The finer analysis changes the interpretation in three ways:

1. `ACTION POLICY` has the only large, consistent contribution across saved-round violation magnitude and trajectory success. Its effect is behavioral, especially under persistent world change, and does not require an audited false belief.
2. `RECENT OBSERVED EPISODES` has a smaller but directionally consistent behavioral contribution in both ablation families. The evidence remains underpowered.
3. Stable persona, current self state, consolidated models, and open hypotheses do not show stable independent effects across both runs. Open hypotheses may suppress a few unsupported consolidations, but the claim audit signal is small and model-judged.

These analyses improve measurement resolution but do not fix the fundamental sample-size problem: there are still only eight independent scenarios and 24 clustered trajectories per condition. The six-component control was also collected in an earlier batch than its ablations. No causal module-necessity claim should be based on these tables alone.

For the next run, the logger must save every round's action, memory snapshot, environment outcome, and claim set. That is required to measure real adaptation lag, recovery lag, cumulative reward/regret, and claim survival time rather than only two checkpoint slices.
