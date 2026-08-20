---
name: topprismwiki
description: Route governed company-knowledge workflows for preview, formal update, query, context, graph, batch status, and source governance. Use when a user asks to update or inspect a Topprismwiki knowledge base.
---

# Topprismwiki

Topprismwiki is a governed company-knowledge workflow. This package exposes
one entry skill; the files under `subskills/` are internal modules and must be
loaded only when the request matches their scope.

## Routing

- For approved chat or document updates, read the matching
  `subskills/topprismwiki-formalize-*/SKILL.md` file and use the deterministic
  runner in `scripts/`.
- For formal knowledge queries, read `subskills/topprismwiki-query/SKILL.md`.
- For bounded task context, read `subskills/topprismwiki-context/SKILL.md`.
- For formal or candidate relationships, read `subskills/topprismwiki-graph/SKILL.md`.
- For batches, watermarks, isolates, or health, read
  `subskills/topprismwiki-status/SKILL.md`.
- For source approval, exclusion, readmission, retry, or validation, read
  `subskills/topprismwiki-governance/SKILL.md`.

Do not present a Workspace candidate, raw message, or document mention as a
formal fact. Formal Vault changes require explicit update intent, a hash-bound
review package, a dry-run, an atomic commit, and post-commit validation. The
agent never edits the Vault directly outside the runner.

## Runtime

Run commands from the public package or an installed copy of this skill:

```bash
python3 scripts/topprismwiki.py doctor --capability all --project /path/to/wiki
python3 scripts/topprismwiki.py preview --source all --project /path/to/wiki
python3 scripts/topprismwiki.py update --source all --authorized --project /path/to/wiki
python3 scripts/topprismwiki.py query "project status" --project /path/to/wiki
python3 scripts/topprismwiki.py context "prepare a customer review" --budget 6000 --project /path/to/wiki
python3 scripts/topprismwiki.py graph "demo-project" --include-candidates --project /path/to/wiki
python3 scripts/topprismwiki.py batch list --project /path/to/wiki
python3 scripts/topprismwiki.py dashboard build --project /path/to/wiki
```

`preview`, `query`, `context`, `graph`, `status`, `batch`, `dashboard`, and
`validate` are read-only with respect to the formal Vault. `update` is the only
command that may commit reviewed facts, and it requires `--authorized`.

Read [references/architecture.md](references/architecture.md) for data
boundaries and [references/dependencies-and-routing.md](references/dependencies-and-routing.md)
before operating a source-specific workflow. The examples under `examples/`
are synthetic and must not be replaced with real company data in a public
repository.
