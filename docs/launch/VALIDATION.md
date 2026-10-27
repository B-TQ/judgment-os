# Validation and release risk / 验证与风险

Date: 2026-10-27. Final remote links and results are recorded in [LAUNCH_REPORT.md](../../LAUNCH_REPORT.md).

## Source and privacy / 源码与隐私

Reviewed current code, Skill and reference, public fixtures, test contracts, docs, workflow permissions, dependencies, license and all four baseline commits. A local heuristic scan inspected working text and reachable historical blobs/commit metadata for credential patterns, personal paths and private email patterns; matched values are not printed. One baseline hit was a deliberately fictional `someone` path in a redaction unit test, manually reviewed and excluded as a false positive. No actual credential or personal-path hit was accepted for publication.

检查源码、Skill、公开示例、测试、文档、工作流权限、依赖、许可及四条历史提交。启发式扫描覆盖当前文本和可达历史 blob/提交元数据。测试里虚构的 someone 路径为已人工确认的误报；未把真实凭据或个人路径带入公开内容。扫描不能证明穷尽所有敏感信息，仍需人工检查。

The supplied chat credential was used only in child-process memory for an authorized retry after the existing OS-keyring login failed to upload workflows. Both attempts were rejected for missing workflow permission. It was not copied into source, archived in requirements, saved in Git authentication, or included in artifacts. The chat credential should be revoked by its owner; this launch does not assert revocation.

现有登录缺少 workflow 权限，随后仅在子进程内存中使用用户提供的凭据做授权重试，仍被 GitHub 以相同原因拒绝。凭据未存源码、需求文档、Git 配置或附件。聊天凭据应由用户撤销，本报告不声称已撤销。

Publish only allowlisted source and original project-owned artwork. Do not upload studies, raw answers, private reviewer maps, account traces, source-history bundles containing private backups, launch operator scripts or requirement archives. Git authors use nonpersonal invalid-domain addresses. Remote URLs carry no embedded credentials. No source history is rewritten.

## Checks / 检查

- Full unittest suite on the final launch tree; disclose the Windows symlink-privilege skip. Linux CI covers the symlink path.
- Strict metadata audit, local doctor, 8-slot tutorial, intentional pass/fail fixtures, larger 64-slot-per-mode smoke, zero new model calls.
- README and new launch-document relative links; all top-level CLI help routes. Existing historical source is preserved rather than retroactively rewritten.
- Release manifest regenerated; source ZIP extracted and hashes checked; PNG dimensions and visual rendering reviewed.
- Fresh local Git clone and clean archive smoke. Final Windows/Linux Python3.11/3.14 matrix observed remotely before Release publication.

## Material limitations / 重要边界

Software tests are not efficacy evidence. No new model experiment, human utility study, Claude Code adapter or cross-model replication was performed. Historical model judgments cannot be completely recomputed without private artifacts. Pattern redaction and this launch scan are incomplete. Managed installation trusts local receipts and is not protection against concurrent malicious local edits. No signed source attestation or signed tag is claimed.

软件测试不证明效果；历史研究私密原件不公开；脱敏和扫描不保证完整；安装回执不是签名；未声明签名 tag 或供应链证明。视觉示例明确标注为软件 fixture，不冒充前后效果。

## License / 许可

Retain the supplied MIT license and contributor copyright. Runtime/tests use standard library only; optional Git/Codex executables and Node/Playwright/browser artwork tooling have their own licenses and are not bundled. Related-work links are citations, not imported source or endorsements. Artwork uses original vector shapes and locally rendered system-font glyphs; no third-party logo, photograph or remote font is embedded.
