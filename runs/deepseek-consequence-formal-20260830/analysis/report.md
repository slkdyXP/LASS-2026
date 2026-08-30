# Consequence-chain analysis

- Episodes: 135
- Balanced matrix: True
- Source error records: 0
- Model calls: 3105

## Paired method comparisons

| Metric | Contrast | n | Mean difference | 95% bootstrap CI | Wilcoxon P |
|---|---|---:|---:|---:|---:|
| late_overgeneralization | Reflection − Full history | 45 | 0.1189 | [0.0494, 0.1950] | 0.002749 |
| late_overgeneralization | Reflection − Scope-aware memory | 45 | 0.1094 | [0.0411, 0.1872] | 0.02714 |
| oracle_normalized_action_mae | Reflection − Full history | 45 | 0.0213 | [0.0136, 0.0302] | 4.205e-06 |
| oracle_normalized_action_mae | Reflection − Scope-aware memory | 45 | 0.0209 | [0.0131, 0.0294] | 8.077e-06 |
| oracle_extreme_action_rounds | Reflection − Full history | 45 | 0.0000 | [0.0000, 0.0000] | 1 |
| oracle_extreme_action_rounds | Reflection − Scope-aware memory | 45 | 0.0000 | [0.0000, 0.0000] | 1 |

> Wilcoxon P values are descriptive because trajectories are clustered within only three domains.
