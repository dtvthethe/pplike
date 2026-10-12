#!/usr/bin/env python3
"""Check a RealWorld Markdown spec locally without changing files."""

import argparse
import json
from pathlib import Path
import re
import sys


def json_blocks(text, path, errors, required=False):
    blocks = re.findall(r"^```json\s*\n(.*?)^```\s*$", text, re.M | re.S)
    if required and not blocks:
        errors.append(f"{path}: missing JSON block")
    for index, block in enumerate(blocks, 1):
        try:
            json.loads(block)
        except ValueError as error:
            errors.append(f"{path}: JSON block {index}: {error}")


def check(code, root, catalog, spec):
    errors = []
    catalog_path = root / catalog
    spec_path = root / spec
    lines = catalog_path.read_text(encoding="utf-8").splitlines()
    header = None
    matches = []
    for line in lines:
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if all(column in cells for column in ("Code", "Method", "Endpoint")):
            header = cells
            continue
        if header is None:
            continue
        row = dict(zip(header, cells))
        if row.get("Code") == code:
            matches.append(row)
    if len(matches) != 1:
        return [f"{catalog_path}: expected one row for {code}, found {len(matches)}"]
    row = matches[0]
    method = row.get("Method", "").strip("`").upper()
    endpoint = row.get("Endpoint", "").strip("`")
    if not method or not endpoint:
        return [f"{catalog_path}: missing Method or Endpoint for {code}"]
    text = spec_path.read_text(encoding="utf-8")
    http_blocks = re.findall(r"^```http\s*\n(.*?)^```\s*$", text, re.M | re.S)
    expected = f"{method} {endpoint}"
    if not any(expected in [line.strip() for line in block.splitlines()]
               for block in http_blocks):
        errors.append(f"{spec_path}: missing HTTP endpoint {expected}")
    json_blocks(text, spec_path, errors)
    checked = set()
    for target in re.findall(r"\[[^\]\n]+\]\(([^)\n]+)\)", text):
        target = target.strip().removeprefix("<").removesuffix(">")
        if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
            continue
        local = target.split("#", 1)[0]
        if not local.endswith(".md"):
            continue
        if Path(local).is_absolute():
            errors.append(f"{spec_path}: expected relative Markdown link: {target}")
            continue
        linked = (spec_path.parent / local).resolve()
        if linked in checked:
            continue
        checked.add(linked)
        if not linked.is_file():
            errors.append(f"{spec_path}: missing link target: {target}")
            continue
        json_blocks(linked.read_text(encoding="utf-8"), linked, errors,
                    required="response_format" in Path(local).parts)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("code", help="Code from the endpoint catalog, e.g. US_003")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--catalog", type=Path, default=Path("my_tasks/ENDPOINTS.md"))
    parser.add_argument("--spec", type=Path)
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_]+", args.code):
        parser.error("code must contain only letters, digits, and underscores")
    spec = args.spec if args.spec is not None else Path(f"my_tasks/{args.code}.md")
    try:
        errors = check(args.code, args.root, args.catalog, spec)
    except (OSError, UnicodeError) as error:
        errors = [str(error)]
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {args.code} — method/path, JSON syntax, and local Markdown links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
