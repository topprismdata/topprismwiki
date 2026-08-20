from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]
RUNNER = ROOT / "scripts" / "topprismwiki.py"
SCANNER = ROOT / "scripts" / "check_public_safety.py"


def run_cli(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(RUNNER), *args, "--project", str(cwd)], text=True, capture_output=True, check=False)


class RunnerTests(unittest.TestCase):
    def test_init_status_and_dashboard_are_readable(self):
        with tempfile.TemporaryDirectory() as raw:
            project = Path(raw)
            result = run_cli("init", cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            result = run_cli("status", cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["batches"], 0)
            result = run_cli("dashboard", "build", cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            dashboard = project / "workspace/artifacts/batch-dashboard.html"
            self.assertTrue(dashboard.is_file())
            html = dashboard.read_text(encoding="utf-8")
            self.assertIn("Read-only local projection", html)
            self.assertNotIn("__DATA__", html)
            self.assertNotIn("/" + "Users/", html)

    def test_preview_records_synthetic_units_without_vault_write(self):
        with tempfile.TemporaryDirectory() as raw:
            project = Path(raw)
            run_cli("init", cwd=project)
            inbox = project / "workspace/inbox/wechat"
            inbox.mkdir(parents=True)
            (inbox / "events.jsonl").write_text(
                '{"unit_id":"demo-001","messages":2,"classification":"formalized","state":"processed"}\n'
                '{"unit_id":"demo-002","messages":1,"classification":"evidence_insufficient","state":"quarantined"}\n',
                encoding="utf-8",
            )
            result = run_cli("preview", "--source", "wechat", cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["batch"]["coverage"]["units"], 2)
            self.assertFalse(list((project / "vault/wiki").rglob("*.md")))

    def test_update_requires_authorization_and_review(self):
        with tempfile.TemporaryDirectory() as raw:
            project = Path(raw)
            run_cli("init", cwd=project)
            result = run_cli("update", "--source", "documents", cwd=project)
            self.assertEqual(result.returncode, 2)
            self.assertIn("explicit_update_authorization_required", result.stdout)

    def test_query_and_graph_are_read_only(self):
        with tempfile.TemporaryDirectory() as raw:
            project = Path(raw)
            run_cli("init", cwd=project)
            page = project / "vault/wiki/demo-project.md"
            page.parent.mkdir(parents=True, exist_ok=True)
            page.write_text("# Demo project\n\n- [[demo-product]] · uses_product\n- Status: active\n", encoding="utf-8")
            result = run_cli("query", "active", cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["results"][0]["state"], "formal")
            result = run_cli("graph", "demo-project", cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["formal_edges"][0]["relation"], "uses_product")

    def test_reviewed_update_is_atomic_and_validatable(self):
        with tempfile.TemporaryDirectory() as raw:
            project = Path(raw)
            run_cli("init", cwd=project)
            inbox = project / "workspace/inbox/documents"
            inbox.mkdir(parents=True)
            (inbox / "events.jsonl").write_text('{"unit_id":"demo-family-001","classification":"formalized","state":"processed"}\n', encoding="utf-8")
            preview = json.loads(run_cli("preview", "--source", "documents", cwd=project).stdout)
            batch_id = preview["batch"]["batch_id"]
            review = project / "workspace/runs" / batch_id / "review.json"
            review.write_text(json.dumps({"facts": [{"status": "formalized", "target": "projects/demo.md", "content": "# Demo\n", "evidence": {"source_sha256": "0" * 64, "location": "page 1"}}]}, ensure_ascii=False), encoding="utf-8")
            result = run_cli("update", "--batch-id", batch_id, "--authorized", cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((project / "vault/wiki/projects/demo.md").is_file())
            result = run_cli("validate", "--batch-id", batch_id, cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_retry_accepts_unit_id(self):
        with tempfile.TemporaryDirectory() as raw:
            project = Path(raw)
            run_cli("init", cwd=project)
            inbox = project / "workspace/inbox/wechat"
            inbox.mkdir(parents=True)
            (inbox / "events.jsonl").write_text('{"unit_id":"demo-retry-unit","classification":"evidence_insufficient","state":"quarantined"}\n', encoding="utf-8")
            preview = json.loads(run_cli("preview", "--source", "wechat", cwd=project).stdout)
            result = run_cli("retry", "--unit-id", "demo-retry-unit", cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["state"], "retry_queued")

    def test_public_safety_scan_passes_package(self):
        result = subprocess.run([sys.executable, str(SCANNER), str(REPO)], text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
