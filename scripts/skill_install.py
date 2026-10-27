"""Project-local managed installation; never overwrite or remove user changes."""
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile

NAME = "judgment-preserver"
RECEIPT = ".judgment-os-install.json"


def linked(path):
    return path.is_symlink() or bool(getattr(path.lstat(), "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def destination(project):
    project = Path(project).resolve(strict=True)
    if not project.is_dir():
        raise ValueError("Project must be an existing directory")
    target = project / ".agents" / "skills" / NAME
    for p in (project / ".agents", project / ".agents/skills", target):
        if p.exists() or p.is_symlink():
            if linked(p) or not p.is_dir():
                raise ValueError("Skill path must contain ordinary directories, not links/reparse points")
    if not target.resolve().is_relative_to(project):
        raise ValueError("Target escaped the named project")
    return target


def tree(path):
    files, directories = {}, set()
    def walk(folder):
        for p in folder.iterdir():
            if linked(p):
                raise ValueError("Links/reparse points are not managed")
            rel = p.relative_to(path).as_posix()
            if p.is_dir():
                directories.add(rel)
                walk(p)
            elif p.is_file():
                files[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
            else:
                raise ValueError("Unsupported filesystem entry")
    walk(path)
    return files, directories


def install(root, project, dry_run=False):
    root = Path(root)
    target = destination(project)
    if target.exists():
        raise FileExistsError("Skill already exists; nothing was overwritten")
    source = root / ".agents/skills" / NAME
    files, directories = tree(source)
    if RECEIPT in files or "SKILL.md" not in files:
        raise ValueError("Invalid source Skill")
    result = {"action": "install", "target": str(target), "dry_run": dry_run, "files": len(files)}
    if dry_run:
        return result
    target.parent.mkdir(parents=True, exist_ok=True)
    # Stage under the verified parent, then rename only into a fresh destination.
    with tempfile.TemporaryDirectory(prefix=".judgment-install-", dir=target.parent) as td:
        staged = Path(td) / NAME
        staged.mkdir()
        for name in sorted(directories):
            (staged / name).mkdir(parents=True, exist_ok=True)
        for name in files:
            (staged / name).write_bytes((source / name).read_bytes())
        receipt = {"managed_by": "judgment-os", "version": (root / "VERSION").read_text(encoding="utf-8").strip(),
                   "files": files, "directories": sorted(directories)}
        (staged / RECEIPT).write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        if target.exists():
            raise FileExistsError("Target appeared during installation; nothing overwritten")
        os.rename(staged, target)
    return result


def uninstall(root, project, dry_run=False):
    target = destination(project)
    if not target.is_dir():
        raise FileNotFoundError("Managed Skill is not installed")
    files, directories = tree(target)
    receipt = json.loads((target / RECEIPT).read_text(encoding="utf-8"))
    if receipt.get("managed_by") != "judgment-os" or not isinstance(receipt.get("files"), dict):
        raise ValueError("No recognized installation receipt")
    expected = receipt["files"]
    # Compare exact names as well as hashes. Do not touch a modified or extended tree.
    if {k: v for k, v in files.items() if k != RECEIPT} != expected or directories != set(receipt.get("directories", [])):
        raise ValueError("Installed files changed or user files were added; remove manually after review")
    result = {"action": "uninstall", "target": str(target), "dry_run": dry_run, "files": len(files)}
    if dry_run:
        return result
    # No recursive deletion: each managed file was verified before any mutation.
    for name in sorted(files):
        (target / name).unlink()
    for name in sorted(directories, key=lambda s: (s.count("/"), s), reverse=True):
        (target / name).rmdir()
    target.rmdir()
    return result
