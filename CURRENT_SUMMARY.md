# 当前工作总结

## 问题

普通 Reflection Agent 通常能正确记住事件来源，但会把少量证据过度总结为长期因果规律，例如从某个 Agent 的一次异常行为推导隐藏阈值、系统脆弱性或群体特征。这种问题主要发生在认知和记忆巩固阶段，有时会进一步导致错误行动。

## 方法

提出 **Evidence-Gated Memory**，将记忆分为：

- Stable Persona
- Current Self State
- Consolidated Models
- Open Hypotheses
- Recent Observed Episodes
- Action Policy

核心规则：单次事件只能作为 episode 或不确定 hypothesis；只有重复一致证据或明确记录的持续因果证据才能进入 consolidated model；恢复和反证会削弱旧假设。当前已验证危险仍允许触发最小、可逆的即时响应。

## 实验

- 开发阶段：14 个场景、3 次重复、84 个 checkpoint。
- 冻结 held-out：8 个全新场景、4 个新领域、5 个消融方法、3 次重复，共 240 个 checkpoint，0 个失败 trial。
- 公平消融包括：Reflection、Guarded Reflection、Structured Reflection、Evidence-Gated Memory 和完整 Evidence-Gated Reflection。

Held-out 核心结果：

| 方法 | Scope Accuracy ↑ | Leakage ↓ | Action Accuracy ↑ |
|---|---:|---:|---:|
| Reflection | 72.9% | 0.0979 | 72.9% |
| Guarded Reflection | 91.7% | 0.0028 | 75.0% |
| Structured Reflection | 91.7% | 0.0398 | 87.5% |
| **Evidence-Gated Memory** | **95.8%** | **0.0028** | **95.8%** |

Evidence-Gated Memory 与 Reflection 使用相同决策提示。前者在 Scope 和 Action 上均有 11 个 checkpoint 改善、0 个退化，配对 McNemar `p=0.00098`。

## 结论

当前证据支持：

> Reflection 的主要问题不是遗忘信息来源，而是把有限证据过度巩固为长期机制。Evidence-Gated Memory 能显著减少这种认知过度泛化，同时保留对真实持续变化的识别和行动能力。

目前最适合作为论文主方法的是 **Evidence-Gated Memory**，因为它只改变记忆机制，不额外修改决策提示。尚需完成 claim-level 人工/模型辅助审计，以及闭环多 Agent 社会模拟，才能进一步证明对长期群体结果的影响。
