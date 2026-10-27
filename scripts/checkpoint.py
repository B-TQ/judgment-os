#!/usr/bin/env python3
"""Create a new immutable version backup; optional evidence stays private."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys
import zipfile

import release


def checkpoint(destination, evidence=()):
    dest = Path(destination).resolve()
    if dest.exists():
        raise FileExistsError("Backup destination already exists; checkpoints never overwrite")
    root = release.ROOT.resolve()
    if dest.is_relative_to(root):
        raise ValueError("Backup must be outside source directory")
    inputs = []
    for item in evidence:
        path = Path(item).resolve()
        if not path.is_dir() or path == dest or dest.is_relative_to(path) or path.is_relative_to(dest):
            raise ValueError("Evidence must be a separate existing directory")
        if path.is_symlink() or any(p.is_symlink() for p in path.rglob("*")):
            raise ValueError("Evidence symlinks are not copied into backups")
        inputs.append(path)
    # A source checksum must already be valid; checkpoint does not rewrite evidence.
    release.main(["--check"])
    dest.mkdir(parents=True)
    archive = dest / f"Judgment-OS-v{release.version()}-source.zip"
    release.main(["--check", "--zip", str(archive)])
    evidence_meta = []
    for index, path in enumerate(inputs, 1):
        name = f"private-evidence-{index}"
        target = dest / name
        shutil.copytree(path, target)
        hashes = {p.relative_to(target).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in sorted(target.rglob("*")) if p.is_file()}
        evidence_meta.append({"directory": name, "files": hashes})
    record = {"version": release.version(), "created_at_utc": datetime.now(timezone.utc).isoformat(),
              "source_archive": archive.name, "source_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
              "evidence": evidence_meta, "private": bool(inputs), "status": "complete"}
    (dest / "checkpoint.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Checkpoint complete: {dest}")
    return record


def verify(destination):
    dest = Path(destination).resolve()
    record = json.loads((dest / "checkpoint.json").read_text(encoding="utf-8"))
    archive = (dest / record["source_archive"]).resolve()
    if not archive.is_relative_to(dest) or record.get("status") != "complete":
        raise ValueError("Invalid checkpoint record")
    if hashlib.sha256(archive.read_bytes()).hexdigest() != record["source_sha256"]:
        raise ValueError("Backup source archive hash mismatch")
    for item in record["evidence"]:
        target = (dest / item["directory"]).resolve()
        if not target.is_relative_to(dest) or not target.is_dir():
            raise ValueError("Invalid evidence path")
        hashes = {p.relative_to(target).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in sorted(target.rglob("*")) if p.is_file()}
        if hashes != item["files"]:
            raise ValueError("Backup evidence changed or missing")
    print(f"Checkpoint verified: {dest}")
    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dest")
    group.add_argument("--verify")
    parser.add_argument("--evidence", action="append", default=[])
    args = parser.parse_args()
    try:
        if args.verify:
            verify(args.verify)
        else:
            checkpoint(args.dest, args.evidence)
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
