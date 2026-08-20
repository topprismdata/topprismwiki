# Contributing to TopprismWiki

Thank you for helping improve TopprismWiki. Contributions should preserve the
project's evidence, privacy and publication boundaries.

## Before opening a pull request

1. Create a focused branch using feat/, fix/, docs/ or test/.
2. Keep real chats, business documents, Vaults, Workspaces, credentials and
   private paths out of the repository.
3. Update the capability matrix when a public capability changes.
4. Run the package validator, unit tests, public safety scan and
   git diff --check.
5. Describe behavior changes, evidence, tests and any adapter assumptions in
   the pull request.

The public Runner is intentionally adapter-based. Do not add a direct source
connector or a Vault write path without updating the contracts, privacy rules
and atomic-commit tests.

## Commit message format

Use a short type prefix, a specific subject and an optional scope:

~~~text
feat: add <capability> — <one-line outcome>
fix: correct <failure> in <component>
docs: update <topic> in <file>
test: cover <behavior>
chore: maintain <tooling>
~~~

Keep the first line concise. Use the body for evidence, compatibility notes and
known limitations. Existing history is preserved; this convention applies to
new commits.

## Pull requests

Include:

- what changed and why;
- which capability level changed: built-in, adapter-required or not-yet-supported;
- commands run and their results;
- privacy and synthetic-data confirmation;
- migration or compatibility impact.

Do not claim production deployment, customer adoption, accuracy improvement or
benchmark performance unless the repository contains reproducible evidence.
