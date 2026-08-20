#!/usr/bin/env python3
"""Small, dependency-free governed Topprismwiki runner for public deployments."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable
from zoneinfo import ZoneInfo


SCHEMA = "topprismwiki-public-runner-v1"
STATES = {"accepted", "no_change", "quarantined", "blocked", "partial", "rolled_back", "review_required", "retry_queued"}
SECRET_PATTERNS = (
    re.compile(r"(?i)(api[_ -]?key|access[_ -]?token|secret|password|passwd|authorization)\s*[:=]\s*\S+"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._-]{12,}"),
)
REL_RE = re.compile(r"(?m)^-\s+\[\[([^\]|]+)(?:\|[^\]]+)?\]\]\s*·\s*([a-z_]+)\s*$")


class RunnerError(RuntimeError):
    pass


def now(tz: ZoneInfo) -> str:
    return datetime.now(tz).isoformat(timespec="seconds")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def redact(value: str) -> str:
    for pattern in SECRET_PATTERNS:
        value = pattern.sub("[REDACTED]", value)
    value = re.sub(r"(?i)(/(?:Users|home)/)[^/\s]+", r"\1<user>", value)
    return value


def atomic_write(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def atomic_json(path: Path, value: Any) -> None:
    atomic_write(path, json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def read_json(path: Path, default: Any) -> Any:
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise RunnerError(f"invalid_json:{path.name}:{error.msg}") from error


class Project:
    def __init__(self, root: Path):
        self.root = root.expanduser().resolve()
        self.control = self.root / ".topprismwiki"
        self.config = read_json(self.control / "config.json", {})
        self.workspace = self.root / self.config.get("workspace", "workspace")
        self.vault = self.root / self.config.get("vault", "vault")
        self.wiki = self.vault / self.config.get("wiki", "wiki")
        self.state = self.workspace / "state"
        self.runs = self.workspace / "runs"
        self.artifacts = self.workspace / "artifacts"
        self.tz = ZoneInfo(self.config.get("timezone", "Asia/Shanghai"))

    def ensure(self) -> None:
        self.control.mkdir(parents=True, exist_ok=True)
        for path in (self.workspace, self.vault, self.wiki, self.state, self.runs, self.artifacts):
            path.mkdir(parents=True, exist_ok=True)

    @property
    def batches_path(self) -> Path:
        return self.state / "batches.json"

    @property
    def sources_path(self) -> Path:
        return self.state / "source-registry.json"


def project_from(args: argparse.Namespace) -> Project:
    raw = args.project or os.environ.get("TOPPRISMWIKI_PROJECT") or "."
    project = Project(Path(raw))
    project.ensure()
    return project


def init_project(args: argparse.Namespace) -> int:
    root = Path(args.project or os.environ.get("TOPPRISMWIKI_PROJECT") or ".").expanduser().resolve()
    project = Project(root)
    project.ensure()
    if not (project.control / "config.json").exists():
        atomic_json(project.control / "config.json", {
            "schema": SCHEMA,
            "timezone": "Asia/Shanghai",
            "workspace": "workspace",
            "vault": "vault",
            "wiki": "wiki",
            "privacy_mode": "masked",
            "validation": {"obsidian_cli_required_for_apply": True},
            "adapters": {
                "wechat_cli": "wechat-cli",
                "officecli": "officecli",
                "vision_base_url": "http://127.0.0.1:8088/v1",
                "vision_model": "<local-vision-model>",
            },
        })
    for path, value in (
        (project.state / "batches.json", {"schema": "topprismwiki-batches-v1", "batches": []}),
        (project.sources_path, {"schema": "topprismwiki-sources-v1", "sources": []}),
    ):
        if not path.exists():
            atomic_json(path, value)
    (project.workspace / "inbox").mkdir(parents=True, exist_ok=True)
    print(json.dumps({"state": "initialized", "project": str(root), "config": str(project.control / "config.json")}, ensure_ascii=False, indent=2))
    return 0


def command_exists(command: str) -> bool:
    return shutil.which(command) is not None


def doctor(args: argparse.Namespace) -> int:
    project = project_from(args)
    capability = args.capability
    checks: dict[str, dict[str, Any]] = {
        "core": {"ok": sys.version_info >= (3, 11), "detail": f"python {sys.version_info.major}.{sys.version_info.minor}"},
        "obsidian": {"ok": command_exists("obsidian"), "detail": "obsidian CLI"},
        "wechat": {"ok": command_exists(project.config.get("adapters", {}).get("wechat_cli", "wechat-cli")), "detail": "wechat adapter"},
        "documents": {"ok": command_exists(project.config.get("adapters", {}).get("officecli", "officecli")), "detail": "officecli"},
        "vision": {"ok": bool(project.config.get("adapters", {}).get("vision_base_url")), "detail": "configured image-capable endpoint"},
        "media": {"ok": command_exists("ffmpeg"), "detail": "ffmpeg"},
    }
    selected = checks if capability == "all" else {capability: checks.get(capability, {"ok": False, "detail": "unknown capability"})}
    required = [row for name, row in selected.items() if name == "core" or (name == "obsidian" and args.strict)]
    state = "accepted" if all(row["ok"] for row in required) else "blocked"
    print(json.dumps({"state": state, "project": str(project.root), "capability": capability, "checks": selected, "strict": args.strict}, ensure_ascii=False, indent=2))
    return 0 if state == "accepted" else 2


def input_records(project: Project, source: str) -> list[dict[str, Any]]:
    inbox = project.workspace / "inbox"
    paths: list[Path] = []
    if source in {"all", "wechat"}:
        paths.extend(sorted(inbox.glob("wechat/*.jsonl")))
    if source in {"all", "documents"}:
        paths.extend(sorted(inbox.glob("documents/*.jsonl")))
    paths.extend(sorted(inbox.glob("*.jsonl")))
    records: list[dict[str, Any]] = []
    for path in dict.fromkeys(paths):
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as error:
                records.append({"unit_id": f"invalid-{path.stem}-{line_no}", "state": "blocked", "error": error.msg, "source": path.name})
                continue
            if isinstance(item, dict):
                item = dict(item)
                item.setdefault("unit_id", f"{path.stem}-{line_no:04d}")
                item.setdefault("source", path.name)
                records.append(item)
    return records


def outcome_counts(records: Iterable[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in records:
        state = str(item.get("classification", item.get("state", "evidence_insufficient")))
        counts[state] = counts.get(state, 0) + 1
    return counts


def new_batch(project: Project, source: str, mode: str, records: list[dict[str, Any]], batch_id: str | None = None) -> dict[str, Any]:
    created = now(project.tz)
    seed = json.dumps(records, ensure_ascii=False, sort_keys=True).encode("utf-8")
    batch_id = batch_id or f"{source}-{datetime.now(project.tz).strftime('%Y%m%d-%H%M%S')}-{sha256_bytes(seed)[:8]}"
    counts = outcome_counts(records)
    attachments = sum(len(item.get("attachments", [])) for item in records if isinstance(item.get("attachments", []), list))
    batch = {
        "batch_id": batch_id,
        "schema": "topprismwiki-batch-v1",
        "source": source,
        "mode": mode,
        "state": "previewed" if mode == "preview" else "review_required",
        "started_at": created,
        "completed_at": None,
        "coverage": {"units": len(records), "messages": sum(int(item.get("messages", 1)) for item in records), "attachments": attachments},
        "outcomes": counts,
        "watermark_advanced": False,
        "retryable_units": [str(item["unit_id"]) for item in records if item.get("state") in {"quarantined", "blocked", "evidence_insufficient"}],
        "input_sha256": sha256_bytes(seed),
    }
    run = project.runs / batch_id
    run.mkdir(parents=True, exist_ok=True)
    atomic_json(run / "coverage.json", {"batch": batch, "records": [redacted_record(item) for item in records]})
    atomic_json(run / "review-template.json", {"batch_id": batch_id, "facts": [], "notes": "Replace with a reviewed decision package before apply."})
    return batch


def redacted_record(item: dict[str, Any]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in item.items():
        if key in {"text", "content", "raw", "body"}:
            output[key] = "[REDACTED_EVIDENCE]"
        elif isinstance(value, str):
            output[key] = redact(value)
        else:
            output[key] = value
    return output


def save_batch(project: Project, batch: dict[str, Any]) -> None:
    ledger = read_json(project.batches_path, {"schema": "topprismwiki-batches-v1", "batches": []})
    rows = [row for row in ledger.get("batches", []) if row.get("batch_id") != batch.get("batch_id")]
    rows.append(batch)
    ledger["batches"] = sorted(rows, key=lambda row: str(row.get("started_at", "")))
    atomic_json(project.batches_path, ledger)


def find_batch(project: Project, batch_id: str) -> dict[str, Any]:
    ledger = read_json(project.batches_path, {"batches": []})
    for batch in ledger.get("batches", []):
        if batch.get("batch_id") == batch_id:
            return batch
    raise RunnerError(f"batch_not_found:{batch_id}")


def preview(args: argparse.Namespace) -> int:
    project = project_from(args)
    records = input_records(project, args.source)
    batch = new_batch(project, args.source, "preview", records, args.batch_id)
    batch["state"] = "no_change" if not records else "previewed"
    batch["completed_at"] = now(project.tz)
    save_batch(project, batch)
    print(json.dumps({"state": batch["state"], "batch": batch, "review_template": str(project.runs / batch["batch_id"] / "review-template.json")}, ensure_ascii=False, indent=2))
    return 0


def validate_review(review: dict[str, Any], project: Project) -> list[dict[str, Any]]:
    if not isinstance(review, dict) or not isinstance(review.get("facts"), list):
        raise RunnerError("review_facts_must_be_array")
    facts: list[dict[str, Any]] = []
    for index, fact in enumerate(review["facts"]):
        if not isinstance(fact, dict) or fact.get("status") != "formalized":
            continue
        target = Path(str(fact.get("target", "")))
        if target.is_absolute() or ".." in target.parts or target.suffix.lower() != ".md":
            raise RunnerError(f"invalid_target:{index}")
        content = fact.get("content")
        evidence = fact.get("evidence")
        if not isinstance(content, str) or not content.strip() or not isinstance(evidence, dict):
            raise RunnerError(f"incomplete_fact:{index}")
        source_sha = str(evidence.get("source_sha256", ""))
        if not re.fullmatch(r"[0-9a-fA-F]{64}", source_sha):
            raise RunnerError(f"missing_source_sha256:{index}")
        facts.append({"target": target.as_posix(), "content": content, "evidence": evidence})
    return facts


def apply_update(args: argparse.Namespace) -> int:
    if not args.authorized:
        print(json.dumps({"state": "blocked", "error": "explicit_update_authorization_required"}, ensure_ascii=False, indent=2))
        return 2
    project = project_from(args)
    if args.batch_id:
        batch = find_batch(project, args.batch_id)
    else:
        records = input_records(project, args.source)
        batch = new_batch(project, args.source, "update", records, None)
    run = project.runs / batch["batch_id"]
    review_path = Path(args.review).expanduser().resolve() if args.review else run / "review.json"
    if not review_path.is_file():
        batch.update({"state": "review_required", "completed_at": now(project.tz)})
        save_batch(project, batch)
        print(json.dumps({"state": "review_required", "batch": batch, "review": str(review_path)}, ensure_ascii=False, indent=2))
        return 2
    try:
        facts = validate_review(read_json(review_path, {}), project)
        before: dict[Path, bytes | None] = {}
        for fact in facts:
            target = project.wiki / fact["target"]
            before[target] = target.read_bytes() if target.exists() else None
        rollback = run / "rollback"
        rollback.mkdir(parents=True, exist_ok=True)
        for target, content in ((project.wiki / fact["target"], fact["content"]) for fact in facts):
            if target in before and before[target] is not None:
                atomic_write(rollback / target.relative_to(project.wiki), before[target].decode("utf-8"))
            atomic_write(target, content.rstrip() + "\n")
        report = {"batch_id": batch["batch_id"], "facts_committed": len(facts), "targets": [fact["target"] for fact in facts], "review_sha256": sha256_file(review_path), "state": "accepted"}
        atomic_json(run / "commit-report.json", report)
        batch.update({"mode": "update", "state": "accepted" if facts else "no_change", "completed_at": now(project.tz), "watermark_advanced": bool(facts), "outcomes": {**batch.get("outcomes", {}), "formalized": len(facts)}})
        save_batch(project, batch)
        print(json.dumps({"state": batch["state"], "batch": batch, "commit": report}, ensure_ascii=False, indent=2))
        return 0
    except Exception as error:
        for target, content in before.items():
            if content is None:
                target.unlink(missing_ok=True)
            else:
                atomic_write(target, content.decode("utf-8"))
        batch.update({"state": "rolled_back", "completed_at": now(project.tz), "error": redact(str(error))})
        save_batch(project, batch)
        print(json.dumps({"state": "rolled_back", "batch": batch}, ensure_ascii=False, indent=2))
        return 2


def query(args: argparse.Namespace) -> int:
    project = project_from(args)
    terms = [part.casefold() for part in re.findall(r"[A-Za-z0-9_.-]{2,}|[\u3400-\u9fff]{2,}", args.question)]
    results: list[dict[str, Any]] = []
    for path in sorted(project.wiki.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        folded = text.casefold()
        score = sum(folded.count(term) for term in terms)
        if score <= 0:
            continue
        line = next((idx for idx, value in enumerate(text.splitlines(), 1) if any(term in value.casefold() for term in terms)), 1)
        results.append({"page": path.relative_to(project.vault).as_posix(), "line": line, "page_sha256": sha256_file(path), "score": score, "state": "formal"})
    results.sort(key=lambda row: (-row["score"], row["page"]))
    payload = {"state": "accepted", "question": args.question, "results": results[: args.limit]}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def context(args: argparse.Namespace) -> int:
    project = project_from(args)
    terms = [part.casefold() for part in re.findall(r"[A-Za-z0-9_.-]{2,}|[\u3400-\u9fff]{2,}", args.task)]
    rows: list[str] = [f"# Topprismwiki context\n\nTask: {redact(args.task)}\n", "## Formal evidence\n"]
    used = len(rows[0]) + len(rows[1])
    for path in sorted(project.wiki.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not any(term in text.casefold() for term in terms):
            continue
        addition = f"- `{path.relative_to(project.vault).as_posix()}` (sha256 `{sha256_file(path)}`)\n"
        if used + len(addition) > args.budget:
            rows.append("\n[TRUNCATED: increase --budget to include more formal pages]\n")
            break
        rows.append(addition)
        used += len(addition)
    output = project.artifacts / "contexts" / f"context-{datetime.now(project.tz).strftime('%Y%m%d-%H%M%S')}.md"
    atomic_write(output, "".join(rows))
    print(json.dumps({"state": "accepted", "output": str(output), "characters": used}, ensure_ascii=False, indent=2))
    return 0


def graph(args: argparse.Namespace) -> int:
    project = project_from(args)
    edges: list[dict[str, str]] = []
    for path in sorted(project.wiki.rglob("*.md")):
        source = path.stem
        for target, relation in REL_RE.findall(path.read_text(encoding="utf-8")):
            if not args.entity or args.entity.casefold() in {source.casefold(), target.casefold()}:
                edges.append({"source": source, "target": target, "relation": relation, "state": "formal"})
    candidates = read_json(project.state / "candidates.json", {"candidates": []}).get("candidates", []) if args.include_candidates else []
    print(json.dumps({"state": "accepted", "formal_edges": edges, "candidate_edges": candidates}, ensure_ascii=False, indent=2))
    return 0


def status(args: argparse.Namespace) -> int:
    project = project_from(args)
    ledger = read_json(project.batches_path, {"batches": []})
    batches = ledger.get("batches", [])
    if args.source != "all":
        batches = [row for row in batches if row.get("source") == args.source]
    counts: dict[str, int] = {}
    for row in batches:
        counts[row.get("state", "unknown")] = counts.get(row.get("state", "unknown"), 0) + 1
    payload = {"state": "accepted", "project": str(project.root), "batches": len(batches), "by_state": counts, "formal_pages": len(list(project.wiki.rglob("*.md"))), "watermarks": "per-unit; not advanced by failure"}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def batch_command(args: argparse.Namespace) -> int:
    project = project_from(args)
    ledger = read_json(project.batches_path, {"batches": []})
    rows = ledger.get("batches", [])
    if args.batch_command == "show":
        payload = find_batch(project, args.batch_id)
    else:
        if args.source != "all":
            rows = [row for row in rows if row.get("source") == args.source]
        if args.status != "all":
            rows = [row for row in rows if row.get("state") == args.status]
        payload = {"state": "accepted", "batches": rows}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def _unused_dashboard_legacy(args: argparse.Namespace) -> int:
    project = project_from(args)
    ledger = read_json(project.batches_path, {"batches": []})
    rows = ledger.get("batches", [])
    if args.batch_id:
        rows = [find_batch(project, args.batch_id)]
    safe_rows = [redacted_record(row) for row in rows]
    data = json.dumps(safe_rows, ensure_ascii=False).replace("</", "<\\/")
    title = html.escape(args.title)
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>
:root{{--bg:#f5f7fb;--panel:#fff;--ink:#172033;--muted:#667085;--line:#e5e7eb;--accent:#3857d6;--ok:#087443;--warn:#a15c00;--bad:#b42318}}
@media(prefers-color-scheme:dark){{:root{{--bg:#111827;--panel:#182235;--ink:#edf2f7;--muted:#a8b3c2;--line:#334155;--accent:#9bb2ff}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
main{{max-width:1180px;margin:auto;padding:32px 20px}}header{{display:flex;justify-content:space-between;gap:16px;align-items:end;margin-bottom:24px}}h1{{margin:0;font-size:30px}}.muted{{color:var(--muted)}}.grid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:20px}}.card,.table-wrap{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px}}.value{{font-size:26px;font-weight:700;margin-top:6px}}.table-wrap{{overflow:auto;padding:0}}table{{border-collapse:collapse;width:100%}}th,td{{padding:13px 15px;text-align:left;border-bottom:1px solid var(--line);white-space:nowrap}}th{{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}}.pill{{display:inline-flex;padding:3px 9px;border-radius:999px;background:#e8eefc;color:var(--accent);font-size:12px;font-weight:650}}.accepted{{color:var(--ok)}}.quarantined,.review_required{{color:var(--warn)}}.blocked,.rolled_back{{color:var(--bad)}}.empty{{padding:32px;text-align:center;color:var(--muted)}}@media(max-width:760px){{.grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}header{{display:block}}}}
</style></head><body><main><header><div><h1>{title}</h1><div class="muted">Read-only local projection · synthetic-safe display</div></div><div class="muted" id="generated"></div></header>
<section class="grid" id="summary"></section><section class="table-wrap"><table><thead><tr><th>Batch</th><th>Source</th><th>State</th><th>Units</th><th>Messages</th><th>Attachments</th><th>Completed</th></tr></thead><tbody id="batches"></tbody></table></section></main>
<script>const batches={data};const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({{"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}}[c]));const count=(state)=>batches.filter(b=>b.state===state).length;document.getElementById('generated').textContent=new Date().toLocaleString();document.getElementById('summary').innerHTML=[['Batches',batches.length,''],['Accepted',count('accepted'),'accepted'],['Review / isolate',batches.filter(b=>['review_required','quarantined','blocked'].includes(b.state)).length,'review_required'],['Formal pages','Vault gated','']].map(x=>`<div class="card"><div class="muted">${x[0]}</div><div class="value ${{x[2]}}">${x[1]}</div></div>`).join('');document.getElementById('batches').innerHTML=batches.length?batches.map(b=>`<tr><td><code>${esc(b.batch_id)}</code></td><td>${esc(b.source)}</td><td class="${{esc(b.state)}}"><span class="pill">${{esc(b.state)}}</span></td><td>${{b.coverage?.units??0}}</td><td>${{b.coverage?.messages??0}}</td><td>${{b.coverage?.attachments??0}}</td><td>${{esc(b.completed_at||'—')}}</td></tr>`).join(''):'<tr><td colspan="7" class="empty">No batches recorded</td></tr>';</script></body></html>'''
    output = Path(args.output).expanduser().resolve() if args.output else project.artifacts / "batch-dashboard.html"
    atomic_write(output, page)
    print(json.dumps({"state": "accepted", "output": str(output), "batches": len(rows)}, ensure_ascii=False, indent=2))
    return 0


def dashboard(args: argparse.Namespace) -> int:
    """Build a self-contained dashboard without interpolating HTML as Python f-strings."""
    project = project_from(args)
    ledger = read_json(project.batches_path, {"batches": []})
    rows = ledger.get("batches", [])
    if args.batch_id:
        rows = [find_batch(project, args.batch_id)]
    data = json.dumps([redacted_record(row) for row in rows], ensure_ascii=False).replace("</", "<\\/")
    title = html.escape(args.title)
    page = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title><style>:root{--bg:#f5f7fb;--panel:#fff;--ink:#172033;--muted:#667085;--line:#e5e7eb;--accent:#3857d6;--ok:#087443;--warn:#a15c00;--bad:#b42318}@media(prefers-color-scheme:dark){:root{--bg:#111827;--panel:#182235;--ink:#edf2f7;--muted:#a8b3c2;--line:#334155;--accent:#9bb2ff}}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{max-width:1180px;margin:auto;padding:32px 20px}header{display:flex;justify-content:space-between;gap:16px;align-items:end;margin-bottom:24px}h1{margin:0;font-size:30px}.muted{color:var(--muted)}.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:20px}.card,.table-wrap{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px}.value{font-size:26px;font-weight:700;margin-top:6px}.table-wrap{overflow:auto;padding:0}table{border-collapse:collapse;width:100%}th,td{padding:13px 15px;text-align:left;border-bottom:1px solid var(--line);white-space:nowrap}th{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}.pill{display:inline-flex;padding:3px 9px;border-radius:999px;background:#e8eefc;color:var(--accent);font-size:12px;font-weight:650}.accepted{color:var(--ok)}.quarantined,.review_required{color:var(--warn)}.blocked,.rolled_back{color:var(--bad)}.empty{padding:32px;text-align:center;color:var(--muted)}@media(max-width:760px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}header{display:block}}</style></head><body><main><header><div><h1>__TITLE__</h1><div class="muted">Read-only local projection · synthetic-safe display</div></div><div class="muted" id="generated"></div></header><section class="grid" id="summary"></section><section class="table-wrap"><table><thead><tr><th>Batch</th><th>Source</th><th>State</th><th>Units</th><th>Messages</th><th>Attachments</th><th>Completed</th></tr></thead><tbody id="batches"></tbody></table></section></main><script>const batches=__DATA__;const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));const count=s=>batches.filter(b=>b.state===s).length;document.getElementById('generated').textContent=new Date().toLocaleString();document.getElementById('summary').innerHTML=[['Batches',batches.length,''],['Accepted',count('accepted'),'accepted'],['Review / isolate',batches.filter(b=>['review_required','quarantined','blocked'].includes(b.state)).length,'review_required'],['Formal pages','Vault gated','']].map(x=>'<div class="card"><div class="muted">'+x[0]+'</div><div class="value '+x[2]+'">'+x[1]+'</div></div>').join('');document.getElementById('batches').innerHTML=batches.length?batches.map(b=>'<tr><td><code>'+esc(b.batch_id)+'</code></td><td>'+esc(b.source)+'</td><td class="'+esc(b.state)+'"><span class="pill">'+esc(b.state)+'</span></td><td>'+(b.coverage?.units??0)+'</td><td>'+(b.coverage?.messages??0)+'</td><td>'+(b.coverage?.attachments??0)+'</td><td>'+esc(b.completed_at||'—')+'</td></tr>').join(''):'<tr><td colspan="7" class="empty">No batches recorded</td></tr>';</script></body></html>"""
    page = page.replace("__TITLE__", title).replace("__DATA__", data)
    output = Path(args.output).expanduser().resolve() if args.output else project.artifacts / "batch-dashboard.html"
    atomic_write(output, page)
    print(json.dumps({"state": "accepted", "output": str(output), "batches": len(rows)}, ensure_ascii=False, indent=2))
    return 0


