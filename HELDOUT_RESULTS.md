# Frozen held-out confirmation

## Protocol

The final method was frozen before any live held-out result was inspected. Eight new scenarios in four previously unused domains were then run with three repeats and two checkpoints per trial:

- shared GPU cluster;
- clinic inventory depot;
- greenhouse irrigation;
- logistics sorter.

Each domain contains matched interventions separating persistent world change from a named participant's conditional event or a resolved anomaly. Five baselines were randomly interleaved:

1. `reflection`: free-form reflection, with persona supplied to the memory writer;
2. `guarded_reflection`: prompt-only caution without a fixed schema;
3. `structured_reflection`: six-section structure without evidence gates;
4. `evidence_gated_memory_only`: six-section structure plus evidence-gated consolidation, with the same decision prompt as the other memory baselines;
5. `evidence_gated_reflection`: the full method plus decision-time minimum-sufficient-response guidance.

The run produced 240 checkpoint records and no failed trials. Raw prompts, memories, actions, and probes are in `runs/heldout-final-20260826/records.jsonl`.

## Main results

| Baseline | Scope accuracy | Protected leakage ↓ | Action accuracy |
|---|---:|---:|---:|
| Reflection | 72.9% | 0.0979 | 72.9% |
| Guarded reflection | 91.7% | 0.0028 | 75.0% |
| Structured reflection | 91.7% | 0.0398 | 87.5% |
| Evidence-gated memory only | **95.8%** | **0.0028** | **95.8%** |
| Full evidence-gated reflection | **100.0%** | **0.0014** | 93.8% |

The cleanest primary method comparison is Reflection versus `evidence_gated_memory_only`, because both use the same decision prompt:

- scope: 11 checkpoints improved, 0 regressed; exact paired McNemar p=0.00098;
- action: 11 improved, 0 regressed; exact paired McNemar p=0.00098.

For the full method versus Reflection:

- scope: 13 improved, 0 regressed; p=0.00024;
- action: 12 improved, 2 regressed; p=0.01294.

These p-values are descriptive because checkpoints are clustered within scenarios and there are only eight scenario families.

## Persistent-change and recovery split

| Subset | Baseline | Scope accuracy | Leakage ↓ | Action accuracy |
|---|---|---:|---:|---:|
| Persistent change | Reflection | 91.7% | 0.101 | 58.3% |
| Persistent change | Evidence-gated memory only | 95.8% | 0.006 | 91.7% |
| Recovery/conditional event | Reflection | 54.2% | 0.094 | 87.5% |
| Recovery/conditional event | Evidence-gated memory only | 95.8% | 0.000 | 100.0% |

The method therefore did not obtain its improvement by refusing to recognize real persistent change. Its largest gain is on conditional and recovered events, where free-form Reflection often retained system-level or long-term interpretations.

## Ablation interpretation

- Guarding the prompt sharply reduces protected-scope leakage, so explicit epistemic caution matters.
- Structure alone improves scope and action, but retains substantially more leakage than evidence gating.
- Evidence-gated memory improves both cognition and action without changing the decision prompt.
- The extra decision-time guidance raises scope from 95.8% to 100% but does not improve action over memory-only gating (93.8% versus 95.8%). The paper should therefore use `evidence_gated_memory_only` as the primary method and treat the full decision guidance as an optional variant.

## Memory size

Mean memory snapshot length in characters:

| Baseline | Mean characters |
|---|---:|
| Reflection | 2746.5 |
| Guarded reflection | 1041.8 |
| Structured reflection | 2189.9 |
| Evidence-gated memory only | 1884.1 |
| Full evidence-gated reflection | 1908.2 |

The improvement is not explained by a longer memory: both evidence-gated variants are shorter than free-form Reflection at the measured checkpoints. API token usage was not retained by the original client, so character length is only a proxy.

## Remaining limitations

- These held-out scenarios were written after the broad phenomenon-discovery phase, but before inspecting their live results. They are a stronger test than the development set, not a substitute for benchmark integration.
- Three repeats and eight scenarios remain small; scenario-level uncertainty should be emphasized.
- The claim-level model-assisted audit could not run inside the restricted network sandbox. Scope, leakage, action, and direct manual log inspection remain the completed evidence.
- Closed-loop multi-agent experiments are implemented but await explicit permission to send their synthetic prompts to the configured DeepSeek endpoint.
