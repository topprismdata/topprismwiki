---
name: topprismwiki-query
description: Query formal Topprismwiki facts with evidence anchors, time bounds, and explicit conflict labels. Internal child module of $topprismwiki.
---

# Query

Use the formal Vault as the default fact layer. Return the page, source time,
evidence location, state, and page hash for important claims. Use Workspace
only when the user requests audit or the formal layer is insufficient; label
those results as raw, candidate, conflicting, or not formalized.

Do not merge candidate evidence into formal facts. Do not apply latest-wins to
conflicting statements. Use:

```bash
python3 scripts/topprismwiki.py query "question" --project /path/to/wiki
```
