# Troubleshooting

Preserve the run before editing a ledger or formal page:

```bash
python3 scripts/topprismwiki.py doctor --capability core --strict \
  --project /path/to/wiki
python3 scripts/topprismwiki.py status --project /path/to/wiki
python3 scripts/topprismwiki.py diagnose --project /path/to/wiki
```

Search the returned `code` in this guide or pass it to
`diagnose --error-code`. Do not upload raw messages, documents, Vault pages,
credentials or complete user paths to GitHub.

## Environment

### <a id="python"></a>Python version

`CORE_PYTHON_MISSING` means the interpreter is older than 3.11. Check
`python3 --version` and ensure the command uses the intended interpreter.

### <a id="obsidian"></a>Obsidian CLI

`OBSIDIAN_CLI_MISSING` matters only when the deployment selected Obsidian as a
production gate. The public Runner does not install or invoke it.

### <a id="wechat"></a>WeChat adapter

`WECHAT_ADAPTER_MISSING` means the configured executable is not on PATH. Install
a compatible private adapter or produce JSONL according to the adapter contract.

### <a id="office"></a>Office extractor

`OFFICECLI_MISSING` means the configured extractor is unavailable. Quarantine the
unit or provide a compatible evidence package; do not infer facts from filenames.

### <a id="vision"></a>Vision configuration

`VISION_CONFIGURATION_MISSING` means no image-capable endpoint is configured.
The model must support OCR, layout, tables, charts and diagrams.

### <a id="media"></a>Media tools

`FFMPEG_MISSING` means media preprocessing is unavailable. Install ffmpeg or keep
the affected media quarantined.

## Input and review

### <a id="invalid-json"></a>Invalid JSON

`INVALID_JSON` means an input, configuration, ledger or review JSON file cannot be
parsed. Validate UTF-8 JSON/JSONL and rerun the same command.

### <a id="authorization-required"></a>Authorization required

`EXPLICIT_UPDATE_AUTHORIZATION_REQUIRED` means update was run without
`--authorized`. Preview and review first; add the flag only for an explicitly
authorized formal write.

### <a id="review-file-missing"></a>Review file missing

`REVIEW_FILE_MISSING` means the expected `review.json` is absent. Copy the review
template into the same batch run directory, complete the evidence and retry.

### <a id="review-schema"></a>Review schema

`REVIEW_FACTS_MUST_BE_ARRAY`, `INVALID_TARGET` and `INCOMPLETE_FACT` indicate a
malformed review package. Compare it with `examples/review.json.example`.

### <a id="evidence-hash"></a>Evidence hash

`MISSING_SOURCE_SHA256` means the evidence lacks a 64-hex SHA-256. Recalculate
from the unchanged source snapshot; never type a placeholder for real data.

## Batches and governance

### <a id="batch-not-found"></a>Batch not found

`BATCH_NOT_FOUND` means the ID is absent from the private ledger. Run `batch list`
and copy the exact ID.

### <a id="unit-not-found"></a>Unit not found

`UNIT_NOT_FOUND` means the ID is neither a batch nor a retryable unit. Inspect
`batch show` and the adapter output.

### <a id="commit-report-missing"></a>Commit report missing

`ACCEPTED_BATCH_MISSING_COMMIT_REPORT` is a stop condition. Preserve the run
directory, run `diagnose`, and obtain a manual decision before repairing state.

### <a id="unknown-state"></a>Unknown state

`UNKNOWN_BATCH_STATE` means the ledger contains an undocumented state. Do not edit
it directly; submit a redacted diagnosis.

### <a id="governance-reason"></a>Governance reason

`REASON_REQUIRED` means an exclusion or readmission event has no audit reason.
Provide a concise non-sensitive reason.

## Still blocked

```bash
python3 scripts/topprismwiki.py diagnose \
  --batch-id <batch-id> --output /tmp/topprismwiki-diagnosis.json \
  --project /path/to/wiki
```

Review the redaction, then use the GitHub Issue template. Security incidents must
follow `SECURITY.md`. Unknown failures use `UNKNOWN_ERROR` and should include a
minimal reproduction.

<a id="unknown-error"></a>
