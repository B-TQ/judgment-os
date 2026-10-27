# v0.7 implementation audit / 功能审查

Date / 日期: 2026-10-27. Audited baseline: `daa114a4d0918533c04d1f3493e7b9a699275f49`. Launch edits preserve the original four commits and optional Skill bytes.

| State / 状态 | Capability / 能力 | Code and evidence / 实现与依据 |
| --- | --- | --- |
| Implemented, software-tested / 已实现且有软件测试 | Unified CLI, doctor, 8-slot tutorial, answer checking / 统一命令与离线入口 | judgment.py; tests/test_public_cli.py |
| Implemented, software-tested | JSON/CSV/text/headings/lines/word checks / 声明文本属性检查 | scripts/validators.py; tests/test_validators.py |
| Implemented, software-tested | Seeded four-arm preparation, equal hard gates, hashes / 四组冻结与哈希 | scripts/benchmark.py; tests/test_benchmark.py |
| Implemented, software-tested | Dry-run/live gates, failures/timeouts, external collection / 收集与失败状态 | scripts/codex_adapter.py; tests/test_adapter.py; live subprocesses are mocked in tests |
| Implemented, software-tested | Re-keyed packets, immutable imports, paired review and phase selection / 评审与轮次 | scripts/review.py, paired_review.py, reporting.py; review tests |
| Implemented, software-tested | Managed install/removal, no overwrite, modified-tree refusal / 安装保护 | scripts/skill_install.py; public CLI tests |
| Implemented, software-tested | Metadata cues, calibration fixtures, body probe, checkpoint / 元数据、校准、探针、检查点 | audit_skills.py, calibration.py, integration_probe.py, checkpoint.py; matching tests |
| Implemented, software-tested | Source allowlist, checksums, stable ZIP / 发布打包 | scripts/release.py; tests/test_tools.py |
| Implemented, not general efficacy / 已实现但未证明通用有效 | Optional Judgment Preserver and project snippet / 可选元 Skill 与项目片段 | .agents/skills/judgment-preserver/SKILL.md; global/AGENTS.md.snippet; v0.6 limited result |
| Recorded experiment, limited verification / 既有实验但验证有限 | Prior native Codex generation and model-only reviews / 原生生成与模型评审 | protocols and result summaries; raw private artifacts excluded; not independently recomputable from public source |
| Experimental / 实验性 | Interpretation of optional defaults, provenance and bounded choice / 可选默认及选择空间 | Natural-language guidance; not machine-enforced policy |
| Planned, not implemented / 规划未实现 | Signed provenance, automatic conflict resolver, host orchestrator / 签名来源、自动冲突裁决、宿主协调器 | Explicit non-goals in docs/architecture.md |
| Not verified / 未验证 | Claude Code native install/activation; general creativity lift; independent human utility / 其他宿主与通用效果 | No such claim or integration in this release |

## Structure and constraints / 目录与边界

`judgment.py` routes to standard-library scripts. `.agents/` holds the actual Skill and its reference; `distribution/` mirrors it portably. `evals/` contains authored task fixtures and protocols. `tests/` exercises tool contracts. `legacy/v0.2/` preserves earlier source; `docs/history/` contains historical handoff data, not active authorization.

没有自动将 must/should 归类成指令权限的模块。audit_skills.py 只标记供人工检查的用词线索，不能授予偏离指令的权限。提示词里的来源意识与机器强制执行必须区分。

Runtime and test dependencies are Python standard library only, plus Git for native staging. Codex CLI is needed only for its adapter. Optional artwork regeneration uses Node/Playwright and a browser, not the runtime. Existing MIT contributor copyright is retained; no copied third-party implementation or unlicensed image is added.

已有测试、离线教程、大型 smoke、元数据和发布清单在本次发布中重新运行。实际远端 CI 与发布地址统一记入 [最终报告](../../LAUNCH_REPORT.md)。不把测试数当成模型评测样本量。
