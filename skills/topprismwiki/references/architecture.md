# Architecture and data boundary

Topprismwiki has three layers:

| Layer | Contents | Mutation rule |
| --- | --- | --- |
| Formal Vault | Approved facts, canonical entities, decisions, and typed `REL` edges | Only the deterministic committer may write it |
| Workspace | Originals, snapshots, hashes, evidence, review packages, conflicts, candidates, ledgers, and projections | Mutable and rebuildable |
| Interaction | Query, context, graph, status, batch, and dashboard views | Read-only projections |

The public runner is deliberately adapter-based. Source adapters may produce
evidence packages, but they do not write the formal Vault. A formal operation
must include source hash, evidence location, entity scope, fact state, and the
review package hash. The committer verifies the current Vault tree before
applying an atomic transaction and runs post-commit validation before advancing
watermarks.

The public examples are synthetic. A real deployment must keep actual raw
evidence outside Git and configure a private source registry.

See [capability-matrix.md](capability-matrix.md) for the boundary between the
reference Runner, external adapters and not-yet-supported production gates.
When a command fails, use the stable error catalog and `diagnose`; do not repair
state by editing Vault pages or ledgers manually.
