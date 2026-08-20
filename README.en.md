# Topprismwiki

Topprismwiki is a governed company-knowledge skill package for source
approval, evidence, entities, relationships, batches, watermarks, conflicts,
and transactional formalization.

Only `$topprismwiki` is exposed as the public entry skill. WeChat, documents,
query, context, graph, status, and governance are nested child modules under
that package and are not installed as peer skills.

## Quick start

Follow the complete [getting started guide](docs/en/getting-started.md) and run the [synthetic walkthrough](docs/en/synthetic-walkthrough.md) before connecting real sources.

```bash
python3 skills/topprismwiki/scripts/topprismwiki.py init --project /path/to/my-wiki
python3 skills/topprismwiki/scripts/topprismwiki.py doctor --capability core --project /path/to/my-wiki
python3 skills/topprismwiki/scripts/topprismwiki.py preview --source all --project /path/to/my-wiki
python3 skills/topprismwiki/scripts/topprismwiki.py dashboard build --project /path/to/my-wiki
```

If a command returns `blocked` or a non-zero exit code, run:

```bash
python3 skills/topprismwiki/scripts/topprismwiki.py diagnose --project /path/to/my-wiki
```

Then use the [troubleshooting guide](docs/en/troubleshooting.md). Full command and state semantics are in [operations](docs/en/operations.md).

Only an explicitly authorized update with a reviewed decision package may write
the formal Vault. Raw evidence, conflicts, candidates, and ledgers stay in the
private Workspace. Co-occurrence, group names, member lists, and filenames do
not establish formal relationships.

See the Chinese guide in [README.md](README.md), the [architecture](skills/topprismwiki/references/architecture.md),
the [dependency and routing contract](skills/topprismwiki/references/dependencies-and-routing.md),
the [capability matrix](skills/topprismwiki/references/capability-matrix.md),
the [adapter guide](docs/en/adapters.md), the [FAQ](docs/en/faq.md), and the [privacy contract](skills/topprismwiki/references/privacy.md).

The public Runner classifies capabilities as `built-in`, `adapter-required`, or
`not-yet-supported`. It does not export WeChat, parse Office files, call vision or
ASR services, or claim automatic Obsidian post-commit validation.
