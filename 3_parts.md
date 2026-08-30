可以，Introduction、Related Work 和 Preliminaries 已经能基本定稿。三部分共同完成一件事：

> Introduction 提出问题，Related Work 划清缺口，Preliminaries 把问题变成可检验的数学对象。

## 1. Introduction：为什么这是一个值得研究的问题

建议 5 段。

第一段：社会模拟中的 memory 不是普通上下文，而是社会状态。

> 长程社会模拟要求 agent 将互动历史转化为关于自己、特定他人和共享环境的持久信念。这些信念进一步决定信任、合作、惩罚和资源分配，因此 memory consolidation 会直接影响模拟出的社会机制。

第二段：现有评价存在盲区。

> 现有社会模拟主要评价最终行动、群体收益和行为可信度，memory benchmark 则主要评价事实能否被保存、更新和检索。但这些指标无法判断 agent 是否因为正确的原因形成了正确的社会信念。

第三段：提出核心反直觉现象。

> 我们发现 agent 可以记住正确的事件，却从中学到错误的教训。一次属于特定个体的异常行为可能被固化为世界规则，一次暂时冲击可能被延伸为长期规律；我们将这一过程称为 reflective misconsolidation，其主要表现是 scope interference。

第四段：介绍 ScopeProbe、核心发现和缓解。

> 我们提出 ScopeProbe，通过构造结果相似但潜在原因不同的 matched social trajectories，分别审计 memory、belief attribution 和 action。实验表明，该问题不是普通遗忘：full history 通常能保留作用域，而 unconstrained reflection 更容易产生跨实体和跨时间的持久化错误。基于诊断结果，我们进一步提出 evidence-gated consolidation 作为轻量缓解。

第五段：贡献总结。

贡献保持三点即可：

1. 形式化 social-agent memory 中的 causal-scope preservation 问题。
2. 提出 ScopeProbe，对 `event → memory → belief → action` 进行干预式诊断。
3. 发现 reflective misconsolidation 的边界和行为后果，并验证 diagnosis-derived mitigation。

Introduction 的最终 takeaway：

> Social simulation should evaluate not only whether agents reach plausible outcomes, but whether they learn the right social model for the right reason.

------

## 2. Related Work：现有工作覆盖了什么，我们缺的是什么

建议只设三个小节。

### 2.1 LLM Agents for Social Simulation

> Generative Agents、SOTOPIA、ALYMPICS 和 GovSim 展示了 LLM agent 在开放社会互动、战略博弈和公共资源治理中的潜力。MoralAgentSim、Spiral of Silence 等工作进一步利用受控模拟研究具体社会机制。这些工作主要从互动行为或群体结果理解 agent，而我们关注产生这些结果的持久信念更新是否具有正确的因果依据。

这里还要明确：

> 我们的资源治理场景是受 GovSim 和 ALYMPICS 启发的 synthetic diagnostic adaptations，而不是对原始 benchmark 的闭环复现。

### 2.2 Reflection and Persistent Agent Memory

> Generative Agents 和 Reflexion 将 reflection 建立为从经验中抽象长期信息的常用机制。MemoryAgentBench、HaluMem、TrustMem 和 memory-management studies 开始评价检索、更新、幻觉及错误传播。但事实保真并不等于认识论保真：reflection 可能准确保留事件内容，却改变该事件是关于谁、什么机制以及多长时间的证据。

### 2.3 Attribution, Temporal Validity, and Memory-to-Action

> PASB 已发现 persistent sycophancy 中的 attribution removal 和 scope broadening；STALE 研究旧信念的隐式失效；Mem2ActBench 将记忆连接到行动；actor–observer asymmetry 则揭示视角导致的归因偏差。ScopeProbe 将这些问题带入受控社会模拟，用 matched causal interventions 联合评价 self、other、world 和 temporal scope，并追踪 protected-belief leakage 及其行动后果。

Related Work 的最后一句应直接锁定缺口：

> Existing work studies whether memories are faithful, current, or useful; we study whether social evidence is consolidated at the correct epistemic address.

------

## 3. Preliminaries and Problem Formulation：我们究竟在测什么

这一节建议不要只叫 `Preliminaries`，而叫：

> **Preliminaries and Problem Formulation**

它应该完成四个定义。

### 3.1 Social Agent with Persistent Memory

> 在时间 \(t\)，agent 接收观察 \(o_t\)，memory updater \(U\) 将观察和旧记忆 \(m_{t-1}\) 转化为新记忆 \(m_t\)。Agent 随后根据观察和持久记忆形成信念 \(b_t\)，并通过 policy 选择行动 \(a_t\)。

用一条链概括：

\[ o_t \xrightarrow{U} m_t \xrightarrow{B} b_t \xrightarrow{\pi} a_t . \]

这里强调 ScopeProbe 诊断的是中间状态，而不只看最终行动。

### 3.2 Epistemic Address of a Memory Claim

把一个持久 claim 写成：

\[ c=(\phi,z,e,\tau,w), \]

其中：

- \(\phi\)：claim 的具体内容；
- \(z\)：作用域，如 self、other 或 world；
- \(e\)：claim 所对应的具体实体；
- \(\tau\)：时间有效范围；
- \(w\)：支持该 claim 的证据。

核心概念是：

> 正确记忆一个事件，不仅要求内容 \(\phi\) 正确，还要求它被写入正确的 scope、entity 和 temporal validity。这些字段共同构成 claim 的 epistemic address。

### 3.3 Reflective Misconsolidation

> 给定截至时间 \(t\) 的证据 \(E_t\)，只有能被证据支持的持久 claims 才属于 licensed belief set \(\mathcal G_t\)。如果 reflection 写入了一个高置信度、但其作用域或持续时间不受 \(E_t\) 支持的 claim，就发生了 reflective misconsolidation。

主要错误类型定义为：

- Cross-scope misattribution：other evidence 被升级为 world belief，或反之。
- Entity overgeneralization：一个人的行为被推广到所有参与者。
- Temporal overextension：暂时或已恢复的状态被固化为长期规律。
- Mechanism invention：从结果中写入证据不支持的因果解释。

`scope interference` 是这些错误在观测上的总称。

### 3.4 Diagnostic Objective

> ScopeProbe 构造 observable outcome 相似、但真实 causal source 不同的 matched trajectories。好的 memory updater 应增强目标作用域中的正确信念，同时保持非目标的 protected beliefs 不变，并使后续行动响应真正发生变化的部分。

因此评价分成三层：

1. Memory：持久化文本写入了什么。
2. Belief：agent 将事件归因给谁或什么。
3. Action：该信念是否改变后续决策。

主要指标对应：

- Target Scope Accuracy；
- Protected-Belief Leakage；
- Scope Separation；
- Action Accuracy。

------

## 三部分连起来的完整逻辑

> 社会模拟依赖持久信念
> → 现有 outcome 和 recall 指标看不到信念的因果来源
> → reflection 可能记对事件却学错作用域
> → 我们将 claim 的 scope、entity 和 temporal validity 形式化为 epistemic address
> → ScopeProbe 用 matched interventions 检验它
> → evidence-gated consolidation 根据诊断结果缓解该问题。

到这里，论文前半部分的主干已经稳定。后面的 Method 只需要解释 ScopeProbe 如何实例化这些定义，Experiments 则依次回答“现象是否存在、边界在哪里、是否影响行动、缓解是否有效”。