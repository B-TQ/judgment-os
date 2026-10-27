# Judgment OS v0.7 launch report / 发布报告

Date / 日期: 2026-10-27 (Asia/Shanghai).

- Repository / 仓库: https://github.com/B-TQ/judgment-os
- Release / 版本: https://github.com/B-TQ/judgment-os/releases/tag/v0.7
- Verified engineering run / 已验证工程 CI: https://github.com/B-TQ/judgment-os/actions/runs/40517468018
- Latest/tag checks / 最新与标签检查: https://github.com/B-TQ/judgment-os/actions/workflows/ci.yml

## Delivered / 交付内容

English/Chinese README, Chinese quickstart, bilingual contribution/security guidance, implementation audit, evidence summary, six original PNGs and editable SVG/HTML, reproducible fixture demo, architecture diagram, dual-language release notes, X/HN/Reddit and four Chinese-community drafts, feedback form and a day 1/3/7/14/30 plan. [Launch kit](docs/launch/README.md).

Windows: install Python 3.11+, then double-click TRY_DEMO.cmd. Cross-platform: `python scripts/try_demo.py`. Both run the same three offline commands with a fresh output directory. No account, pip install or API key is needed.

原 v0.7 未覆盖；发布副本保留四条原 Git 历史及 MIT 许可。可选 Skill 正文与原基线逐字节一致，历史案例与研究结论未改。只为发布材料扩展了限定目录内的源码打包白名单，新增防止其他目录私密图片误打包的回归测试，并补便捷离线入口。

## Verification / 实际验证

- Local Windows/Python 3.14, including a clean Git clone: **69 tests, 68 passed, one skipped** for unavailable Windows symlink privilege. The skip remains disclosed.
- The linked remote engineering workflow completed with **success** for Windows/Linux × Python 3.11/3.14. Each job ran 69 tests, plus doctor, strict Skill metadata audit, 8-slot tutorial, 64-slot-per-mode smoke, release manifest and clean-tree checks. Final documentation/manifest changes are required to pass the same workflow before the tag is published; the Release records that final run.
- Public HTTPS clone tested: doctor, tutorial, correct-answer check and manifest check succeeded. The intentional incorrect fixture exits 1; the correct fixture exits 0.
- Source ZIP extraction and all source-manifest hashes verified. All active checked Markdown relative links resolve. Six PNGs were visually inspected; social covers are exactly 1280×640 and contain no text/EXIF metadata.
- **Zero new model calls**, generated answers or ratings for launch. Software verification is not efficacy evidence.

本地与干净克隆均为 69 项，68 通过、1 项权限跳过。远端四组合工程工作流已成功，每组运行 69 项及离线完整流程。最终文档与清单提交也需经同样 CI 通过才发布 tag，最终运行链接写入 Release。公开克隆、解压哈希、正误示例、相对链接和六张图均已检查。本次没有新增模型效果调用。

## Privacy and authorization / 隐私与授权

Current source and reachable Git-history blobs/metadata were inspected using a local heuristic scan plus manual review. The only baseline personal-path finding was a fictional `someone` redaction-test fixture, manually confirmed and excluded as an example. No actual credential or personal path was accepted for publication. Detection is not exhaustive; it is not a security certification.

Initial pushes using the existing OAuth login and supplied chat token were rejected for missing workflow permission. The chat token was used only in child-process memory for one authorized retry; it was not saved in source, requirements, Git config or artifacts. The owner then explicitly authorized GitHub CLI permission refresh and completed GitHub's device flow. The refreshed OS-keyring CLI login supplied workflow scope and pushed successfully. **Revoke the token pasted in chat.** This report does not claim it has been revoked.

Only allowlisted source and original artwork are published. Raw studies, genuine private answers, reviewer maps/receipts, account traces, requirement archives and local operator scripts stay outside the public repository. No history rewrite, force push, private-study upload, telemetry or social-media posting is part of this launch.

源码及完整可达历史已做启发式扫描和人工检查。初次两种认证缺 workflow 权限，随后用户明确授权补授并完成 GitHub 浏览器流程，CLI 推送成功。聊天令牌仅在内存重试，未写入项目和附件；请撤销。公开范围只含白名单源码与原创图，私密研究、真实回答、映射、账号日志及需求档案均不公开。未改写历史、未加遥测、未代发社区内容。

## Repository setup / 仓库配置

Public repository, main branch, bilingual description, eight relevant topics, Discussions and private vulnerability reporting are configured and verified. No invented homepage. Pinned Actions retain read-only workflow permissions. The optional artwork renderer uses existing Node/Playwright/browser tooling; those packages are not runtime dependencies or bundled assets.

## Manual actions / 需手动完成

1. Revoke the credential pasted in chat / 撤销聊天中提供的令牌。
2. Upload [social-preview.png](docs/launch/assets/social-preview.png) at Settings → General → Social preview. The browser settings tab opened, but automation could not attach; the image has **not** been set as the repository Social Preview. 中文封面也已提供，浏览器自动上传未完成。
3. Choose and publish community drafts after checking each community's current rules. Nothing was posted on your behalf. Follow the first-month plan manually; no recurring automation was created. / 自行选渠道发文并手动执行首月计划。

## Unverified or planned / 尚未验证与规划

The eight-case C–D result remains **1 win / 7 ties**, with the sole win caused by D exceeding a word budget by one word. Both initial review-context leakage and the corrective phase remain disclosed. No general superiority, independent human utility, Claude Code native integration or cross-model replication is claimed. Complete historical model judgments cannot be independently recomputed without private artifacts. [Evidence](docs/launch/EVIDENCE.md) · [Risk and validation boundaries](docs/launch/VALIDATION.md).

原八题有限结果、评审偏差和采用门槛均保留。独立人工效用、其他宿主原生适配和跨模型研究是后续工作，不是已交付功能。完整核心继续可选。
