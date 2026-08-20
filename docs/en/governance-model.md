# Governance model

TopprismWiki treats formal publication as a controlled state transition:

~~~text
source approval
  -> evidence extraction and hashing
  -> entity and relationship review
  -> reviewed decision package
  -> dry-run or preview
  -> authorized atomic commit
  -> post-commit validation
~~~

## Admission rules

A formal fact needs a source identity, evidence anchor, content hash, subject,
object or value, time or scope and an applicable review decision. A shared
group name, filename, co-occurrence or brand mention is not enough to establish
a customer, project, person or delivery relationship.

## State separation

- formalized: evidence passed and was published;
- duplicate: the same supported fact already exists;
- conflicting: supported statements coexist with scope and status;
- relation_candidate: useful lead without enough direct evidence;
- evidence_insufficient: the claim is held back;
- non_durable: the observation is not persistent business knowledge.

## Mutation boundary

Preview, query, context, graph, status and dashboard operations are read-only
with respect to the formal Vault. Update requires explicit authorization and a
review package. A failed atomic commit must not advance the relevant watermark.

## Privacy boundary

Raw evidence stays in the private Workspace. Public examples use synthetic
identities, paths and hashes. Credentials and model endpoints must never be
written to Markdown, logs, issues or generated projections.