def retry(args: argparse.Namespace) -> int:
    project = project_from(args)
    try:
        batch = find_batch(project, args.unit_id)
    except RunnerError:
        ledger = read_json(project.batches_path, {"batches": []})
        batch = next((row for row in ledger.get("batches", []) if args.unit_id in row.get("retryable_units", [])), None)
        if batch is None:
            raise RunnerError(f"unit_not_found:{args.unit_id}")
    batch.update({"state": "retry_queued", "retry_requested_at": now(project.tz)})
    save_batch(project, batch)
    print(json.dumps({"state": "retry_queued", "batch": batch}, ensure_ascii=False, indent=2))
    return 0


def validate(args: argparse.Namespace) -> int:
    project = project_from(args)
    batch = find_batch(project, args.batch_id)
    errors: list[str] = []
    if batch.get("state") == "accepted" and not (project.runs / args.batch_id / "commit-report.json").exists():
        errors.append("accepted_batch_missing_commit_report")
    if batch.get("state") not in STATES and batch.get("state") != "previewed":
        errors.append("unknown_batch_state")
    payload = {"state": "accepted" if not errors else "blocked", "batch_id": args.batch_id, "errors": errors, "formal_pages": len(list(project.wiki.rglob("*.md")))}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not errors else 2


def source_command(args: argparse.Namespace) -> int:
    project = project_from(args)
    registry = read_json(project.sources_path, {"schema": "topprismwiki-sources-v1", "sources": []})
    if args.source_command == "list":
        print(json.dumps({"state": "accepted", **registry}, ensure_ascii=False, indent=2))
        return 0
    if args.source_command in {"exclude", "readmit"} and not args.reason:
        raise RunnerError("reason_required")
    if args.source_command == "approve":
        registry.setdefault("sources", []).append({"id": args.id, "path": args.path, "approved": True, "sensitivity": args.sensitivity})
    else:
        registry.setdefault("events", []).append({"action": args.source_command, "path": args.path, "sha256": args.sha256, "reason": args.reason, "at": now(project.tz)})
    atomic_json(project.sources_path, registry)
    print(json.dumps({"state": "accepted", "registry": registry}, ensure_ascii=False, indent=2))
    return 0


