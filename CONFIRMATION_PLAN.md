# Frozen confirmation plan

This plan was written after breadth discovery and before confirmation calls.

## Baselines

`direct`, `full_history`, `summary`, `reflection`.

## Sampling

Three repeats per scenario. The sample intentionally contains discovery-positive cases, negative controls, and boundary cases; it is not restricted to cases supporting the hypothesis.

### Batch A

- `auction_self_need_shift`: discovery-positive self→world reflection error.
- `epidemic_other_violation`: discovery-positive other→world reflection error.
- `grid_bob_overuse`: discovery-positive other→world reflection error.
- `traffic_world_lane_closure`: discovery-positive world→self reflection error.
- `fish_world_anomaly_recovery`: recovery/persistence boundary.
- `public_goods_world_multiplier`: explicit-world negative control.
- `public_goods_david_free_rider`: explicit-other negative control.

### Batch B

- `auction_bob_conditional`: corrected conditional relationship retention boundary.
- `team_self_capability_drop`: self-state errors appeared in summary/direct variants.
- `long_history_late_world_shift`: high-history-pressure negative control.
- `entity_binding_bob_not_david`: entity-binding negative control.
- `salience_other_storm_named`: irrelevant-world-salience negative control.
- `fish_world_regime`: original persistent-world motivation case.
- `fish_other_shift`: original specific-other motivation case.

## Frozen primary outcomes

- scope accuracy;
- protected-scope leakage;
- target-agent accuracy;
- recovery/conditional retention;
- action accuracy;
- raw memory evidence.

The model-based evaluator is excluded because discovery auditing showed systematic false negatives. Raw memory, probe, and action remain available for manual audit.

