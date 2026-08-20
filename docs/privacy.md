# Public repository privacy checklist

This repository is a reusable template, not a data snapshot. Before publishing
a clone:

- Replace every real path, person, group, customer, project, document name,
  hash, endpoint, and timestamp with synthetic values.
- Keep raw exports, Vault pages, state ledgers, review packages, screenshots,
  and model credentials outside Git.
- Do not place real denylist terms in the repository or its tests. Supply them
  to a local scanner through a temporary file.
- Run the public safety scanner on the worktree and Git history.
- Review generated HTML and screenshots manually for hidden metadata and
  embedded source text.

The runtime defaults to masked aliases and relative paths in projections. A
private deployment may configure local reporting separately, but its private
configuration must remain outside the public package.
