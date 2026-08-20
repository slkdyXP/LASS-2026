# Multi-Agent Social Simulation Base

默认入口已从人口估计/广播实验切换到模块化投票社会模拟。旧的 `run_social.py`、`run_experiment.py`、`config.social*.json` 和旧结果保留为历史材料，但 `run.sh` 不会调用它们。

```bash
cd /Users/slkdy/Desktop/workshop/c2r_baseline
./run.sh --validate-only
./run.sh
```

`./run.sh` 只调用真实配置的 API；没有 `C2R_API_KEY` 会退出，绝不产生 mock 结果。

## 模块

- `social_base/data/personas.json`：20 个稳定 ID 的独特合成 Persona。
- `social_base/data/interaction_profiles.json`：20 个独立的互动倾向；例如建议型、易受说服型、反驳型、倾听型、调停型。它们不含候选人选择。
- `social_base/data/candidates.json`：6 名匿名、权衡均衡的虚构候选人。
- `social_base/tasks/voting.py`：可替换下游 task；负责输入/输出 schema 和 task prompt。
- `social_base/pairing.py`：固定种子的 circle-method 双人配对。
- `social_base/provider.py`：真实 OpenAI-compatible API 调用。
- `social_base/run.py`：私有记忆、轨迹、盲评调度、导出。
- `social_base/metrics.py`：Persona—选择一致性、稳定性、多样性、影响和网络指标。

## 运行产物

每次真实 run 写入 `voting_runs/<UTC timestamp>/`：冻结配置、Personas、候选人、配对、初始私有状态、完整 JSONL 轨迹、私有记忆、Judge 盲评、指标、审计和 HTML 报告。

Judge 调用仅接收单个 Persona 和候选人材料；其 prompt 不含 agent 的初始/最终选择、对话、轨迹或群体结果。Judge 输出单独存放在 `judge_blind.json`，再由 `metrics.py` 比对。

## 验证

```bash
python3 -m unittest discover -s social_base/tests -v
./run.sh --validate-only
```

`--validate-only` 不调用 API，验证配置、20 agent、6 名候选人、6 轮完美匹配和 Judge 隔离声明。完整真实 run 约有 280 次模型调用（20 初始 + 6×10×4 交流/私有更新 + 20 Judge），不会自动启动。

对多个完成的 20-agent、6-round run，可用 `python3 -m social_base.aggregate voting_runs/<run1> voting_runs/<run2> --output aggregate.json` 汇总跨 seed 均值、标准差和近似 95% CI；smoke run 会被自动排除。
