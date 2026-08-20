# TopprismWiki

## Enterprise Knowledge Governance Layer for Agentic AI

[![Python](https://img.shields.io/badge/python-3.11%2B-3776AB.svg)](https://www.python.org/)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF.svg)](.github/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-%24topprismwiki-6E56CF.svg)](skills/topprismwiki/SKILL.md)
[![Privacy](https://img.shields.io/badge/data-public%20examples%20only-0B7A75.svg)](docs/en/privacy.md)

TopprismWiki is an evidence-governed knowledge layer that turns approved
enterprise evidence into traceable formal knowledge for AI agents.

Traditional retrieval helps agents find information. TopprismWiki governs what
can become knowledge, why it is trusted, and how it may be published and
consumed.

It is implemented as an Agent Skill package and a dependency-free Python
reference runner. The long-term direction is an enterprise knowledge operating
layer; the public repository currently provides the governed contracts and
reference workflow needed to build toward that direction.

## Why TopprismWiki

Agentic systems do more than retrieve documents. They summarize, recommend,
update records, and take actions. That makes provenance and change control part
of the knowledge problem:

- Which source is approved for this decision?
- What evidence supports a fact or relationship?
- How should conflicting statements coexist?
- Who or what may publish a change?
- Can an agent distinguish formal knowledge from a candidate or an unresolved
  source?

TopprismWiki places a governed publication layer between enterprise sources and
agent-facing context:

~~~text
Enterprise evidence
        |
        v
Source adapters and evidence contracts
        |
        v
Review, entity and relationship governance
        |
        v
Deterministic formal publication
        |
        v
Trusted Knowledge Vault
        |
        v
Query, context and graph projections for AI agents
~~~

## What it is

TopprismWiki provides:

- evidence contracts for approved sources and adapter-produced records;
- source hashes, evidence anchors, review packages and conflict states;
- canonical entities and typed relationships with separate candidate overlays;
- review-gated, atomic publication into a formal Markdown Vault;
- bounded query, context, graph, batch and diagnostic projections;
- a single public entry Skill, $topprismwiki, with internal child modules.

TopprismWiki is not a vector database, a general-purpose RAG framework, an
automatic truth generator, or a bundled WeChat/Office/OCR connector. The public
runner deliberately separates built-in governance behavior from deployment-owned
adapters and model services.

## Enterprise Knowledge Lifecycle

~~~mermaid
flowchart TB
    S[Enterprise sources] --> A[Source adapters]
    A --> W[Evidence Workspace]
    W --> G[Review and governance]
    G --> C[Deterministic committer]
    C --> V[Trusted Knowledge Vault]
    V --> R[Query, context and graph]
    R --> AG[AI agents]
    W -. conflicts, candidates, status .-> R
~~~

The three-layer boundary is intentional:

| Layer | Role | Write rule |
| --- | --- | --- |
| Formal Vault | Approved facts, canonical entities, decisions and typed relationships | Only the deterministic committer writes |
| Evidence Workspace | Originals, snapshots, hashes, review packages, conflicts, candidates and ledgers | Mutable and rebuildable |
| Interaction projections | Query, context, graph, status, batch and dashboard views | Read-only projections |

Co-occurrence, group names, member lists, filenames and brand mentions do not
establish formal relationships by themselves.

## Core capabilities

| Capability | Public status |
| --- | --- |
| Project initialization, JSONL preview and batch ledger | Built-in |
| Review-gated atomic Markdown publication and rollback | Built-in |
| Formal query, bounded context and REL graph projection | Built-in |
| Read-only batch dashboard and diagnostics | Built-in |
| WeChat, Office, PDF, image and media source processing | Adapter-required |
| Per-source production watermarks and Obsidian post-commit validation | Not yet enforced by the public runner |

See the [capability matrix](skills/topprismwiki/references/capability-matrix.md)
for the complete boundary.

## 60-second synthetic demo

The public demo uses synthetic chat events only. It verifies the same governed
path without exposing private sources:

~~~bash
git clone https://github.com/topprismdata/topprismwiki.git
cd topprismwiki
python3 -m unittest discover -s skills/topprismwiki/tests -v
~~~

For the complete end-to-end path, follow the
[synthetic walkthrough](docs/en/synthetic-walkthrough.md). A clean run
currently demonstrates:

~~~text
2 processing units
11 input messages
1 formalized fact
1 evidence-insufficient unit
1 atomically committed formal page
accepted post-commit validation
~~~

Preview creates Workspace evidence and does not write the formal Vault.
Update requires an explicit authorization flag and a reviewed decision package.

## How it differs from common patterns

This is a comparison of representative architecture patterns, not a benchmark
or a claim about every product in a category.

| Concern | Document knowledge base | Typical RAG pipeline | Typical GraphRAG pipeline | TopprismWiki |
| --- | --- | --- | --- | --- |
| Primary focus | Store and read documents | Retrieve passages for generation | Retrieve and connect graph context | Govern what becomes formal, traceable knowledge |
| Source approval | Usually external to the store | Application-defined | Application-defined | Explicit source and admission contracts |
| Evidence anchors | Varies by implementation | Often passage-level | Often document/edge-level | Required for formal facts and operations |
| Relationship promotion | Usually manual or implicit | Usually outside retrieval | Often extraction-driven | Typed, evidence-backed, candidate-separated |
| Conflict handling | Often manual | Prompt/application responsibility | Graph/application responsibility | Explicit conflict and unresolved states |
| Publication control | Tool or process dependent | Pipeline dependent | Pipeline dependent | Review package, hash check and atomic commit |
| Agent context | Search or document access | Retrieved passages | Graph-plus-text context | Bounded formal facts, relationships and evidence gaps |

## Current evidence and evaluation

The current public package is validated as a governance reference workflow, not
as a production-scale knowledge quality benchmark.

- package validation covers eight nested Skill modules;
- the test suite covers authorization, preview isolation, atomic update,
  rollback, query, graph, retry and diagnostic paths;
- the public safety scan rejects private paths, credentials and unsanitized
  source examples;
- the synthetic walkthrough verifies preview, reviewed update, validation,
  query, graph and dashboard behavior.

The [evaluation guide](docs/en/evaluation.md) defines the next measurement
layer: traceability coverage, admission precision, conflict handling,
idempotence, rollback correctness and, later, labeled knowledge-quality and
agent-task benchmarks. No accuracy, hallucination-reduction or deployment
improvement claim is made by this repository today.

## Quick start

Read [Getting started](docs/en/getting-started.md) and run the synthetic
walkthrough before connecting real sources.

~~~bash
python3 skills/topprismwiki/scripts/topprismwiki.py init --project /path/to/my-wiki
python3 skills/topprismwiki/scripts/topprismwiki.py doctor --capability core --project /path/to/my-wiki
python3 skills/topprismwiki/scripts/topprismwiki.py preview --source all --project /path/to/my-wiki
python3 skills/topprismwiki/scripts/topprismwiki.py status --project /path/to/my-wiki
python3 skills/topprismwiki/scripts/topprismwiki.py dashboard build --project /path/to/my-wiki
~~~

If a command returns blocked or a non-zero exit code, run diagnose first:

~~~bash
python3 skills/topprismwiki/scripts/topprismwiki.py diagnose --project /path/to/my-wiki
~~~

Only an explicitly authorized update with a reviewed decision package may write
the formal Vault:

~~~bash
python3 skills/topprismwiki/scripts/topprismwiki.py update \
  --source documents --authorized --project /path/to/my-wiki
~~~

## Documentation

- [Concepts](docs/en/concepts.md)
- [Product architecture](docs/en/product-architecture.md)
- [Governance model](docs/en/governance-model.md)
- [Adapter contracts](docs/en/adapters.md)
- [Dependencies and agent routing](skills/topprismwiki/references/dependencies-and-routing.md)
- [Operations and state semantics](docs/en/operations.md)
- [Troubleshooting](docs/en/troubleshooting.md)
- [Privacy contract](docs/en/privacy.md)
- [Evaluation](docs/en/evaluation.md)
- [Roadmap](ROADMAP.md)
- [中文文档](README.zh-CN.md)

## Privacy and contribution boundaries

The repository contains synthetic contacts, chats, customers, projects,
filenames, hashes, paths and timestamps only. Real messages, business
documents, Vaults, Workspaces, ledgers, model endpoints and credentials must
remain outside Git.

Run the public safety scanner before release:

~~~bash
python3 skills/topprismwiki/scripts/check_public_safety.py .
~~~

See [SECURITY.md](SECURITY.md) and [CONTRIBUTING.md](CONTRIBUTING.md) before
opening an issue or pull request.

## License

Apache-2.0. See [LICENSE](LICENSE).
