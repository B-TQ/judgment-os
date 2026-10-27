# Judgment OS v0.2 — 中文快速上手

**目标：让 Skill 提供专业知识，而不是用默认模板取代 AI 的独立判断。**

这不是一个“强制创新”的 Skill，更不是能突破规则的工具。它的原则是：**必须遵守的要求照常遵守；只有明确允许选择时，才根据真实任务灵活选方案。**

## 这次真正升级了什么？

1. **元 Skill 核心：** 强化指令来源意识、最小干预、避免机械调用；不会因“创新”放弃强制检查。
2. **审查器：** 检查 `SKILL.md` 结构并标出可能过度僵化的表述，仅供人工检查，绝不自动判断何者可以忽略。
3. **A/B/C 实验：** 16 个测试（8 个开放任务 + 8 个严格/无需干预的对照），可固定随机种子准备提示词。
4. **盲评与统计：** 隐藏分组标记、导出评审材料、记录人工评分；必须通过硬性约束后才统计质量得分。没有真实结果时不会伪造提升。
5. **工程化：** Python 标准库脚本、单元测试、GitHub Actions、许可证、架构文档与下一阶段 Codex 任务书。

## 用于 Codex

把 `.agents/skills/judgment-preserver/` 整个目录复制进你项目的同一路径（也可复制到 `~/.agents/skills/judgment-preserver/`）。在 Codex 中任务涉及多个 Skill 冲突、可选模板锁死风格等问题时，显式提到 `$judgment-preserver`。如果目录没有被发现，重新启动 Codex 并核实 Skills 列表。

若希望试验广泛持续的策略，可以**另行**把 `global/AGENTS.md.snippet` 放进你的项目 `AGENTS.md`。不要不加比较地同时启用两种版本，避免混淆干预效果。

## 本地验证与实验（Python 3.11+）

```bash
python -m unittest discover -s tests -v
python scripts/audit_skills.py .agents/skills/judgment-preserver/SKILL.md --strict-metadata
python scripts/benchmark.py prepare --out runs/pilot --seed 42 --repeats 1
```

把 `runs/pilot/prompts/` 中每个文件依次提交给**同一模型且保持参数相同**，回答逐一粘进 `runs/pilot/outputs/` 中对应文件。随后：

```bash
python scripts/benchmark.py packets --out runs/pilot
# 只把 review_packets/ 与 ratings.csv 交给人工盲评者，评分填到 ratings.csv
python scripts/benchmark.py report --out runs/pilot
```

没有填入评分时，脚本会报错并停止，不会生成虚假的研究结论。具体打分规则参阅 `evals/PROTOCOL.md`。**提示词模拟 ≠ Codex 原生 Skill 调用测试**，所以即便有结果也必须注明实验条件。

## 下一步交给 Codex 做什么？

`docs/CODEX_HANDOFF.md` 包含可直接复制的 v0.3 工程任务书：真实 Codex Skills 触发、自动检查严格输出格式、保密的评审数据、可靠的统计与文档。你可以先在本地检验 v0.2，再选择是否继续。

**状态：实验原型，尚未证明性能提升，更未证明“通用解决”。**
