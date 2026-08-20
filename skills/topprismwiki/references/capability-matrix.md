# Capability matrix

This matrix is the source of truth for what a clean public checkout can do.
The labels are intentionally conservative:

- `built-in`: implemented by `scripts/topprismwiki.py` and covered by tests.
- `adapter-required`: the public package defines the input contract, but the
  source adapter or local model is supplied by the deployment owner.
- `not-yet-supported`: a design goal or contract detail that the public runner
  does not currently enforce. It must not appear as a ready-to-run command.

| Capability | Level | What is verified | What is not claimed |
| --- | --- | --- | --- |
| Project initialization | `built-in` | Creates private control, Workspace, Vault and state directories. | It does not import private data. |
| JSONL preview | `built-in` | Reads redacted event records and creates a coverage batch. | It does not extract WeChat or Office files. |
| Reviewed Vault update | `built-in` | Validates a review package, writes Markdown atomically and records a commit report. | It does not perform domain-level entity adjudication. |
| Rollback | `built-in` | Restores files when the atomic update fails. | It does not recover a damaged external source. |
| Query | `built-in` | Searches formal Markdown pages and returns page, line, score and hash. | `--as-of`, semantic search and Workspace fallback are not implemented. |
| Context | `built-in` | Produces a formal-page projection with a configured character limit. | The limit is not a token counter. |
| Formal REL graph | `built-in` | Parses the documented Markdown REL form. | Reverse-edge validation and automatic cross-linking are not implemented. |
| Candidate graph overlay | `adapter-required` | Reads a private `candidates.json` projection when present. | Co-occurrence is never promoted automatically. |
| Batch and dashboard | `built-in` | Stores batch summaries and creates a local read-only HTML projection. | The dashboard is not a control plane. |
| Source approval ledger | `built-in` | Records approval, exclusion and readmission events. | Full production precedence enforcement remains a deployment responsibility. |
| WeChat export and filtering | `adapter-required` | Accepts adapter-produced JSONL with session and message evidence fields. | The public runner does not connect to WeChat or enforce interval filtering. |
| Office extraction | `adapter-required` | Documents `officecli` output requirements. | `officecli` is not bundled. |
| PDF/PPT/image review | `adapter-required` | Documents page rendering and local vision requirements. | The public runner does not call a vision endpoint. |
| Audio/video transcription | `adapter-required` | Documents `ffmpeg` and ASR evidence requirements. | ASR is not bundled. |
| Per-unit source watermarks | `not-yet-supported` | Batch summaries expose whether the public update advanced a watermark. | A production adapter must own durable per-session watermarks. |
| Obsidian post-commit validation | `not-yet-supported` | The configuration can declare it as a production gate. | The public runner does not invoke Obsidian CLI. |

When a capability changes, update this file, the matching bilingual guide and
the tests in the same change.
