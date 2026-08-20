---
name: topprismwiki-context
description: Build a bounded, evidence-traceable task context from formal Topprismwiki facts and relationships. Internal child module of $topprismwiki.
---

# Context

Create a Workspace projection containing only task-relevant facts, decisions,
timeline, formal relationships, conflicts, and evidence gaps. Do not dump raw
documents or expose secrets. Enforce the token budget and state when content
was truncated.

```bash
python3 scripts/topprismwiki.py context "task" --budget 6000 --project /path/to/wiki
```
