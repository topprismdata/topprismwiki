#!/usr/bin/env python3
"""Fail on common accidental private-data patterns in a public package."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".jsonl", ".py", ".toml", ".txt", ".html", ".css", ".js", ".sh"}
PATTERNS = (
    ("absolute_user_path", re.compile(r"/(?:Users|home)/[A-Za-z0-9][A-Za-z0-9._-]*(?:/|$)")),
    ("windows_user_path", re.compile(r"[A-Za-z]:\\Users\\[A-Za-z0-9][A-Za-z0-9._-]*")),
    ("api_secret", re.compile(r"(?i)(?:api[_ -]?key|access[_ -]?token|password|secret)\s*[:=]\s*[^<\s][^\s,;]{8,}")),
    ("openai_like_key", re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b")),
    ("old_wechat_skill_name", re.compile("llmwiki" + r"-formalize-wechat")),
)
FORBIDDEN_NAMES = {".DS_Store", "chat_registry.json", "sync_state.json", "batches.json", "wechat_manifest.json"}
SKIP_PARTS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache"}


def files(root: Path):
    for path in root.rglob("*"):
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.is_file():
            yield path


def git_history(root: Path) -> str:
    git = root / ".git"
    if not git.exists():
        return ""
    completed = subprocess.run(["git", "-C", str(root), "log", "--all", "-p", "--no-ext-diff"], capture_output=True, text=True, check=False)
    return completed.stdout


def scan(root: Path) -> list[str]:
    findings: list[str] = []
    for path in files(root):
        if path.name in FORBIDDEN_NAMES:
            findings.append(f"forbidden_filename:{path.relative_to(root)}")
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(f"non_text_file:{path.relative_to(root)}")
            continue
        for label, pattern in PATTERNS:
            if pattern.search(text):
                findings.append(f"{label}:{path.relative_to(root)}")
    for label, pattern in PATTERNS:
        if pattern.search(git_history(root)):
            findings.append(f"history_{label}")
    return sorted(set(findings))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args(argv)
    findings = scan(Path(args.root).resolve())
    payload = {"state": "accepted" if not findings else "blocked", "findings": findings}
    import json
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not findings else 2


if __name__ == "__main__":
    raise SystemExit(main())
