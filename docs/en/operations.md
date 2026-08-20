# Commands and operations

Use an explicit private project root in production. If `--project` is omitted,
the Runner uses `TOPPRISMWIKI_PROJECT` or the current directory.

| Command | Purpose | Writes formal Vault |
| --- | --- | --- |
| `init` | Create the project skeleton | No |
| `doctor` | Check tools and configuration | No |
| `preview` | Read JSONL and create a coverage batch | No |
| `update` | Validate review and write Markdown atomically | Yes, with `--authorized` |
| `query` | Search formal Markdown | No |
| `context` | Create a formal-page projection | No; writes an artifact |
| `graph` | Show formal REL and candidate overlay | No |
| `status` | Show batch and formal-page summary | No |
| `batch list/show` | Inspect batches | No |
| `dashboard build` | Create a redacted static HTML view | No; writes an artifact |
| `retry` | Queue a unit for retry | No Vault write; updates ledger |
| `validate` | Validate a batch | No |
| `source approve/exclude/readmit` | Record source governance | No Vault write; requires explicit instruction |
| `diagnose` | Produce a redacted diagnosis | No unless `--output` is used |

Recommended gate sequence:

```bash
python3 scripts/topprismwiki.py preview --source all --project /path/to/wiki
python3 scripts/topprismwiki.py batch list --project /path/to/wiki
python3 scripts/topprismwiki.py update --batch-id <batch-id> \
  --authorized --project /path/to/wiki
python3 scripts/topprismwiki.py validate --batch-id <batch-id> \
  --project /path/to/wiki
```

Exit code `0` means the command completed, including `no_change`. Exit code `2`
means a gate, review, validation or runtime error needs attention. Use the
returned `code` and `diagnose` for any other non-zero result.
