# Product architecture

TopprismWiki presents one governed lifecycle to an AI agent while preserving
three separate operational layers.

~~~mermaid
flowchart LR
    S[Approved enterprise sources] --> A[Adapters]
    A --> E[Evidence Workspace]
    E --> H[Human and policy review]
    H --> P[Deterministic publication]
    P --> V[Formal Knowledge Vault]
    V --> X[Context and query projections]
    X --> G[Agent applications]
    E -. candidates and conflicts .-> X
~~~

## Source and adapter boundary

An adapter turns a private source into a documented evidence record. It keeps
the original outside the public repository, records a stable hash and provides
message, page, table or visual anchors. The public Runner does not pretend to
be a WeChat exporter, Office parser or vision service.

## Evidence Workspace

The Workspace stores source snapshots, evidence packages, review decisions,
conflicts, candidate relationships, processing state and rebuildable dashboard
artifacts. It may contain sensitive material in a private deployment, but it
must never be published with the public package.

## Formal Knowledge Vault

The Vault contains only accepted facts, canonical entities, decisions and typed
relationships. A deterministic committer checks source hashes, target paths,
review-package integrity and post-commit state before advancing a successful
batch.

## Interaction layer

Query, context, graph, status and dashboard commands are projections. They do
not bypass governance or directly mutate the formal Vault.
