# Command reference

[Documentation map / 文档导航](README.md) · [Quickstart EN](QUICKSTART.md) · [中文](QUICKSTART.zh-CN.md) · [Optional Skill EN／中文](USAGE_DECISION.md)

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
| `python judgment.py review --help` | Re-keyed review export/import subcommands and immutable model-rating imports | 0 |
| `python judgment.py report --out STUDY --reviewer ID ...` | Selected-phase model review report | 0 |
| `python judgment.py selftest --out NEW_DIR` | Larger zero-answer pipeline smoke test | 0 |
| `python judgment.py release --check` | Verify source manifest | 0 |
| `python judgment.py skill install/uninstall --project PROJECT [--dry-run]` | Optional managed project-local Skill | 0 |

Public reports require explicit --reviewer IDs or deliberate --all-reviewers selection. Use command-specific `--help`. Errors are returned as nonzero exit codes; routine user errors at the public entry point do not print a traceback. Exact parsers and whitespace-word counting have limited scope. Unknown served model revisions remain unknown.

中文：doctor、demo、check 是离线入口；prepare 固定研究输入，run 默认只生成计划；collect 导入真实外部回答；review 导出／导入匿名评审材料；report 必须明确选择评审轮次。表中的 0 表示默认不调用模型，不是启用 live 参数后的承诺。目标项目路径须存在，带空格时加引号。

## Managed Skill installation

```sh
python judgment.py skill install --project /path/to/existing/project --dry-run
python judgment.py skill install --project /path/to/existing/project
python judgment.py skill uninstall --project /path/to/existing/project --dry-run
python judgment.py skill uninstall --project /path/to/existing/project
```

On Windows quote paths containing spaces. Use an existing project directory. Installation creates only `.agents/skills/judgment-preserver/` with an installation receipt; it never replaces an existing Skill or changes global settings. Explicitly invoke `$judgment-preserver` in a supporting host. The core content is unchanged since v0.2 and general efficacy is not established.

Uninstall requires the receipt and an exact match of managed files/directories. If you edit or add anything, it refuses before deleting any managed file; inspect and remove manually if that is your choice. Links/reparse paths are refused. Empty `.agents/skills` parent directories are retained. Receipts and local files are trusted, not signed; avoid concurrent editing. An existing manual installation should not be relabeled as managed by fabricating a receipt.
