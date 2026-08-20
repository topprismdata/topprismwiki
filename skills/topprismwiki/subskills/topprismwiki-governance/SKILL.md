---
name: topprismwiki-governance
description: Manage explicit source approval, exclusion, readmission, retry, and batch validation for Topprismwiki. Internal child module of $topprismwiki.
---

# Governance

Source approval and readmission require an explicit user instruction. Keep all
governance records in Workspace. Apply exclusion precedence as:

1. explicit readmission;
2. permanent SHA-256 denial;
3. scoped path or version-family rule;
4. approved source registry.

Missing originals preserve historical formal knowledge and are marked
`source_unavailable`; they are not silently deleted. Use `retry` only for a
specific failed or isolated unit and `validate` for read-only audit.
