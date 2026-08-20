# Synthetic end-to-end walkthrough

This walkthrough verifies the built-in public Runner. All sessions, projects,
hashes and content are synthetic.

```bash
cd /path/to/topprismwiki
DEMO_ROOT="$(mktemp -d)"
RUNNER="$(pwd)/skills/topprismwiki/scripts/topprismwiki.py"
python3 "$RUNNER" init --project "$DEMO_ROOT"
mkdir -p "$DEMO_ROOT/workspace/inbox/wechat"
cp skills/topprismwiki/examples/wechat-events.jsonl.example \
  "$DEMO_ROOT/workspace/inbox/wechat/events.jsonl"
PREVIEW_JSON="$(python3 "$RUNNER" preview --source wechat --project "$DEMO_ROOT")"
printf '%s\n' "$PREVIEW_JSON"
BATCH_ID="$(printf '%s' "$PREVIEW_JSON" | python3 -c \
  'import json,sys; print(json.load(sys.stdin)["batch"]["batch_id"])')"
```

Preview creates a Workspace coverage package and batch ledger, not formal pages.
Create the reviewed package and commit the synthetic fact:

```bash
cp skills/topprismwiki/examples/review.json.example \
  "$DEMO_ROOT/workspace/runs/$BATCH_ID/review.json"
python3 "$RUNNER" update --batch-id "$BATCH_ID" --authorized \
  --project "$DEMO_ROOT"
python3 "$RUNNER" validate --batch-id "$BATCH_ID" --project "$DEMO_ROOT"
python3 "$RUNNER" query "demo project" --project "$DEMO_ROOT"
python3 "$RUNNER" graph demo-project --project "$DEMO_ROOT"
python3 "$RUNNER" context "prepare a demo project review" --budget 6000 \
  --project "$DEMO_ROOT"
python3 "$RUNNER" dashboard build --project "$DEMO_ROOT"
```

Open the generated `workspace/artifacts/batch-dashboard.html` locally. The
dashboard is read-only and contains no raw evidence. Remove only the temporary
directory after the test:

```bash
rm -rf "$DEMO_ROOT"
```
