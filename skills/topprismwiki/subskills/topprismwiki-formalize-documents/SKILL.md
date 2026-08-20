---
name: topprismwiki-formalize-documents
description: Process approved local Office, PDF, image, Markdown, and related documents by evidence, version family, and formal admission rules. Internal child module of $topprismwiki.
---

# Document formalization

Process only sources in the approved registry. Preserve originals and record
path, hash, modification time, version family, sensitivity, and page/section
anchors. Office uses `officecli`; PDF and presentation pages require visual
review; images require a local or explicitly approved vision adapter.

Document outcomes are `formal_source`, `catalog_only`,
`duplicate_or_superseded`, `quarantined`, `excluded`, and `blocked`. Fact
outcomes are `formalized`, `duplicate`, `conflicting`, `relation_candidate`,
`evidence_insufficient`, and `non_durable`.

Route visual pages to `vision-reviewer`, bulk text to `bulk-worker`, and
ambiguous entities or relationships to `adjudicator`. A filename, directory,
brand co-occurrence, or ordinary Wikilink is not relationship evidence.

See [document-contract.md](../../references/document-contract.md) before
creating a review package.
