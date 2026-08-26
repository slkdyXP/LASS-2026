# 多方向现象勘探与确认计划

## 目标

当前目标不是证明预设 idea 正确，而是系统寻找：统一文本记忆是否在社会模拟中产生 `cross-scope interference`，它在哪些条件下出现、在哪些条件下不出现、是否影响行动。

因此采用两阶段设计：

1. **Discovery**：广领域、广错误类型、低重复，寻找稳定候选模式和反例。
2. **Confirmation**：冻结 prompt、标签和阈值，对预先声明的分层样本重复；不能只复现支持假设的 case。

## 实验维度

### 变化来源

- `world`：资源再生率、公共品乘数、病毒传播率、太阳能供给、道路容量、任务复杂度、港口物流。
- `specific other`：过度捕捞、free-riding、违反防疫规则、过度耗电、降低团队努力、阻塞道路、供应商扣货。
- `self`：自身需水、健康、工具或能力状态变化。
- `persona boundary`：策略失败是否错误升级为稳定价值和身份改变。

### 时间结构

- 单次异常；
- 持续 regime change；
- 异常后恢复；
- 某人在特定健康或资源状态下的条件性行为；
- 多轮背叛后的针对性策略变化。

### 记忆挑战

- 低历史压力；
- sliding-window 遗忘；
- retrieval 取错人物或旧事件；
- 长历史中的已解决争议干扰当前归因；
- summary/reflection 的错误巩固；
- 人名高频造成 entity-binding 错误；
- 一个 newcomer 的行为被泛化到整个群体。

### 社会领域

捕鱼、竞价、公共品、防疫协调、共享微电网、团队协作、交通协调、供应链。

## 当前矩阵

- 29 个场景；
- 8 个领域；
- 6 个普通 Agent baselines；
- 约 57 个关键 checkpoint；
- matched pairs 尽量保持宏观坏结果相近，只改变因果来源；
- `core / breadth / inferential / stress` 四个 suite，可按领域和实验轴分批运行。

## Baselines

- `direct`：persona + 当前观测；
- `recent_window`：最近三轮；
- `retrieval`：透明的 lexical history cache；
- `full_history`：完整历史；
- `summary`：统一非结构化摘要；
- `reflection`：统一非结构化反思。

## 多角度测量

### 行为输出

实际 harvest、bid、contribution、precaution、consumption、work hours、departure delay 或 order quantity，以及公开消息。

### 当前信念 probe

关键轮次读取 Agent 当时真正可访问的记忆，测量：

- primary scope；
- self/other/world/persona/episodic 更新强度；
- 具体 target agent；
- 是否泛化到群体；
- 是否认为变化暂时；
- 是否声称 persona 已改变。

probe 不写回后续上下文。

### 原始记忆文本审查

保存每一轮 transcript、retrieved entries、summary、reflection。可选 evaluator 在知道实验真值的条件下，对以下错误评分：

- wrong-scope claim；
- unsupported blame；
- world overgeneralization；
- group overgeneralization；
- persona drift；
- behavioral consequence。

模型 evaluator 只是第二测量渠道，最终关键样本仍需人工读原文。

### 分层统计

同时按 baseline、场景、领域、实验轴、证据难度、时间形态、历史压力和 matched group 聚合。不能只报告总体平均数。

## 执行策略

### API smoke test

先选一个非捕鱼 matched pair，运行 `full_history + summary` 各一次，检查 JSON、摘要杜撰、probe 诱导和动作范围。

### Breadth discovery

按两类领域一批运行 1 repeat，覆盖全部六个 baselines。每批结束立即审计所有错误记录和部分正确记录。

### Stress discovery

单独运行长历史、entity binding、group generalization、transient recovery 和 persona boundary 场景。

### Confirmation

冻结后至少 3 repeats。若调用预算不够，使用预先声明的分层抽样：每个领域至少保留一组 world/other pair，并保留所有不同时间结构；不能按首轮结果挑 case。

## 支持、限制或否决 idea 的标准

### Discovery-stage label correction log

- Conditional-other recovery initially used `expected_scope=none`. This was corrected before core/stress execution: recovery should retain a scoped conditional model of Bob while lowering current threat, rather than erase relationship knowledge. The correction follows the original hypothesis and is not based on choosing the better-performing label.

### 支持

- 多个领域出现方向一致的 wrong-scope update；
- 错误集中于某些记忆机制或历史压力条件；
- 原始记忆文本、probe 和行动至少两个渠道相互支持；
- transient recovery、entity binding 或 group generalization 中存在可重复的持久错误。

### 限制

- 只在 summary/reflection 出现：论文应聚焦 consolidation，而不是所有文本记忆；
- 只在长历史/retrieval 出现：论文应聚焦 interference 或 retrieval；
- 只在模糊证据出现：贡献应改成 uncertainty-aware attribution；
- belief 错但行动正常：不能宣称群体后果，只能报告认知诊断。

### 否决

- 各 baseline 在多个领域都能稳定区分作用域；
- 错误仅来自 probe 或 evaluator，不存在于原始 memory/action；
- 换领域或换措辞后现象消失；
- 错误率不高于 direct/no-memory control，或无系统模式。
