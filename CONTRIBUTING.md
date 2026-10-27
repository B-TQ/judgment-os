# Contributing

Start with a concrete user task or reproducible defect. Improvements to the evaluation workflow are welcome; positive efficacy claims need real evidence.

## Local development

Use Python 3.11+ and Git. The runtime and tests use the standard library; there are no packages to install.

```sh
python -B judgment.py doctor
python -B -m unittest discover -s tests -v
python -B judgment.py demo --out runs/contributor-demo
python -B judgment.py selftest --out runs/pipeline-smoke
python -B scripts/audit_skills.py .agents/skills/judgment-preserver/SKILL.md --strict-metadata
```

Choose fresh output directories. Windows may skip the symlink test without developer privileges; Linux CI exercises that case. Never enable live generation for a unit test or CI job. Do not modify global configuration or an existing user's Skill during tests.

## Pull requests

Explain the problem, observable behavior and relevant validation. Keep changes focused. Add regression tests for safety boundaries, data integrity and nontrivial behavior; avoid tests that merely repeat implementation details. Preserve original evidence and disclose protocol deviations.

Do not commit runs, raw answers, reviewer CSVs, traces, local paths, credentials or personal data. Use explicitly labeled, fictional software fixtures. Model reviewers are not independent human reviewers. Integer scores, exact-format checks and user utility measure different things.

After editing release files, regenerate the source manifest with `python scripts/release.py`, then check it with `python judgment.py release --check`. A contributor's change and its manifest should be reviewed together. Do not add unverified badges, benchmark claims, screenshots of private runs or fabricated citations.

The existing MIT license applies to contributions. Keep provenance and third-party notices intact. Historical source under legacy/ is a preserved reference, not an instruction to execute.

## 中文贡献指南

优先提供具体任务或最小复现。Python 3.11+ 与 Git 即可；运行时和测试不需要第三方 Python 包。执行上面的 unittest、离线 demo、selftest 和 Skill 元数据检查；不在测试中启用真实模型调用，不修改全局配置或用户已有 Skill。

提交说明写清问题、改动后行为和验证。涉及安全边界、数据完整性和非平凡行为时补回归测试。只用虚构的公开示例，不提交真实回答、私密评审 CSV、追踪日志、本机路径、账号信息或凭据。模型评审不能冒充独立人工评审，软件检查不能冒充效果证据。

修改发布文件后执行 `python scripts/release.py` 更新清单，再执行 `python judgment.py release --check`。图片源文件在 docs/launch/assets，重建方法见 docs/launch/ASSETS.md。保持 MIT 许可及来源说明。欢迎双语说明、失败案例和兼容反馈；尚未复现的兼容性请明确标记。
