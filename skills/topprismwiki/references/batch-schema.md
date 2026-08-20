# Batch and dashboard schema

The runner stores a rebuildable `workspace/state/batches.json`. A batch summary
contains:

```json
{
  "batch_id": "demo-batch-001",
  "source": "wechat",
  "mode": "preview",
  "state": "previewed",
  "started_at": "2026-01-01T09:00:00+08:00",
  "completed_at": "2026-01-01T09:01:00+08:00",
  "coverage": {"units": 3, "messages": 18, "attachments": 2},
  "outcomes": {"formalized": 4, "duplicate": 2, "quarantined": 1},
  "watermark_advanced": false,
  "retryable_units": ["demo-unit-003"]
}
```

The dashboard may display these aggregates and aliases. It must not display raw
message text, secrets, or unredacted paths. Dashboard actions only copy a CLI
command; state changes still require the governed runner.

The public Runner records batch-level state. An adapter may keep a separate
private per-unit watermark ledger, but that ledger is not created or validated by
the reference implementation. Use `diagnose --batch-id <id>` when a stored state
and its run artifacts disagree.
