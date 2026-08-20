# Production setup

The production flow is:

```text
private adapter → hashed evidence → preview → review package
→ authorized update → validate → status/dashboard
```

The public package does not read real WeChat, Office files or model services.

## Isolation and privacy

- Keep the checkout limited to code, documentation and synthetic examples.
- Keep originals, Workspace, Vault, source registrations and model settings in
  a separate private project.
- Preserve original bytes, paths, modification times and hashes.
- Formal queries default to `vault/wiki/`; Workspace material must be labelled.
- Never commit credentials, raw messages, private documents or unrestricted
  endpoint configuration.

## Environment checks

```bash
python3 skills/topprismwiki/scripts/topprismwiki.py doctor \
  --capability all --project /path/to/private-wiki
```

Optional checks may be absent when that source is not in use. Use `--strict` for
the capability required by a production run.

The configured `obsidian_cli_required_for_apply` flag is a deployment gate; the
public Runner does not automatically invoke Obsidian CLI or claim post-commit
Obsidian validation.

## Governance and visual review

Source approval, exclusion and readmission require explicit user instructions.
The public Runner records governance events; full source-precedence enforcement
belongs to the deployment governance layer.

Images, PDF and PPT pages require a local or explicitly approved model with OCR,
layout, table, chart and diagram understanding. OCR-only output is insufficient.
Cloud endpoints require a separate data-egress decision.

On failure, quarantine the affected unit, run `diagnose`, and preserve the run
directory. Do not edit `batches.json` or formal Vault pages by hand.
