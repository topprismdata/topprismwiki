# Privacy and public release

The public repository may contain only synthetic contacts, sessions, customers,
projects, files, hashes, paths and timestamps. Real exports, business documents,
Vault, Workspace, ledgers, model endpoints and credentials belong in a private
project and are excluded by `.gitignore`.

- Keep raw evidence in private Workspace and write only reviewed derived facts
  to the formal Vault.
- Never place keys, tokens, passwords, Authorization headers or raw model output
  in Markdown, logs, dashboards, diagnosis packages or Issues.
- Send only the minimum approved evidence to an external model; local models are
  the default.
- GitHub Issues may contain only versions, error codes, synthetic reproductions
  and redacted `diagnose` output.
- Follow `SECURITY.md` privately for security reports.

Run the public safety scanner before release:

```bash
python3 skills/topprismwiki/scripts/check_public_safety.py .
```
