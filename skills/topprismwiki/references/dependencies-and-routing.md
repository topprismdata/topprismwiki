# Dependencies and model routing

## Capability matrix

| Capability | Required adapter/tool | Model requirement | Missing dependency result |
| --- | --- | --- | --- |
| Core query/status | Python 3.11+ and a configured project | Structured tool use is helpful but not required by the CLI | Core read-only commands may run |
| Formal Vault validation | Obsidian + Obsidian CLI | No model; deterministic parser and validation | Production validation is blocked |
| WeChat | `wechat-cli` or compatible export adapter | Text extraction plus conservative entity reasoning | WeChat unit is blocked |
| Office | `officecli` | Text/structure extraction | Office attachment is quarantined |
| PDF/PPT/image | `pdftoppm` and an image-capable model | OCR plus layout, table, chart, and flow understanding | Visual evidence is quarantined |
| Audio/video | `ffmpeg` and an ASR adapter | Chinese-capable speech recognition | Media attachment is quarantined |

The default public configuration is local-first. Cloud model endpoints require
an explicit data-egress decision by the deployment owner and must never receive
credentials or unrestricted raw Workspace directories.

## Role routing

1. `orchestrator` freezes scope, checks authorization, and creates a batch.
2. `text-extractor` handles ordinary text and structured evidence.
3. `vision-reviewer` handles visual pages and OCR.
4. `bulk-worker` handles low-risk batches with no formal-write permission.
5. `adjudicator` handles identity, namespace, conflict, and relationship review.
6. `governance-reviewer` checks coverage and commit eligibility.
7. `committer` performs the deterministic dry-run, atomic write, rollback, and
   post-commit validation.

The same model may fill multiple roles sequentially, but role separation must
remain visible in the artifacts and permissions.
