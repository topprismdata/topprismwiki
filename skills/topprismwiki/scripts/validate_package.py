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
        if path.read_text(encoding="utf-8").startswith("\ufeff"):
            findings.append(f"utf8_bom:{path.relative_to(root)}")
    repo_root = root.parent.parent
    markdown_paths = list(root.rglob("*.md"))
    markdown_paths.extend([repo_root / "README.md", repo_root / "README.en.md"])
    markdown_paths.extend((repo_root / "docs").rglob("*.md"))
    for path in dict.fromkeys(markdown_paths):
        text = path.read_text(encoding="utf-8")
        if "TODO" in text:
            findings.append(f"unfinished_placeholder:{path.relative_to(repo_root)}")
        if text.startswith("\ufeff"):
            findings.append(f"utf8_bom:{path.relative_to(repo_root)}")

        for target in re.findall(r"\]\(([^)]+)\)", text):
            target = target.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "<")):
                continue
            candidate = (path.parent / target).resolve()
            if not candidate.exists():
                findings.append(f"broken_link:{path.relative_to(repo_root)}:{target}")

    catalog_path = root / "references" / "error-catalog.json"
    catalog: dict = {}
    catalog_error: Exception | None = None
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        catalog_error = error

    required_docs = (
        "docs/zh-CN/getting-started.md",
        "docs/zh-CN/synthetic-walkthrough.md",
        "docs/zh-CN/production-setup.md",
        "docs/zh-CN/adapters.md",
        "docs/zh-CN/operations.md",
        "docs/zh-CN/troubleshooting.md",
        "docs/zh-CN/privacy.md",
        "docs/zh-CN/faq.md",
        "docs/en/getting-started.md",
        "docs/en/synthetic-walkthrough.md",
        "docs/en/production-setup.md",
        "docs/en/adapters.md",
        "docs/en/operations.md",
        "docs/en/troubleshooting.md",
        "docs/en/privacy.md",
        "docs/en/faq.md",
    )
    for relative in required_docs:
        if not (root.parent.parent / relative).exists():
            findings.append(f"missing_public_doc:{relative}")

    for relative in required_docs:
        if relative.startswith("docs/zh-CN/"):
            mirror = "docs/en/" + relative.removeprefix("docs/zh-CN/")
            if not (root.parent.parent / mirror).exists():
                findings.append(f"missing_language_mirror:{relative}:{mirror}")
    for relative in ("docs/zh-CN/troubleshooting.md", "docs/en/troubleshooting.md"):
        text = (root.parent.parent / relative).read_text(encoding="utf-8") if (root.parent.parent / relative).exists() else ""
        for code in catalog.get("errors", {}):
            if code not in text:
                findings.append(f"error_code_missing_from_docs:{relative}:{code}")

    if catalog_error:
        findings.append(f"invalid_error_catalog:{catalog_error}")
    for code, item in catalog.get("errors", {}).items():
        docs = item.get("docs")
        if not isinstance(docs, str) or not (root.parent.parent / docs.split("#", 1)[0]).exists():
            findings.append(f"error_doc_missing:{code}:{docs}")

    runner = root / "scripts" / "topprismwiki.py"
    if "def diagnose(" not in runner.read_text(encoding="utf-8"):
        findings.append("missing_diagnose_command")
    payload = {"state": "accepted" if not findings else "blocked", "skills": len(paths), "findings": sorted(set(findings))}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not findings else 2


if __name__ == "__main__":
    raise SystemExit(main())
