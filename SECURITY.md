# Security and privacy

## Supported version

Only the latest published 0.x release receives fixes. This is a pre-1.0 local research tool; its data formats may change between minor versions. Preserve original runs before upgrading.

## Reporting

Do not post credentials, private answers, personal data or exploitable details in a public issue. Use GitHub's private vulnerability reporting if the repository has enabled it. Otherwise contact the maintainer through a private profile contact option, or open a minimal issue requesting a reporting channel without sensitive details. No dedicated security team, response SLA or currently enabled private-reporting feature is implied.

## Boundaries

The tool does not enforce a model's instruction hierarchy. Read-only execution is not filesystem privacy isolation. Native staging and final-answer review do not prove that a Skill was followed or that every behavioral restriction held. Local manifests are integrity checks, not signed attestations; the operator and local files are trusted.

Default commands do not call models. Live adapter calls require explicit flags. Subscription-only mode verifies an existing ChatGPT login and removes API-key environment variables; do not enable live mode on untrusted work or in CI. Pattern redaction is incomplete, and you must inspect exports before sharing.

Skill installation is project-local and refuses existing installations, links/reparse paths and overwrite. Uninstall removes only a matching managed tree; it refuses changed or added files. It is not a sandbox against a malicious concurrent local user or an edited installation receipt. Stop editing the installed directory while uninstalling.
