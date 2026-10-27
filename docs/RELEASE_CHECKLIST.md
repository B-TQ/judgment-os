# Suggested source-release checks

- Run unit tests, the Skill metadata audit, offline demo and `release.py --check` on the exact source being packaged.
- Confirm the original v0.2 baseline and its MIT license remain intact; review copyright/contributor attribution before publishing under a personal account.
- Keep README/status language experimental. Do not claim model gains, native E2E success, independent scoring or cross-host compatibility without corresponding real evidence.
- Build the source ZIP with `release.py --check --zip` to an external directory. Inspect its contents and checksum; do not publish a full workspace archive.
- Confirm no runs, private condition maps, reviewer receipts/ratings, raw answers/traces, `.env` files or local Git state are included.
- Review source and documentation for residual sensitive data. Pattern redaction is not an exhaustive secret detector.
- Verify the extracted package checksum and entry commands. Run the configured Windows/Linux and Python 3.11/3.14 CI matrix after creating the repository; configured CI is not executed CI.
- Keep research data publication separate. Use genuine consented outputs and authentic reviews, inspect redactions, and document missingness, failed gates, reviewer independence, model versions and activation evidence.

This checklist does not publish, push, create a remote repository or authorize distribution of private study data. The current delivery contains source and offline verification only.
