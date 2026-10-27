#!/usr/bin/env python3
"""Non-authoritative, dependency-free Skill manifest validation and review cues.

IMPORTANT: keyword cues are NOT instruction hierarchy or permission judgements.
"""
import argparse
import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PATTERNS = {
    "mandatory_wording_candidate": re.compile(r"\b(?:must|shall|required|never|always|only|strictly)\b", re.I),
    "suggestion_wording_candidate": re.compile(r"\b(?:should|recommended|prefer|usually|typically|may|optional|default)\b", re.I),
    "example_wording_candidate": re.compile(r"\b(?:for example|e\.g\.|example:|sample|illustrat)\b", re.I),
}


def audit(path):
    path = Path(path)
    issues = []
    cues = []
    if not path.is_file():
        return {"file": str(path), "metadata_valid": False, "issues": ["SKILL.md not found"], "review_cues": []}
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {"file": str(path), "metadata_valid": False, "issues": ["YAML frontmatter must begin with ---"], "review_cues": []}
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {"file": str(path), "metadata_valid": False, "issues": ["YAML frontmatter has no closing ---"], "review_cues": []}
    # This lightweight validator intentionally handles scalar key: value only.
    metadata = {}
    for line in lines[1:end]:
        m = re.match(r"^([\w-]+):\s*(.*)$", line)
        if m:
            value = m.group(2).strip()
            if value.startswith(('"', "'")) and value.endswith(value[0]):
                value = value[1:-1]
            metadata[m.group(1)] = value
    name = metadata.get("name", "")
    description = metadata.get("description", "")
    if not NAME_RE.fullmatch(name) or len(name) > 64:
        issues.append("name must be <=64 lowercase alphanumerics/hyphens, no repeated/edge hyphens")
    if name and path.parent.name != name:
        issues.append("name should match Skill directory name")
    if not 1 <= len(description) <= 1024:
        issues.append("description must be nonempty and <=1024 characters")
    if not any(line.strip() for line in lines[end + 1:]):
        issues.append("Skill body is empty")
    for lineno, line in enumerate(lines[end + 1:], end + 2):
        if not line.strip() or line.lstrip().startswith('```'):
            continue
        tags = [name for name, pattern in PATTERNS.items() if pattern.search(line)]
        if tags:
            cues.append({"line": lineno, "signals": tags, "excerpt": line.strip()[:180]})
    return {
        "file": str(path), "metadata_valid": not issues, "issues": issues,
        "review_cues": cues,
        "caveat": "Signals identify text for human review. They never assign authority or permission to deviate."
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills", nargs="+", help="One or more SKILL.md paths")
    parser.add_argument("--strict-metadata", action="store_true", help="Nonzero exit on detected metadata issues")
    parser.add_argument("--json", action="store_true", help="Machine-readable output")
    args = parser.parse_args(argv)
    results = [audit(p) for p in args.skills]
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for report in results:
            print(f"{report['file']}: {'PASS' if report['metadata_valid'] else 'FAIL'} metadata")
            for issue in report['issues']:
                print(f"  ERROR: {issue}")
            print(f"  {len(report['review_cues'])} human-review wording cues (NOT policy classifications)")
    return 1 if args.strict_metadata and any(not r['metadata_valid'] for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
