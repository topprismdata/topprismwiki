#!/usr/bin/env python3
"""Validate the public package without depending on Codex internals."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def frontmatter(path: Path) -> tuple[str | None, str | None]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) < 5 or lines[0].strip() != "---":
        return None, None
    values: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        match = re.match(r"^(name|description):\s*(.+)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip('"')
    return values.get("name"), values.get("description")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    findings: list[str] = []
    parent = root / "SKILL.md"
    paths = [parent] + sorted((root / "subskills").glob("*/SKILL.md"))
    for path in paths:
        name, description = frontmatter(path)
        expected = path.parent.name if path.parent != root else "topprismwiki"
        if not name:
            findings.append(f"missing_name:{path.relative_to(root)}")
        elif name != expected:
            findings.append(f"name_directory_mismatch:{path.relative_to(root)}:{name}:{expected}")
        if not description or "TODO" in description:
            findings.append(f"missing_description:{path.relative_to(root)}")
        if ("llmwiki" + "-formalize-wechat") in path.read_text(encoding="utf-8"):
            findings.append(f"old_skill_name:{path.relative_to(root)}")
    for path in root.rglob("*.md"):
        if "TODO" in path.read_text(encoding="utf-8"):
            findings.append(f"unfinished_placeholder:{path.relative_to(root)}")
    payload = {"state": "accepted" if not findings else "blocked", "skills": len(paths), "findings": sorted(set(findings))}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not findings else 2


if __name__ == "__main__":
    raise SystemExit(main())
