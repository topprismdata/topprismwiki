# Evaluation guide

The current package demonstrates governance workflow correctness. It does not
claim production-scale knowledge accuracy or agent performance.

## Current reproducible checks

- package validation discovers and validates eight nested Skill modules;
- unit tests cover explicit authorization, preview isolation, atomic update,
  rollback, query, graph, retry and diagnostics;
- public safety scanning checks for credentials, private paths and unsanitized
  source examples;
- the synthetic walkthrough verifies preview, reviewed update, validation,
  query, graph and dashboard projections.

## Governance metrics

The next labeled evaluation set should measure:

- traceability coverage: formal facts with valid source and location anchors;
- admission precision: accepted facts that satisfy the written contract;
- duplicate detection precision and recall;
- conflict detection and resolution auditability;
- relationship precision, with candidate edges excluded from formal metrics;
- idempotence: repeated input produces zero additional formal changes;
- rollback correctness: failed commits leave the formal Vault unchanged.

## Agent-facing metrics

After a stable labeled knowledge set exists, evaluate bounded context retrieval,
evidence citation completeness, answer support and task-level decision quality.
Do not report hallucination reduction, customer impact or deployment reliability
until the dataset, baseline, environment and repeatable procedure are checked
into the repository.
