# Judgment OS v0.2：给 Codex 的完整交接包

> **这份 ZIP 是完整项目，而不是只有提示词。** 请在解压后的仓库根目录打开 Codex。

## 项目要解决什么问题

领域 Skill 可以带来专业能力，但也可能将示例风格、惯常做法、推荐流程过度泛化，压缩 AI 的自由判断空间。Judgment OS 尝试在 **不违反上位指令、必要流程、安全要求和用户明确约束** 的前提下，保留合理的自主判断与创造性。

目前 **v0.2 只是实验性 Meta-Skill + 离线评估工具**，不是具备特殊权限的调度引擎，也尚未证明提升性能。**不要在 GitHub README 中宣称效果已验证。**

## 推荐给 Codex 的完整任务

请阅读本目录的 `README.md`、`README.zh-CN.md`、`docs/architecture.md`、`evals/PROTOCOL.md`、`docs/CODEX_HANDOFF.md`、`.agents/skills/judgment-preserver/SKILL.md`、`scripts/`、`tests/`，在保留全部 v0.2 内容的基础上，按 `docs/CODEX_HANDOFF.md` 开发 **v0.3 可复现实证原型**。不要重新从零生成仓库。

**优先实现**：

1. **真实 Codex 调用适配层**：先核对本机 Codex CLI/SDK 能力及官方文档；支持缺少 CLI 时的显式 dry-run，不伪造集成成功。
2. **硬约束确定性校验**：对合适任务加入 JSON、CSV、固定前缀、严格顺序等验证器；不要声称可自动判断所有安全或审美要求。
3. **可复现的盲评框架**：安全处理日志、模型版本、失败/缺失输出、独立评价者及评分汇总，防止 treatment 标签或敏感数据泄漏。
4. **可信的比较基线**：除无 Skill / 领域 Skill / 领域 Skill + Judgment OS 之外，再加一个极简的 task-fit 提示词基线，防止误把通用提醒带来的提升归功于复杂架构。
5. **测试 + 文档 + CI**：在无 API Key 条件下完整跑离线测试；若无模型调用权限，则停在能验证的范围，记录真实阻塞。

**不可越过的边界**：
- 不覆盖系统、开发者、用户要求、工具契约或真正具有强制性的领域规则。
- 不以词语匹配取代规则来源识别；静态 Skill 审查结果只是人工复核线索。
- 不制造假的 A/B 测试样本、人工评分、模型性能指标或星标数据。
- 不要求模型输出私有推理链或每次都生成多个候选方案。
- 不默默调用付费 API，不提交密钥，不擅自推送公开 GitHub 仓库。

**最终交付**：更新后的代码、通过的测试、README 中英文、变更日志、一份可重复运行的演示命令，以及一份明确标注「已完成 / 未完成 / 尚未验证」的报告。**不需要先征求我关于实现细节的逐项意见；可以按上述边界自主推进。**

完整的英文工程规范与验收条件：[`docs/CODEX_HANDOFF.md`](docs/CODEX_HANDOFF.md)。

## 当前文件说明

| 路径 | 作用 |
|---|---|
| `.agents/skills/judgment-preserver/SKILL.md` | 真正使用的 v0.2 Meta-Skill |
| `.agents/skills/judgment-preserver/references/` | 判断边界说明 |
| `global/AGENTS.md.snippet` | 可选的全局指导语 |
| `scripts/audit_skills.py` | 静态审查候选提示（不具有权限判定力） |
| `scripts/benchmark.py` | 可重复生成匿名化实验样本与评分模板 |
| `scripts/make_cases.py` | 测试用例维护脚本 |
| `evals/cases.json`, `evals/PROTOCOL.md` | 16 个场景和实验协议 |
| `tests/`, `.github/workflows/ci.yml` | 软件测试和 CI |
| `docs/architecture.md`, `docs/ROADMAP.md` | 原理、局限与路线图 |
| `docs/CODEX_HANDOFF.md` | Codex v0.3 详细任务书 |
| `distribution/judgment-preserver-v0.2-SKILL.md` | 与正式安装版字节一致的单独拷贝，方便人工使用；**编辑时以 `.agents/` 中的原文件为准，并同步这里的副本** |
| `README.md`, `README.zh-CN.md`, `CHANGELOG.md`, `LICENSE` | 发布与使用说明 |

## 环境验证（原始 v0.2）

要求：Python 3.11+，无第三方依赖。

```bash
python -m unittest discover -s tests -v
python scripts/audit_skills.py .agents/skills/judgment-preserver/SKILL.md --strict-metadata
python scripts/benchmark.py prepare --out runs/pilot --seed 42 --repeats 1
```

在本次打包验证中：7 项单元测试通过；Skill 元数据校验通过；能为 16 个场景生成 48 个 A/B/C 实验槽位。**这不是模型效果评测结果。**
