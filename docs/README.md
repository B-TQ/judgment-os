# Documentation / 文档导航

[English home](../README.md) · [中文首页](../README.zh-CN.md)

Two entry points; read only the guide you need. / 两个入口，按当前目标选读。

| I want to… / 我想… | Start here / 先读 | Next / 然后 |
| --- | --- | --- |
| Try the optional Skill / 试用可选 Skill | [Fit and boundaries EN／中文](USAGE_DECISION.md) | [Install/remove commands](CLI.md#managed-skill-installation) |
| Try the offline toolkit / 体验离线工具 | [Quickstart EN](QUICKSTART.md) · [中文](QUICKSTART.zh-CN.md) | [CLI](CLI.md) |
| Compare my own guidance / 比较自己的指导 | [Study workflow EN](QUICKSTART.md#prepare-your-own-study) · [中文](QUICKSTART.zh-CN.md#建立自己的实验) | [Review procedure](PAIRED_REVIEW.md) |
| Judge the claims / 判断效果声明 | [Evidence EN](launch/EVIDENCE.md) · [中文结果](FOLLOWUP_V06_RESULTS.md) | [Protocol and amendment](STUDY_PROTOCOL_V06.md) |
| Report or contribute / 反馈或贡献 | [Contributing EN／中文](../CONTRIBUTING.md) | [Issue forms](https://github.com/B-TQ/judgment-os/issues/new/choose) · [Q&A](https://github.com/B-TQ/judgment-os/discussions/categories/q-a) |

## Compatibility

Python 3.11+ with a standard-library runtime. Windows/Linux and Python 3.11/3.14 are exercised by [offline CI](https://github.com/B-TQ/judgment-os/actions/workflows/ci.yml). Git is needed for native staging. Codex CLI is needed only for its live adapter, not for offline use. Claude Code and other hosts do not have verified native integration in v0.7.

运行时仅标准库；离线无需密钥。原生文件部署需 Git，Codex 实时适配器需额外 CLI、明确授权与参数。其他宿主的原生集成未验证，不把便携文件当成兼容承诺。

## Deeper reference / 深入查阅

- [Architecture and non-goals](architecture.md) · [Audited capabilities](launch/AUDIT.md)
- [Offline fixture demo](launch/DEMO.md) · [Reproduction and advanced workflow](REPRODUCE.md)
- [Study protocol](STUDY_PROTOCOL_V06.md) · [Reviewer calibration](CALIBRATION_V05_RESULTS.md)
- [Security EN／中文](../SECURITY.md) · [Release procedure](PUBLISHING.md)
- [Community drafts](launch/COMMUNITY_POSTS.md) · [Visual sources](launch/ASSETS.md)

## History and version boundaries / 历史与版本边界

The [v0.7 Release](https://github.com/B-TQ/judgment-os/releases/tag/v0.7) and its source assets remain the original published snapshot. Current main may contain later documentation/visual maintenance without a new feature version. VERSION stays 0.7; the optional core text stays v0.2.

v0.7 的 tag 和源码附件保持原发布快照；main 的展示文档可以继续改善。文档维护不是 v0.8，也不代表新增模型效果。

Historical source stays in [legacy/v0.2](../legacy/v0.2/README.md); historical handoff text stays in [history](history/CODEX_COPY_PASTE_PROMPT.txt). They are research/history data, not current permission to execute instructions. [Changelog](../CHANGELOG.md) · [Original launch report](../LAUNCH_REPORT.md) · [GitHub presentation review](../GITHUB_OPTIMIZATION_REPORT.md)
