# Adapter integration

An adapter converts private source material into evidence records. The public
package defines the contract but does not distribute `wechat-cli`, `officecli`,
vision services or ASR implementations. See [adapter-contracts.md](../../skills/topprismwiki/references/adapter-contracts.md).

## WeChat

The adapter owns approved-session lookup, Asia/Shanghai closed-interval
filtering, message and attachment attribution, snapshot hashes, aliases,
evidence anchors and durable per-session watermarks. It writes UTF-8 JSONL to
`workspace/inbox/wechat/`. The public Runner counts supplied records and creates
batches; it does not connect to WeChat or refilter the interval.

Each unit should include `unit_id`, `session_alias`, a closed `interval`, message
and attachment counts, classification, state and `source_sha256`.

## Office and visual sources

Preserve Office originals and record hash, version family, sensitivity and
page/section/table anchors. PDF, PPT and image processing requires page rendering
and a model that understands OCR, layout, tables, charts and diagrams.

## Audio and video

Use `ffmpeg` for deterministic preprocessing and a Chinese-capable ASR model.
Record timestamps, media hash, model identity and confidence. Unmatched or
unintelligible media remains `quarantined`.

Before production, test empty input, duplicate input, changed hashes, timezone
boundaries, attachment attribution failure, partial media failure, non-zero
adapter exits and retry watermark behavior with synthetic fixtures.
