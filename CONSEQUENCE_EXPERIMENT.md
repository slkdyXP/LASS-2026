# DeepSeek consequence-chain experiment

## Question

Does the previously observed reflection/consolidation-induced cognitive overgeneralization remain internal, or can it propagate into persistent action changes and measurable social-resource harm?

## Frozen formal design

The formal run was launched only after two pilot defects were corrected: the first stimulus stated the answer too explicitly, and the external controller treated its last action as a policy anchor. Pilot outputs are retained but excluded from formal estimates.

- Model: `deepseek-v4-flash`, real API, temperature 0.2.
- Unit: one 12-round trajectory with one focal LLM agent and four deterministic partners.
- Domains: shared fishery, water auction, and public goods.
- Conditions: no shock, one named-participant shock, and one world shock.
- Memory methods: Full History, unconstrained Reflection, and the external scope-aware controller.
- Repeats: 5 per cell.
- Matrix: 3 domains × 3 conditions × 3 methods × 5 repeats = 135 trajectories.
- Probes: rounds 5, 8, and 12; probes are never written back into memory.
- Raw artifacts: every observation, action, settlement, memory snapshot, probe context, model response, and API-usage record.

Deterministic partners are deliberate: they prevent a second LLM's stochasticity from obscuring whether the focal agent's cognition caused the downstream change. This is a controlled causal-isolation experiment, not yet a fully endogenous multi-LLM society.

## Causal structure

```text
matched transient event
        ↓
focal memory/belief update
        ↓
post-recovery action deviation
        ↓
domain mechanism
  fishery: harvest / stock
  auction: bid / budget / health
  public goods: contribution / reciprocal partner cascade / welfare
```

The no-shock condition distinguishes shock-induced errors from instability created by repeated reflection itself. Outcome accounting excludes the intervention round wherever possible, so the direct physical cost of a pump failure or contamination is not mislabeled as an agent-caused consequence.

## Primary measurements

1. **Cognition:** late scope, update strengths, temporary/persistent judgment, group generalization, and persona drift. The composite overgeneralization score is secondary; all components remain visible.
2. **Behavior:** post-recovery deviation from a domain-specific oracle action, persistent last-three-round deviation, and extreme-action count.
3. **Consequences:**
   - fishery: focal yield loss and remaining stock deficit;
   - auction: unnecessary winning-bid expenditure, missed allocations, health, and budget;
   - public goods: post-recovery group-welfare loss, focal payoff, and partner-contribution cascade.

## Analysis commitments

- Refuse the main analysis when any formal cell is missing or duplicated.
- Report raw trajectories and method/condition/domain breakdowns, not only an aggregate.
- Use matched shock-minus-control effects within method, domain, and repeat.
- Report bootstrap 95% confidence intervals and sample sizes.
- Treat cognition–action correlation as association, not mediation proof.
- If cognition changes without action or outcome changes, conclude that the tested consequence chain is unsupported.
- If Full History or the proposed method is worse in a domain, retain and report that result.

## Figures

The analysis script creates editable PDF/SVG and 600-dpi PNG outputs:

- cognition by method and condition;
- persistent action deviation by method and condition;
- control-adjusted post-recovery domain harm;
- cognitive-change versus action-change association;
- all round-by-round action trajectories with uncertainty bands.

Run with:

```bash
python3 scripts/analyze_consequences.py RUN_DIR --output RUN_DIR/analysis
```
