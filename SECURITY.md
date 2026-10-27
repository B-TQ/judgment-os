# Security and privacy

## Supported version

Only the latest published 0.x release receives fixes. This is a pre-1.0 local research tool; its data formats may change between minor versions. Preserve original runs before upgrading.

## Reporting

Do not post credentials, private answers, personal data or exploitable details in a public issue. Use GitHub's private vulnerability reporting if the repository has enabled it. Otherwise contact the maintainer through a private profile contact option, or open a minimal issue requesting a reporting channel without sensitive details. No dedicated security team, response SLA or currently enabled private-reporting feature is implied.

## Boundaries

The tool does not enforce a model's instruction hierarchy. Read-only execution is not filesystem privacy isolation. Native staging and final-answer review do not prove that a Skill was followed or that every behavioral restriction held. Local manifests are integrity checks, not signed attestations; the operator and local files are trusted.

Default commands do not call models. Live adapter calls require explicit flags. Subscription-only mode verifies an existing ChatGPT login and removes API-key environment variables; do not enable live mode on untrusted work or in CI. Pattern redaction is incomplete, and you must inspect exports before sharing.

Skill installation is project-local and refuses existing installations, links/reparse paths and overwrite. Uninstall removes only a matching managed tree; it refuses changed or added files. It is not a sandbox against a malicious concurrent local user or an edited installation receipt. Stop editing the installed directory while uninstalling.

## 中文安全与隐私说明

仅最新公开的 0.x 版本接受修复，升级前保留原始实验。不要在公开 Issue 粘贴密钥、真实回答、个人信息或漏洞利用细节。私密报告使用仓库 Security 页实际可用的私密漏洞通道；如不可用，只开不含敏感细节的渠道请求。

离线默认命令不读取认证、不调用模型。真实适配器需显式参数和实际授权，只读执行不等于文件隐私隔离。模式脱敏有限，导出后需人工检查。Skill 安装拒绝覆盖，卸载遇到用户增改则停止；回执及本地文件受信任，不应与编辑并发执行，也不是针对恶意本地用户的沙盒。发现凭据泄露应先在服务商撤销，不能只删除代码中的字符串。

本次发布未加入遥测或静默跟踪。公共反馈请使用虚构输入和已脱敏错误信息。
