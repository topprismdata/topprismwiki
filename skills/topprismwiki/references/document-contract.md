# Document admission contract

Each document must be in an approved source registry, preserve its original,
have a stable hash and modification time, be reliably readable, have known
nature/status/scope/sensitivity, and expose a page, section, table, or visual
anchor.

Evaluate source integrity, document status, durable business value, novelty,
temporal validity, entity identity, relationship evidence, and sensitive-data
handling independently as `pass`, `needs_review`, `fail`, or
`not_applicable`. Do not calculate a weighted total.

Conflict statements coexist with scope and status labels until explicitly
resolved. Co-occurrence is a candidate relationship only. Credentials never
enter Markdown, logs, reports, or query output.

This is the admission contract for a production adapter and review process. The
public Runner does not independently render Office/PDF/PPT files or enforce all
document-level gates; those units remain `adapter-required` until the capability
matrix says otherwise.
