# Getting started

This guide targets Git and terminal users who do not need to read the Python
implementation. macOS is the complete supported production path. Linux is
supported for the core Runner; Windows is not yet verified.

## Requirements

- Python 3.11 or newer.
- Git.
- Codex. Only `$topprismwiki` is installed as a public Skill; child modules are
  internal modules.
- A compatible source adapter for real data. Adapters are not bundled.

```bash
python3 --version
git --version
```

## Install the Skill

Clone the repository and link the public entry skill into the Codex skills
directory:

```bash
git clone <repository-url> topprismwiki
cd topprismwiki

SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$SKILL_ROOT"
if [ -e "$SKILL_ROOT/topprismwiki" ] || [ -L "$SKILL_ROOT/topprismwiki" ]; then
  echo "Skill path already exists: $SKILL_ROOT/topprismwiki"
else
  ln -s "$(pwd)/skills/topprismwiki" "$SKILL_ROOT/topprismwiki"
fi

python3 skills/topprismwiki/scripts/validate_package.py skills/topprismwiki
```

Do not replace an unknown existing Skill path. Restart a Codex session after
installation or upgrade so the Skill inventory is refreshed.

## Create a private project

Keep Workspace, Vault, source registrations, originals and state ledgers outside
the public checkout:

```bash
PROJECT_ROOT="/path/to/my-private-wiki"
python3 skills/topprismwiki/scripts/topprismwiki.py init --project "$PROJECT_ROOT"
python3 skills/topprismwiki/scripts/topprismwiki.py doctor \
  --capability core --strict --project "$PROJECT_ROOT"
```

The expected result is `state: accepted`. If it is `blocked`, use the returned
`code`, `next_action` and [troubleshooting guide](troubleshooting.md).

Continue with the [synthetic walkthrough](synthetic-walkthrough.md) before
connecting real sources. Then read [production setup](production-setup.md),
[adapter contracts](adapters.md) and the [capability matrix](../../skills/topprismwiki/references/capability-matrix.md).
