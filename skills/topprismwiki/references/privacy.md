# Public release privacy contract

The repository contains no real chat export, business document, Vault page,
state ledger, local endpoint, API key, or personal path. Examples use aliases
such as `demo_contact_001`, `demo_project_group_001`, and
`/path/to/company-documents`.

Runtime data belongs in the configured private project and is excluded by
`.gitignore`. Reports redact credentials, bearer tokens, absolute user paths,
raw session identifiers, and attachment contents unless the operator explicitly
requests a private local report.

Before a public commit, scan both the worktree and Git history. Do not encode a
real denylist in the public repository; pass private patterns to the scanner
from an external temporary file.
