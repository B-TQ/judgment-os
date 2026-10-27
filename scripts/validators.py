"""Deterministic checks for declared properties, never safety/aesthetic judgments."""
import csv
import io
import json
import re


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def check(spec, answer):
    validate_spec(spec)
    kind = spec["kind"]
    text = answer.strip()
    try:
        if kind == "json_exact":
            value = json.loads(text, object_pairs_hook=_unique_object,
                               parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))
            # JSON boolean and number must not compare equal (True == 1 in Python).
            passed = json.dumps(value, sort_keys=True) == json.dumps(spec["value"], sort_keys=True)
        elif kind == "csv_exact":
            rows = list(csv.reader(io.StringIO(text), strict=True))
            passed = rows == [spec["headers"], *spec["rows"]]
        elif kind == "exact_text":
            passed = text == spec["value"]
        elif kind == "headings":
            headings = re.findall(r"^#{1,6} .+$", text, re.M)
            passed = headings == spec["values"]
        elif kind == "lines_prefix":
            lines = text.splitlines()
            passed = len(lines) == spec["lines"] and lines[0].startswith(spec["prefix"])
        elif kind == "word_count":
            passed = spec["min"] <= len(text.split()) <= spec["max"]
        else:
            raise ValueError(f"Unknown validator: {kind}")
        return {"kind": kind, "pass": passed, "detail": "matched" if passed else "declared property failed"}
    except (json.JSONDecodeError, csv.Error, ValueError) as exc:
        if kind not in KINDS:
            raise
        return {"kind": kind, "pass": False, "detail": str(exc)}


KINDS = {"json_exact", "csv_exact", "exact_text", "headings", "lines_prefix", "word_count"}


def validate_spec(spec):
    if not isinstance(spec, dict) or spec.get("kind") not in KINDS:
        raise ValueError("Unknown validator configuration")
    kind = spec["kind"]
    if kind in ("json_exact", "exact_text"):
        if "value" not in spec or kind == "exact_text" and not isinstance(spec["value"], str):
            raise ValueError("Validator value is missing or invalid")
        if kind == "json_exact":
            json.dumps(spec["value"], allow_nan=False)
    elif kind == "csv_exact":
        if not isinstance(spec.get("headers"), list) or not isinstance(spec.get("rows"), list):
            raise ValueError("CSV validator needs headers and rows")
        if not all(isinstance(row, list) and len(row) == len(spec["headers"]) and all(isinstance(v, str) for v in row)
                   for row in [spec["headers"], *spec["rows"]]):
            raise ValueError("CSV validator columns/values are invalid")
    elif kind == "headings":
        if not isinstance(spec.get("values"), list) or not spec["values"] or not all(isinstance(v, str) and re.fullmatch(r"#{1,6} .+", v) for v in spec["values"]):
            raise ValueError("Heading validator needs valid heading strings")
    elif kind == "lines_prefix":
        if type(spec.get("lines")) is not int or spec["lines"] < 1 or not isinstance(spec.get("prefix"), str):
            raise ValueError("Line validator needs positive line count and string prefix")
    elif kind == "word_count":
        if type(spec.get("min")) is not int or type(spec.get("max")) is not int or not 0 <= spec["min"] <= spec["max"]:
            raise ValueError("Word-count validator needs ordered nonnegative integer bounds")


def validate(specs, answer):
    results = [check(spec, answer) for spec in specs]
    return {"scope": "declared properties only; human hard-gate review still required",
            "status": "pass" if results and all(x["pass"] for x in results) else
                      "fail" if results else "not_applicable", "checks": results}
