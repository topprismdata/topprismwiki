# WeChat evidence contract

Each message record must retain a session alias, sender alias, message time,
message ID, raw snapshot SHA-256, and classification. Valid message states are
`formalized`, `duplicate`, `non_business`, and `evidence_insufficient`.

Each attachment must retain a message ID, file SHA-256, extractor, attribution
check, and one of `processed`, `quarantined`, or `failed`.

The closed interval is interpreted in the configured timezone. Failed or
quarantined units do not advance watermarks. Group names, member lists,
filenames, and one-off brand mentions are never sufficient evidence for a
customer, project, delivery, adoption, or person relationship.

The source adapter owns approved-session lookup, closed-interval filtering and
durable per-session watermarks. The public Runner consumes the resulting JSONL
records and reports their supplied coverage; it does not connect to WeChat or
verify the adapter's filtering independently.
