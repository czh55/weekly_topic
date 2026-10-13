#!/usr/bin/env python3
"""Validate weekly topic entries and keep docs/index.json sorted."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INDEX = DOCS / "index.json"
HISTORY = ROOT / "data" / "history.json"


def load_index() -> list[dict]:
    if not INDEX.exists():
        return []
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit("docs/index.json must be a JSON array")
    return data


def validate(items: list[dict]) -> list[str]:
    errors: list[str] = []
    seen_slugs: set[str] = set()
    for i, item in enumerate(items):
        prefix = f"[{i}]"
        for key in ("week", "date", "title", "slug"):
            if not item.get(key):
                errors.append(f"{prefix} missing required field: {key}")
        slug = item.get("slug")
        if slug:
            if slug in seen_slugs:
                errors.append(f"{prefix} duplicate slug: {slug}")
            seen_slugs.add(slug)
        outputs = item.get("outputs") or {}
        for kind, filename in outputs.items():
            path = DOCS / filename
            if not path.exists():
                errors.append(f"{prefix} missing output file ({kind}): {filename}")
    return errors


def sort_items(items: list[dict]) -> list[dict]:
    return sorted(items, key=lambda x: (x.get("date") or "", x.get("week") or ""), reverse=True)


def write_index(items: list[dict]) -> None:
    INDEX.write_text(
        json.dumps(items, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def sync_history(items: list[dict]) -> None:
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    HISTORY.write_text(
        json.dumps(
            [
                {
                    "week": i.get("week"),
                    "date": i.get("date"),
                    "slug": i.get("slug"),
                    "title": i.get("title"),
                }
                for i in items
            ],
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate / sort weekly topic index")
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate only; do not rewrite files",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="sort index.json and sync data/history.json",
    )
    args = parser.parse_args()
    if not args.check and not args.write:
        args.write = True

    items = load_index()
    errors = validate(items)
    if errors:
        print("Validation failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    sorted_items = sort_items(items)
    if args.write:
        write_index(sorted_items)
        sync_history(sorted_items)
        print(f"OK: {len(sorted_items)} week(s) → docs/index.json")
    else:
        print(f"OK: {len(sorted_items)} week(s) validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
