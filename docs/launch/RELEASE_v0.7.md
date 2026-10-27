# Judgment OS v0.7 — test what your agent's Skills change

[English](#english) · [中文](#中文)

## English

An offline-first evaluation toolkit with an optional experimental Judgment Preserver Skill. The core Skill text remains v0.2; v0.7 versions the toolkit.

### Available now

- Unified CLI: local doctor, eight-slot offline tutorial, one-answer deterministic checking, study preparation/collection, explicit review phases and reports.
- Project-local managed Skill install/uninstall with dry-run, overwrite refusal and preservation of changed or extended trees.
- English/Chinese README, quickstart, contribution/security guidance, reproducible demo, architecture and social images, and manual community launch drafts.
- Source allowlist/checksums, deterministic ZIP packaging, pinned Actions and Windows/Linux Python 3.11/3.14 offline checks.

Download the attached `Judgment-OS-v0.7-source.zip`, extract, and run:

```sh
python judgment.py doctor
python judgment.py demo --out runs/first-demo
python judgment.py check --case Q01 --answer examples/quickstart/correct.json
```

Python 3.11+, no pip or API key for offline use. Repeated demos need fresh directories. The optional Skill and live adapter are separate from this offline path.

Windows shortcut: double-click `TRY_DEMO.cmd` after installing Python. On any supported OS, run `python scripts/try_demo.py` for the same three offline commands with a fresh output directory.

### Tests, evidence and limitations

Local Windows Python 3.14: 69 tests, 68 passed and one symlink-privilege skip. See [LAUNCH_REPORT.md](https://github.com/B-TQ/judgment-os/blob/main/LAUNCH_REPORT.md) for actual remote matrix results and final release verification. The tutorial and larger smoke make zero model calls.

No new model efficacy experiment was run. The recorded eight-case follow-up remains C–D **1 win / 7 ties**, with the sole win due to D exceeding a word limit by one word. Both initial review leakage and the corrective review phase are disclosed. The adoption threshold was not met; the full Skill stays optional. Raw private studies are not release assets; complete historical model judgments cannot be recomputed from public source alone. Claude Code native compatibility, human utility and general efficacy remain unverified.

Next: independent human utility review, held-out/cross-model studies, and installation feedback. These are plans, not shipped results. Community posts remain drafts.

## 中文

这是离线优先的轻量评测工具，附带可选实验性 Judgment Preserver。核心正文仍为 v0.2，v0.7 是工具包版本。

新增统一命令入口、8 槽位离线教程、单份答案检查、显式选择评审轮次，以及支持预览、拒绝覆盖、保留用户修改的项目内 Skill 安装与卸载。本次补齐中英首页、上手与贡献安全说明、真实软件演示、架构及传播图片、手动发布文案。

下载附件源码 ZIP 并解压，运行上面的三个命令。要求 Python 3.11+；离线不需要安装包、配置密钥或调用模型。重复演示换新目录。

Windows 装好 Python 后也可以双击 `TRY_DEMO.cmd`；跨平台便捷命令为 `python scripts/try_demo.py`，自动执行三个离线步骤并换新目录。

本地 Windows Python 3.14 共 69 项测试，68 通过、1 项因符号链接权限跳过；远端矩阵以最终报告为准。教程和大型 smoke 均为零模型调用。本次没有新增模型效果实验。八题实验完整核心对一句提醒仍为 **1 胜 7 平**，唯一胜出是对方字数超限一词。初始评审摘要泄漏与修正评审均已披露，未达到默认采用门槛，完整核心继续可选。私密研究原始材料不作为附件公开，不能仅凭源码重算历史全部模型评分。Claude Code 原生兼容、独立人工效用和通用提升尚未验证。

下一步是独立人工评审、留出与跨模型研究、安装反馈；均未在本次完成。各社区文案只是草稿，未代发。
