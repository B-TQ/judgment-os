#!/usr/bin/env python3
"""Allowlist source packaging: never include runs, private maps, reviewer data or traces."""
import argparse
import hashlib
import re
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TOP = ("README.md", "README.zh-CN.md", "CHANGELOG.md", "LICENSE", ".gitignore", ".gitattributes",
       "AGENTS.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md", "judgment.py", "VERSION", "LAUNCH_REPORT.md", "GITHUB_OPTIMIZATION_REPORT.md", "TRY_DEMO.cmd")
DIRS = (".agents", ".github", "distribution", "docs", "evals", "examples", "global", "scripts", "tests", "legacy")
SUFFIXES = {".md", ".txt", ".py", ".json", ".yml", ".yaml", ".snippet", ".cjs"}
PRIVATE_DIRS = {"__pycache__", ".git", "runs", "review-exports", "artifacts", "traces", "workspaces", "judges", "paired_judges", "outputs", "prompts", "states", "review_packets"}
PRIVATE_FILES = {"private_condition_map.json", "protocol.json", "cases_snapshot.json", "skill_snapshot.json",
                 "adapter_plan.json", "cli_probe.json", "validation.json", "report.json", "report.md", "ratings.csv",
                 "private_manifest.json", "calibration_result.json", "calibration_plan.json",
                 "expected_codes.json", "expected_probe_codes.json", "probe_result.json", "paired_report.json", "study_plan.json"}


def public_source(path):
    parts = path.relative_to(ROOT).parts
    return (not (set(parts) & PRIVATE_DIRS) and path.name not in PRIVATE_FILES
            and not path.name.endswith((".receipt.json", ".ratings.json", ".last-message.tmp")))


def sources():
    paths = [ROOT / p for p in TOP]
    for name in DIRS:
        paths.extend(p for p in (ROOT / name).rglob("*") if p.is_file()
                     and (p.suffix in SUFFIXES or p.name in (".gitignore", "LICENSE"))
                     and public_source(p))
    # Artwork is public only in this reviewed directory, not arbitrary study exports.
    assets = ROOT / "docs/launch/assets"
    paths.extend(p for p in assets.rglob("*") if p.is_file()
                 and p.suffix in {".svg", ".html", ".png"} and public_source(p))
    return sorted(set(paths), key=lambda p: p.relative_to(ROOT).as_posix())


def version():
    value = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+(?:\.\d+)?", value):
        raise ValueError("VERSION must contain a numeric release version")
    return value


def manifest_text():
    return "".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT).as_posix()}\n" for p in sources())


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--zip", dest="archive")
    args = parser.parse_args(argv)
    manifest = ROOT / "SHA256SUMS.txt"
    expected = manifest_text()
    if args.check:
        if not manifest.exists() or manifest.read_text(encoding="utf-8") != expected:
            raise ValueError("Release checksum manifest differs; regenerate before packaging")
    else:
        manifest.write_bytes(expected.encode("utf-8"))
    skill = ROOT / ".agents/skills/judgment-preserver/SKILL.md"
    if skill.read_bytes() != (ROOT / "distribution/judgment-preserver-v0.2-SKILL.md").read_bytes():
        raise ValueError("Portable Skill distribution copy is out of sync")
    for ref in (skill.parent / "references").rglob("*"):
        if ref.is_file():
            portable = ROOT / "distribution/references" / ref.relative_to(skill.parent / "references")
            if not portable.is_file() or portable.read_bytes() != ref.read_bytes():
                raise ValueError("Portable Skill references are missing or out of sync")
    if args.archive:
        archive = Path(args.archive).resolve()
        if archive.is_relative_to(ROOT):
            raise ValueError("Save release ZIP outside the source directory")
        if archive.exists():
            raise FileExistsError("Refusing to overwrite an existing release archive")
        archive.parent.mkdir(parents=True, exist_ok=True)
        # Fixed timestamps and sorted files make the archive stable for identical source bytes.
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
            for p in [*sources(), manifest]:
                info = zipfile.ZipInfo("judgment-os-v" + version() + "/" + p.relative_to(ROOT).as_posix(), (2026, 10, 27, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                z.writestr(info, p.read_bytes())
        print(f"Source ZIP: {archive}")
    print(f"PASS: {len(sources())} allowlisted source files; Skill copy synchronized")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