def add_project_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--project", help="private Topprismwiki project root")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="command", required=True)
    for name in ("init",):
        action = sub.add_parser(name)
        add_project_argument(action)
        action.set_defaults(func=init_project)
    doctor_parser = sub.add_parser("doctor")
    add_project_argument(doctor_parser)
    doctor_parser.add_argument("--capability", choices=("all", "core", "obsidian", "wechat", "documents", "vision", "media"), default="all")
    doctor_parser.add_argument("--strict", action="store_true", help="require optional production gates selected by the command")
    doctor_parser.set_defaults(func=doctor)
    for name in ("preview", "update"):
        action = sub.add_parser(name)
        add_project_argument(action)
        action.add_argument("--source", choices=("all", "wechat", "documents"), default="all")
        action.add_argument("--batch-id")
        action.add_argument("--review")
        action.add_argument("--authorized", action="store_true")
        action.set_defaults(func=preview if name == "preview" else apply_update)
    query_parser = sub.add_parser("query")
    add_project_argument(query_parser)
    query_parser.add_argument("question")
    query_parser.add_argument("--limit", type=int, default=12)
    query_parser.set_defaults(func=query)
    context_parser = sub.add_parser("context")
    add_project_argument(context_parser)
    context_parser.add_argument("task")
    context_parser.add_argument("--budget", type=int, default=6000)
    context_parser.set_defaults(func=context)
    graph_parser = sub.add_parser("graph")
    add_project_argument(graph_parser)
    graph_parser.add_argument("entity", nargs="?")
    graph_parser.add_argument("--include-candidates", action="store_true")
    graph_parser.set_defaults(func=graph)
    status_parser = sub.add_parser("status")
    add_project_argument(status_parser)
    status_parser.add_argument("--source", choices=("all", "wechat", "documents"), default="all")
    status_parser.set_defaults(func=status)
    batch_parser = sub.add_parser("batch")
    add_project_argument(batch_parser)
    batch_sub = batch_parser.add_subparsers(dest="batch_command", required=True)
    batch_list = batch_sub.add_parser("list")
    add_project_argument(batch_list)
    batch_list.add_argument("--source", choices=("all", "wechat", "documents"), default="all")
    batch_list.add_argument("--status", choices=("all", *sorted(STATES)), default="all")
    batch_list.set_defaults(func=batch_command)
    batch_show = batch_sub.add_parser("show")
    add_project_argument(batch_show)
    batch_show.add_argument("batch_id")
    batch_show.set_defaults(func=batch_command)
    dashboard_parser = sub.add_parser("dashboard")
    add_project_argument(dashboard_parser)
    dashboard_sub = dashboard_parser.add_subparsers(dest="dashboard_command", required=True)
    dashboard_build = dashboard_sub.add_parser("build")
    add_project_argument(dashboard_build)
    dashboard_build.add_argument("--batch-id")
    dashboard_build.add_argument("--output")
    dashboard_build.add_argument("--title", default="Topprismwiki Batch Dashboard")
    dashboard_build.set_defaults(func=dashboard)
    retry_parser = sub.add_parser("retry")
    add_project_argument(retry_parser)
    retry_parser.add_argument("--unit-id", required=True)
    retry_parser.set_defaults(func=retry)
    validate_parser = sub.add_parser("validate")
    add_project_argument(validate_parser)
    validate_parser.add_argument("--batch-id", required=True)
    validate_parser.set_defaults(func=validate)
    source_parser = sub.add_parser("source")
    add_project_argument(source_parser)
    source_sub = source_parser.add_subparsers(dest="source_command", required=True)
    source_list = source_sub.add_parser("list")
    add_project_argument(source_list)
    source_list.set_defaults(func=source_command)
    approve = source_sub.add_parser("approve")
    add_project_argument(approve)
    approve.add_argument("--id", required=True)
    approve.add_argument("--path", required=True)
    approve.add_argument("--sensitivity", default="internal")
    approve.set_defaults(func=source_command)
    for name in ("exclude", "readmit"):
        action = source_sub.add_parser(name)
        add_project_argument(action)
        action.add_argument("--path")
        action.add_argument("--sha256")
        action.add_argument("--reason", required=True)
        action.set_defaults(func=source_command)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return int(args.func(args))
    except (RunnerError, OSError, ValueError) as error:
        print(json.dumps({"state": "blocked", "error": redact(str(error))}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
