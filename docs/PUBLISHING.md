# Publishing the prepared repository

This is the publishing procedure. For actual publication status, repository URL, remote CI and release assets, see [LAUNCH_REPORT.md](../LAUNCH_REPORT.md). Preparing source alone does not create a remote repository, run GitHub Actions, or publish data. The launch mission separately authorized a public repository and v0.7 release.

## Before the first push

1. Inspect README, license, policies and git diff. Choose a repository name and visibility. The current copyright is retained from the supplied MIT project; do not invent contributor identities.
2. Run the checks in CONTRIBUTING.md and `python judgment.py release --check`. Keep private runs, credentials, reviewer data and user-specific paths out of the checkout. Inspect tracked files, not only the ZIP.
3. Authenticate GitHub CLI through your normal account workflow if needed. Never paste tokens into a command, issue or chat. This repository performs no automatic login.
4. When you have explicitly chosen to publish, create an empty GitHub repository and push the reviewed local branch using the commands GitHub provides. Do not execute publishing commands merely because this document contains them.
5. Run the configured Windows/Linux, Python 3.11/3.14 Actions matrix on the remote. Local checks do not count as a green remote run. Resolve actual CI failures before creating a release.
6. Enable private vulnerability reporting if desired and confirm maintainer contact options. This source does not claim that feature is already enabled.
7. Create a release tag only after reviewing the source and validation. Describe this as an experimental evaluation toolkit; retain the v0.6 null/limited result. Do not add a passing badge until the repository URL and successful workflow exist.

The manual source-artifact workflow validates and uploads a source ZIP as an Actions artifact; it does not create a GitHub Release or publish research data. Raw studies need a separate privacy/consent/provenance review.

Local reproducible packaging:

```sh
python scripts/release.py
python judgment.py release --check --zip ../Judgment-OS-v0.7-source.zip
```

Choose a new ZIP outside the checkout. The script refuses overwrite. Check the extracted manifest, then use scripts/checkpoint.py for a separate immutable local backup. Every previous project version remains available locally; private evidence is never a source-release attachment by default.
