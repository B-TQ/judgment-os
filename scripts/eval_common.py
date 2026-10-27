"""Shared file integrity and best-effort redaction helpers (stdlib only)."""
import hashlib
import json
import os
import re
from pathlib import Path

ID_RE = re.compile(r"S[0-9a-f]{12}")
JUDGE_RE = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}")


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Atomic replacement avoids leaving half-written status on interruption.
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def redact(text, extra=()):
    # Never promise exhaustive secret/PII detection. Custom literals are supported.
    text = re.sub(r"\bsk-[A-Za-z0-9_-]{12,}\b", "[REDACTED_KEY]", text)
    text = re.sub(r"(?i)(bearer\s+)[A-Za-z0-9._~+/-]{8,}", r"\1[REDACTED]", text)
    text = re.sub(r"(?i)((?:api[_-]?key|token|password|secret)\s*[=:]\s*)[^\s,;]+",
                  r"\1[REDACTED]", text)
    text = re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[REDACTED_EMAIL]", text)
    text = re.sub(r"[A-Za-z]:[\\/](?:Users|CodexData)[^\s\"<>]*", "[REDACTED_PATH]", text)
    for literal in sorted(set(extra), key=len, reverse=True):
        if literal:
            text = text.replace(literal, "[REDACTED_CUSTOM]")
    return text


def private_file(path):
    # POSIX permissions; Windows access depends on parent directory ACL.
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def load_mapping(out):
    out = Path(out)
    rows = read_json(out / "private_condition_map.json")
    protocol = read_json(out / "protocol.json")
    if protocol.get("schema_version") != 3:
        raise ValueError("Use a fresh v0.3 experiment; v0.2 run directories are not silently migrated")
    if digest(json.dumps(rows, sort_keys=True, ensure_ascii=False)) != protocol["mapping_sha256"]:
        raise ValueError("Private mapping changed since preparation")
    cases = read_json(out / "cases_snapshot.json")
    if digest(json.dumps(cases, sort_keys=True, ensure_ascii=False)) != protocol["cases_sha256"]:
        raise ValueError("Case snapshot changed since preparation")
    seen = set()
    pairs = set()
    for row in rows:
        key = row.get("blind_id", "")
        if not ID_RE.fullmatch(key) or key in seen:
            raise ValueError("Invalid or duplicate blind_id in private map")
        pair = (row["case_id"], row["repeat"], row["condition"])
        if row["condition"] not in protocol["conditions"] or pair in pairs:
            raise ValueError("Invalid or duplicate condition/case/repeat in private map")
        seen.add(key)
        pairs.add(pair)
    expected = {(c["id"], r, cond) for c in cases for r in range(1, protocol["repeats"] + 1) for cond in protocol["conditions"]}
    if pairs != expected:
        raise ValueError("Incomplete or unexpected condition/case/repeat mapping")
    return {row["blind_id"]: row for row in rows}
