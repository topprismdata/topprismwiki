---
name: topprismwiki-status
description: Inspect watermarks, batches, document families, isolates, candidates, and formal-store health. Internal child module of $topprismwiki.
---

# Status and batch dashboard

Use the status ledger and generated projections. Distinguish `accepted`,
`no_change`, `quarantined`, `blocked`, `partial`, and `rolled_back`. A failed
or quarantined unit does not advance its watermark.

```bash
python3 scripts/topprismwiki.py status --project /path/to/wiki
python3 scripts/topprismwiki.py batch list --project /path/to/wiki
python3 scripts/topprismwiki.py dashboard build --project /path/to/wiki
```

The HTML dashboard is a read-only local projection. It may expose only
configured aliases and relative paths.
