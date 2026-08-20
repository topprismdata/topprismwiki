# Core concepts

TopprismWiki separates evidence, formal knowledge and agent-facing projections.
This keeps a useful lead from becoming a company fact before it has the required
authority and evidence.

## Evidence

Evidence is an immutable source observation with a source identity, content
hash, time, location anchor and processing status. Adapter output is evidence
input; it is not formal knowledge by itself.

## Formal knowledge

Formal knowledge is a durable fact, decision, entity or typed relationship that
passed the applicable source, evidence, entity and authorization gates. It is
published to the formal Vault through the deterministic committer.

## Candidates and conflicts

Candidate relationships, unresolved entities and conflicting statements remain
in the Workspace. They may be shown in a clearly labeled overlay or review
package, but they do not count as formal relationships.

## Agent context

Agent context is a bounded projection of formal knowledge, evidence anchors,
time and known gaps. It is not a dump of every source document and does not
silently promote Workspace candidates.

## Built-in and deployment-owned behavior

The public Runner implements the governance reference path. Source extraction,
OCR, transcription, entity adjudication and production validation may require
deployment-owned adapters or services. The capability matrix is the source of
truth for these boundaries.
