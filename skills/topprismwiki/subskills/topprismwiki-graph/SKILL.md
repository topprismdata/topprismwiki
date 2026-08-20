---
name: topprismwiki-graph
description: Inspect formal REL edges and an explicitly separate candidate relationship overlay. Internal child module of $topprismwiki.
---

# Graph

Formal `REL` edges are the primary graph and must be supported by typed direct
evidence. Candidate edges are a separate Workspace projection with
`state: candidate`; they never affect formal graph metrics and never trigger
automatic cross-links.

```bash
python3 scripts/topprismwiki.py graph "entity" --include-candidates --project /path/to/wiki
```
