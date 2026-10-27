# Command reference

Run from a source checkout with Python 3.11+. The entry point also works from another current directory when invoked by its absolute path. Runtime and tests have no third-party Python dependencies. Advanced scripts remain available for compatibility.

| Command | Purpose | Model calls by default |
| --- | --- | --- |
| `python judgment.py doctor` | Offline prerequisites; no credential/account reads | 0 |
| `python judgment.py demo --out NEW_DIR` | Eight empty slots plus labeled fixture checks | 0 |
| `python judgment.py check --case ID --answer FILE [--cases FILE]` | Declared deterministic properties for one answer | 0 |
| `python judgment.py prepare --out NEW_STUDY ...` | Freeze cases, conditions and prompt hashes | 0 |
| `python judgment.py run --out STUDY ...` | Adapter plan; live mode requires explicit extra flags | 0 |
| `python judgment.py collect --help` | Collect genuine external output with provenance | 0 |
| `python judgment.py validate --out STUDY` | Check actual output integrity/properties | 0 |
| `python judgment.py review export/import --help` | Blind packet export and immutable model review import | 0 |
| `python judgment.py report --out STUDY --reviewer ID ...` | Selected-phase model review report | 0 |
| `python judgment.py selftest --out NEW_DIR` | Larger zero-answer pipeline smoke test | 0 |
| `python judgment.py release --check` | Verify source manifest | 0 |
| `python judgment.py skill install/uninstall --project PROJECT [--dry-run]` | Optional managed project-local Skill | 0 |

Public reports require explicit --reviewer IDs or deliberate --all-reviewers selection. Use command-specific `--help`. Errors are returned as nonzero exit codes; routine user errors at the public entry point do not print a traceback. Exact parsers and whitespace-word counting have limited scope. Unknown served model revisions remain unknown.

## Managed Skill installation

```sh
python judgment.py skill install --project /path/to/existing/project --dry-run
python judgment.py skill install --project /path/to/existing/project
python judgment.py skill uninstall --project /path/to/existing/project --dry-run
python judgment.py skill uninstall --project /path/to/existing/project
```

On Windows quote paths containing spaces. Use an existing project directory. Installation creates only `.agents/skills/judgment-preserver/` with an installation receipt; it never replaces an existing Skill or changes global settings. Explicitly invoke `$judgment-preserver` in a supporting host. The core content is unchanged since v0.2 and general efficacy is not established.

Uninstall requires the receipt and an exact match of managed files/directories. If you edit or add anything, it refuses before deleting any managed file; inspect and remove manually if that is your choice. Links/reparse paths are refused. Empty `.agents/skills` parent directories are retained. Receipts and local files are trusted, not signed; avoid concurrent editing. An existing manual installation should not be relabeled as managed by fabricating a receipt.
