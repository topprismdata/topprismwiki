# Adapter contracts

The public package does not ship a WeChat exporter, `officecli`, a vision
server, or an ASR implementation. An adapter is a private or third-party
component that produces evidence records for the public runner.

## Common rules

- Never send credentials or unrestricted raw Workspace paths to a model.
- Preserve the original source outside Git and calculate SHA-256 before and
  after extraction.
- Use stable aliases for sessions, people, files, customers and projects in
  public-facing reports.
- A non-zero adapter exit code blocks the affected unit; it does not advance a
  watermark.
- Every record must be independently traceable to a source hash and location.

## WeChat adapter

Write UTF-8 JSONL to the private project's `workspace/inbox/wechat/` directory.
Each line represents one approved session or processing unit:

```json
{
  "unit_id": "private-session-unit",
  "session_alias": "approved-session-alias",
  "interval": {
    "start": "2026-01-01T00:00:00+08:00",
    "end": "2026-01-02T00:00:00+08:00",
    "timezone": "Asia/Shanghai",
    "closed": true
  },
  "messages": 12,
  "attachments": 2,
  "classification": "formalized",
  "state": "processed",
  "source_sha256": "64-hex-source-snapshot-hash"
}
```

The adapter owns approved-session lookup, time filtering, message identity,
attachment attribution and durable watermarks. The public Runner counts and
records the supplied units; it does not connect to WeChat or independently
verify that the interval was filtered.

## Office and visual adapters

`officecli` or a compatible extractor must preserve the original file, file
hash, version-family identifier and page/section/table anchor. PDF, PPT and
image units require a visual model capable of OCR plus layout, table, chart and
diagram understanding. OCR-only output is insufficient for formal admission.

## Media adapters

Use `ffmpeg` for deterministic preprocessing and a Chinese-capable ASR model
for speech. Store timestamps, media hash, model identity and confidence in the
private evidence package. Unmatched or unintelligible media remains
`quarantined`.
