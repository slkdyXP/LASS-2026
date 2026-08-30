可以把这篇工作包装得很 solid，但关键不是“把薄实验说厚”，而是把它组织成一套闭合的证据链：

> 一个反直觉社会认知现象 → 一个能隔离该现象的诊断 harness → 三个机制性 insight → 一个由诊断直接推导出的轻量缓解方案。

论文应当是 50% 问题分析、30% ScopeProbe、20% mitigation，而不是新架构论文。

## 1. 这些代表性工作的共同叙事套路

| 工作                               | 最有效的叙事动作                                             | 我们应该借鉴什么                                             |
| ---------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| GovSim                             | “Cooperate or Collapse”的公共资源困境 → benchmark → 找到失败机制 → 用 Universalization 做初步缓解。[NeurIPS 2024](https://papers.neurips.cc/paper_files/paper/2024/file/ca9567d8ef6b2ea2da0d7eed57b933ee-Paper-Conference.pdf) | 不停留在“模型失败”，而是回答“为什么失败、这一诊断能否导出干预” |
| Spiral of Silence                  | 从经典社会理论提出中心问题，再用 `History × Persona` 的四个受控条件拆解机制。[EMNLP Findings 2025](https://aclanthology.org/2025.findings-emnlp.1262/) | 把实验组织成概念因子的交叉，而不是一堆场景和 baseline        |
| Everyone Conforms, No One Believes | 用悖论式标题抓住 private belief/public behavior gap，并把结果上升到“模拟器可能高估规范稳定性”。[SocialSim 2026](https://arxiv.org/abs/2608.02758) | 我们也需要一个“记得事件，却学错教训”的悖论和 simulator-validity implication |
| CRAFT                              | 先问“更强个体推理是否意味着更强协作”，再用 oracle 隔离通信瓶颈，最后给出 failure taxonomy；结论是更强推理并不可靠地转化为更好协作。[CRAFT](https://arxiv.org/abs/2603.25268) | ScopeProbe 必须被描述成隔离 memory consolidation 的实验仪器  |
| Why Are We Moral?                  | 从“自利进化为何产生利他道德”的社会科学 puzzle 开始，再说明 LLM simulation 能操纵传统模型无法表达的认知因素。[ACL 2026](https://github.com/MoralAgentSim/social-evol-sim) | 从社会认知问题出发，而不是从 memory module 出发              |
| BEACOF                             | 静态协作造成 groupthink/deadlock → 不完全信息下的 belief update → 动态干预。[WWW 2026](https://arxiv.org/abs/2603.24973) | 借鉴“failure → belief mechanism → intervention”，但不要借它过重的理论术语 |

它们最成功的共同点不是实验一定极厚，而是：

> 每篇论文只有一个容易复述的社会性矛盾，benchmark/harness 被用来隔离矛盾，方法只是回答由分析自然产生的问题。

------

# 2. 我们最强的核心悖论

我建议把整篇论文的 hook 改成：

> **Social agents can remember the right event but learn the wrong lesson.**

更完整的技术表述：

> Reflection is causally lossy: it often preserves what happened while blurring who or what the event is evidence about.

这比“Reflection 存在 cross-scope interference”更好懂，也更像上述顶会论文的中心 insight。

它对应一个非常清楚的反直觉现象：

- Agent 正确记得 Bob 做了异常行为；
- 但 Reflection 把它写成“市场机制已经变化”；
- Agent 正确记得一次供应冲击；
- 但冲击恢复后仍把它作为长期行动依据。

因此问题不是普通 hallucination，也不只是 forgetting，而是：

> **Reflective misconsolidation**：从事件到持久信念的转换错误。
> **Scope interference**：这种错误在 `self / other / world / temporal` 作用域上的表现。

建议统一术语：

- 过程：`reflective misconsolidation`
- 错误模式：`scope interference`
- harness：`ScopeProbe`
- 缓解原则：`evidence-gated consolidation`
- 方法：`Evidence-Gated Memory`
- 外部实现：`Executable Evidence-Gated Controller`

正文尽量不突出 HSCM、Hexahedral Manifold 等名字。它们容易让 reviewers 把论文看成术语重、证据弱的 prompt architecture。

------

# 3. 推荐标题

首选：

> **The Right Event, the Wrong Lesson: Diagnosing Reflective Misconsolidation in Social LLM Agents**

如果必须突出 harness：

> **ScopeProbe: When Social LLM Agents Remember the Right Event but Learn the Wrong Lesson**

更保守的技术标题：

> **ScopeProbe: Diagnosing Reflection-Induced Scope Interference in Social LLM Agents**

我最推荐第一个。它同时具备：

- GovSim 的结果张力；
- Pluralistic Ignorance 的悖论感；
- CRAFT 的诊断导向；
- 足够明确的技术关键词。

------

# 4. 整篇论文的唯一中心命题

> Social-agent reflection should be treated as a belief-update operator, not a benign memory compressor: unconstrained reflection can misassign the causal scope and temporal validity of social evidence, while controlled diagnosis and evidence-gated consolidation substantially reduce this failure.

所有实验只能服务这句话。

------

# 5. Introduction 应该这样展开

### Paragraph 1：为什么 memory 是社会模拟的科学变量

不要从“LLM agents have achieved remarkable success”开始。

应该从：

> Long-running social simulations require agents to transform interaction histories into persistent beliefs about themselves, particular partners, and the shared environment.

然后指出这些 beliefs 决定信任、合作、惩罚和资源策略。

### Paragraph 2：现有评估的盲区

现有 social simulation 多观察：

- survival；
- cooperation；
- reward；
- final action；
- linguistic plausibility。

但相同的社会结果可能来自完全不同的因果来源：

- 世界规则真的变了；
- 某个人临时异常；
- Agent 自身能力变了。

只看 outcome 无法知道 Agent 学到了什么。

### Paragraph 3：引入悖论案例

放一个完全可视化的 matched pair：

- Case A：所有人行为稳定，但世界容量下降；
- Case B：世界稳定，但 Bob 因一次 emergency 过度使用资源。

宏观结果都出现 shortage。

Full History 保留两者差异；Reflection 却可能把两者都总结成：

> “The shared system is fragile and participants may systematically overconsume.”

然后一句：

> The agent remembers the event, but learns the wrong lesson.

### Paragraph 4：定义现象

定义 reflective misconsolidation：

- 错误 causal scope；
- temporary → persistent；
- named other → group/world；
- self → environment；
- resolved evidence → active policy premise。

强调它区别于 retrieval failure：

> The relevant observation remains available; the error is introduced when experience is rewritten as a persistent lesson.

### Paragraph 5：ScopeProbe

ScopeProbe 通过 matched intervention 控制：

- evidence source；
- temporal pattern；
- persona；
- current observation；
- action space；
- memory mechanism。

并同时审计：

```
source observation → persistent memory → attributed belief → action
```

### Paragraph 6：主要发现

不要堆所有结果，只讲三条：

1. Reflection 不是普遍改善 memory；Full History 往往更可靠。
2. 错误集中在 consolidation，尤其是 conditional/recovered evidence。
3. 认知正确也不保证行动正确，belief consolidation 与 policy compilation 是两个不同瓶颈。

然后介绍 mitigation。

------

# 6. 三条贡献

建议正文只列三条：

1. **A diagnostic problem formulation.**
   We identify reflective misconsolidation as a distinct failure of social LLM agents: locally or temporally valid evidence is promoted into a persistent belief at an unsupported causal scope.
2. **An intervention-based harness.**
   We introduce ScopeProbe, which uses matched social trajectories to isolate evidence source and temporal validity while jointly auditing persistent memory, belief attribution, and behavior.
3. **Mechanistic findings and a diagnosis-derived mitigation.**
   We show that the failure arises from unconstrained consolidation rather than textual memory in general, distinguish belief errors from policy errors, and demonstrate that evidence-gated consolidation substantially reduces both scope leakage and behavioral failures.

不要把“提出六模块架构”列为独立贡献。

------

# 7. 实验不要按数据集写，要按研究问题写

| 研究问题                                                   | 对比                                                    | 得出的 insight                                           |
| ---------------------------------------------------------- | ------------------------------------------------------- | -------------------------------------------------------- |
| RQ1: Does reflection preserve causal scope?                | Full History vs Reflection                              | Reflection 会在保留事件的同时损坏作用域                  |
| RQ2: Is the failure caused by forgetting or consolidation? | Direct / Full History / Summary / Reflection            | Full History 稳健，说明错误主要由重写与抽象引入          |
| RQ3: What part of consolidation matters?                   | Reflection → Guarded → Structured → Evidence-Gated      | prompt caution、structure、evidence gate 构成逐层干预    |
| RQ4: When does it occur?                                   | Persistent vs conditional vs recovery；self/other/world | 错误具有 scope × time 边界，不是普遍失败                 |
| RQ5: Does a wrong belief affect behavior?                  | memory text + probe + action                            | 部分 cognition error 会传播为 action error               |
| RQ6: Can diagnosis guide mitigation?                       | Reflection vs Evidence-Gated Memory                     | 作用域和行动均从 72.9% 提升到 95.8%                      |
| RQ7: Are belief and policy separable?                      | module ablation                                         | Action Policy 是主要行为组件，但不决定 scope attribution |

这样即使样本量不大，论文仍然显得“分析充分”，因为每组实验回答不同的机制问题，而不是反复测 accuracy。

------

# 8. ScopeProbe 的正确定位

不要叫普通 benchmark。建议写成：

> **An intervention-based diagnostic harness for epistemic credit assignment in social agents.**

CRAFT 使用 oracle 隔离 communication；ScopeProbe 使用 matched causal interventions 隔离 memory consolidation。

你们的价值不在“大规模模拟”，而在：

- 已知真实 causal source；
- matched macro outcomes；
- 可控 temporal transition；
- 非持久 belief probe；
- memory–belief–action 三层日志；
- negative controls；
- discovery 后冻结 held-out。

可以直接用一句：

> ScopeProbe functions as a unit-test suite for the epistemic integrity of social-agent memory, complementing outcome-oriented social simulations such as GovSim.

“unit test”类比能很好地防御 synthetic 场景质疑：生态模拟复杂，但无法隔离错误；诊断 harness 简化，但能确定因果位置。

------

# 9. Mitigation 的最佳叙事

不要先介绍六个模块。先从 findings 推导三个 design principles：

### Principle 1：Separate observation from consolidation

单次事件可以被保留，但不能自动升级为长期机制。

### Principle 2：Separate causal scopes

关于自己、特定对象和世界的证据必须独立更新。

### Principle 3：Separate belief persistence from action urgency

证据不足以形成长期规则，不代表 Agent 必须忽略当前危险；可以采取最小、可逆、带 rollback 条件的即时行动。

然后再说 Evidence-Gated Memory 是这三条原则的一个实例。

最干净的主结果来自 [HELDOUT_RESULTS.md](/Users/tanghaohan/Desktop/ALL/thh/research/LASS-2026/HELDOUT_RESULTS.md)：

| Method                | Scope Accuracy ↑ | Leakage ↓  | Action Accuracy ↑ |
| --------------------- | ---------------- | ---------- | ----------------- |
| Reflection            | 72.9%            | 0.0979     | 72.9%             |
| Guarded Reflection    | 91.7%            | 0.0028     | 75.0%             |
| Structured Reflection | 91.7%            | 0.0398     | 87.5%             |
| Evidence-Gated Memory | **95.8%**        | **0.0028** | **95.8%**         |

这张表本身就是很好的机制梯度：

- caution 主要降低 leakage；
- structure 改善行动；
- evidence gating 同时改善 cognition 和 action。

外部控制器放在后面，作为：

> These principles can be executed outside the language model rather than merely described in a prompt.

不要把当前未完成的 long-context 结果放入主 claim。

------

# 10. Figure 1 应该怎么画

建议四栏：

```
A. Matched social events
   Same shortage, different source
   [World regime] vs [Bob emergency]

B. Reflective misconsolidation
   Both become:
   “The shared system is unreliable.”

C. ScopeProbe diagnosis
   Observation → Memory → Belief → Action
        ✓           ✗         ✗

D. Evidence-gated mitigation
   World change → world model
   Bob emergency → conditional episode
   Recovery → rollback
```

Figure 1 的核心 caption：

> Two trajectories produce similar adverse outcomes but warrant different persistent beliefs. Unconstrained reflection can preserve the event while erasing this causal distinction. ScopeProbe isolates the resulting memory, attribution, and behavioral errors; evidence-gated consolidation preserves the distinction.

------

# 11. 可直接采用的 Abstract

> Long-running social simulations require language-model agents to convert interaction histories into persistent beliefs about themselves, other participants, and the shared environment. We identify a counterintuitive failure in this process: agents can remember the correct event yet learn an unsupported lesson about whom or what the event reveals. We call this failure reflective misconsolidation and introduce ScopeProbe, an intervention-based diagnostic harness that constructs matched social trajectories differing in causal source or temporal validity while jointly auditing persistent memory, belief attribution, and action. Across controlled social-resource scenarios, we find that the failure is selective rather than a generic limitation of textual context: full-history agents largely preserve causal scope, whereas unconstrained reflection often converts conditional or recovered events into persistent cross-scope beliefs and associated action errors. This diagnosis motivates evidence-gated consolidation, which separates observations from persistent models, causal scope from event salience, and immediate precautions from long-term policy. On a frozen held-out suite, Evidence-Gated Memory improves both scope and action accuracy from 72.9% to 95.8% relative to unconstrained reflection under the same decision prompt. Our findings suggest that social-agent memory should be evaluated as an explicit belief-update process rather than treated as benign transcript compression.

如果补了多模型实验，可以把 `Across controlled social-resource scenarios` 改成更强的跨模型表述；目前不要暗示 universal prevalence。

------

# 12. 如何让薄实验真正经得起推敲

充分感不来自表格数量，而来自四种 triangulation：

1. **Breadth**：29 个 discovery 场景、8 个领域，说明现象不是一个捕鱼 prompt。
2. **Confirmation**：冻结的 8 个 held-out 场景，防止事后挑案例。
3. **Mechanism ladder**：Reflection → Guarded → Structured → Gated，说明不是单一 prompt 偶然。
4. **Multiple observables**：memory text、belief probe、action 三层证据。

但要真正稳住 reviewer，最高收益的补实验是：

- 用 2–3 个模型复现 6 个高信号案例和 2 个 negative controls；
- 对约 100 个 memory snapshot 做双人 blind annotation，报告 agreement；
- 用 scenario 而不是 checkpoint 作为独立单位，补 scenario-level bootstrap interval；
- 做 2–3 个 paraphrase 版本，排除特定措辞效应。

这四项比继续扩展 CPTG 数学术语或再跑大量不平衡长程调用更有价值。

------

# 13. 最后必须守住的 claim boundary

主文可以说：

> We establish the existence, structure, and behavioral relevance of reflective misconsolidation in controlled social-agent interactions.

不要说：

- 所有 LLM 都存在该现象；
- 所有 textual memory 都有害；
- Evidence-Gated Memory 已经优于 Full History；
- 已证明长期群体收益；
- 已经在原始 GovSim/Alympics 闭环环境验证；
- 六个模块都独立必要；
- CPTG 已获得长上下文优势。

最有顶会叙事感、同时最经得起推敲的最终 takeaway 是：

> **Social simulation should not only ask whether agents reach the right collective outcome. It should ask whether they learn the right social model—and whether they learned it for the right reason.**

这就是这篇 workshop paper 真正有分量的 insight。