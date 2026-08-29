# External Controller and Long-Context Experiment Update

## Changes since the previous `main`

### Executable six-module controller

The repository now contains an external memory controller whose state transitions are executed in Python rather than described as decorative terminology inside the Agent prompt. It preserves the six operational roles:

1. `STABLE PERSONA`
2. `CURRENT SELF STATE`
3. `CONSOLIDATED MODELS`
4. `OPEN HYPOTHESES`
5. `RECENT OBSERVED EPISODES`
6. `ACTION POLICY`

`Contextual Phase-Transition Gate (CPTG)` keeps the two slow-memory modules dormant during short interactions and activates them after the configured event/context threshold. Evidence is accumulated externally before activation and retrospectively consolidated when the gate opens. The event-parser claim catalog is capped at 32 entries so parser input remains bounded at long horizons.

Primary implementation files:

- `scopeprobe/external_memory.py`
- `scopeprobe/memory.py`
- `scopeprobe/runner.py`
- `EXTERNAL_CONTROLLER_METHOD.md`

### Provider and reliability support

- Added `deepseek`, `openai`, and `claude` provider selection.
- Added per-call `usage.jsonl` records with provider, scenario, baseline, repeat, call type, token counts, cache hits, and finish reason.
- Added retries for empty/invalid JSON and network failures.
- Disabled default DeepSeek V4 thinking for structured calls to prevent reasoning tokens from consuming the response budget.
- API credentials remain in ignored local dotenv files and are not committed.

### Long-context stress suite

`scripts/generate_long_scale_scenarios.py` deterministically generates `configs/scenarios_long_scale.json` with a full factorial design:

- GovSim-compatible fishing rules and Alympics-compatible water-allocation rules;
- 50 and 100 rounds;
- 5 and 12 observed participants;
- matched `world` and `specific-other` persistent changes;
- explicit but irrelevant social distractors;
- four frozen checkpoints per trajectory.

These are controlled trace-replay memory stress tests derived from the public environment rules. They are not represented as executions of the original closed-loop GovSim or Alympics code.

## Phase-1 controlled live experiment

Run: `runs/phase1-controlled-r1-20260829`

- 29 scenarios, five methods, one repeat;
- 145 completed trajectories;
- 765 Agent-rounds and 285 checkpoints;
- 1,662 valid model responses and zero failed trials;
- maximum Full History input: 1,209 tokens.

| Method | Scope accuracy | Action accuracy | Protected leakage |
|---|---:|---:|---:|
| Full History | 100.0% | 94.7% | 0.000 |
| Always-4 | 96.5% | 93.0% | 0.002 |
| CPTG | 96.5% | 91.2% | 0.001 |
| Always-6 | 91.2% | 94.7% | 0.003 |
| Reflection | 96.5% | 78.9% | 0.034 |

This run is a short-horizon controlled experiment. It does not test the claimed long-context advantage.

## DeepSeek long-scale run

Run: `runs/deepseek-long-scale-formal-20260829`

Planned design:

- 16 scenarios × 5 methods × 3 repeats = 240 trajectories;
- 33,360 planned model calls;
- 50/100 rounds and 5/12 observed participants.

Observed API usage before interruption:

- 16,912 successful calls;
- 30,057,830 input tokens;
- 17,115,648 cache-hit tokens;
- 4,946,628 output tokens;
- maximum Full History input: 20,609 tokens;
- estimated DeepSeek-equivalent cost: approximately CNY 44–45, excluding proxy-specific pricing.

### Completion failure

Only 116/240 trajectories completed. Of the 124 failed trajectories, 122 ended after the proxy began returning `HTTP 401 Unauthorized`; two ended because the model emitted an out-of-range fishing action. Only 4/48 scenario-repeat blocks contain all five methods. Therefore the aggregate table below is descriptive partial data and must not be used as a balanced formal comparison.

| Method | Completed checkpoints | Scope accuracy | Action accuracy | Protected leakage |
|---|---:|---:|---:|---:|
| Full History | 92 | 100.0% | 87.0% | 0.000 |
| CPTG | 108 | 93.5% | 60.2% | 0.000 |
| Always-6 | 92 | 83.7% | 84.8% | 0.004 |
| Always-4 | 84 | 86.9% | 77.4% | 0.000 |
| Reflection | 88 | 64.8% | 69.3% | 0.026 |

The available data do **not** show Full History degrading below Reflection or CPTG. CPTG's main current weakness is action selection, especially its insufficient bidding response in water-allocation world-change cases. Because missing trajectories are extensive and unbalanced, the long-scale experiment must be completed before any confirmatory claim.

## Required next steps

1. Restore or replace the DeepSeek proxy credential/quota and rerun only missing trajectory keys.
2. Add resumable execution so a provider interruption does not discard an entire expensive batch.
3. Add equal client-side context budgets (for example 4k, 8k, 16k, and unrestricted) to test memory efficiency rather than relying on the model's hard context limit.
4. Fix and freeze CPTG action compilation, then evaluate it without changing labels or selectively removing failures.
5. Run the original closed-loop GovSim and Alympics environments as a separate ecological-validity layer.

## Verification

The current test suite contains 17 unit tests and passes with:

```bash
python3 -m unittest discover -s tests -v
```
