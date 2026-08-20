# 合成数据闭环

这条路径验证公开 Runner 的内置能力。示例中的会话、项目、哈希和内容
都是合成数据，不代表任何真实公司资料。

## 1. 初始化临时项目

```bash
cd /path/to/topprismwiki
DEMO_ROOT="$(mktemp -d)"
RUNNER="$(pwd)/skills/topprismwiki/scripts/topprismwiki.py"
python3 "$RUNNER" init --project "$DEMO_ROOT"
```

## 2. 放入合成事件并预览

```bash
mkdir -p "$DEMO_ROOT/workspace/inbox/wechat"
cp skills/topprismwiki/examples/wechat-events.jsonl.example \
  "$DEMO_ROOT/workspace/inbox/wechat/events.jsonl"
PREVIEW_JSON="$(python3 "$RUNNER" preview --source wechat --project "$DEMO_ROOT")"
printf '%s\n' "$PREVIEW_JSON"
BATCH_ID="$(printf '%s' "$PREVIEW_JSON" | python3 -c \
  'import json,sys; print(json.load(sys.stdin)["batch"]["batch_id"])')"
```

预览只创建 Workspace 证据包和批次账本，不应在 `vault/wiki/` 产生页面。
运行以下命令查看批次：

```bash
python3 "$RUNNER" batch show "$BATCH_ID" --project "$DEMO_ROOT"
```

## 3. 生成审阅包并正式提交

公开 Runner 要求提交前存在人工审阅过的 `review.json`。合成示例可以直接
作为审阅包使用：

```bash
cp skills/topprismwiki/examples/review.json.example \
  "$DEMO_ROOT/workspace/runs/$BATCH_ID/review.json"
python3 "$RUNNER" update --batch-id "$BATCH_ID" --authorized \
  --project "$DEMO_ROOT"
python3 "$RUNNER" validate --batch-id "$BATCH_ID" --project "$DEMO_ROOT"
```

`--authorized` 只表示本次明确授权写入；它不会替代证据哈希、目标路径和
审阅包校验。没有它，命令应返回 `EXPLICIT_UPDATE_AUTHORIZATION_REQUIRED`。

## 4. 查询、图谱和看板

```bash
python3 "$RUNNER" query "demo project" --project "$DEMO_ROOT"
python3 "$RUNNER" graph demo-project --project "$DEMO_ROOT"
python3 "$RUNNER" context "prepare a demo project review" --budget 6000 \
  --project "$DEMO_ROOT"
python3 "$RUNNER" status --project "$DEMO_ROOT"
python3 "$RUNNER" dashboard build --project "$DEMO_ROOT"
open "$DEMO_ROOT/workspace/artifacts/batch-dashboard.html"
```

看板是只读投影，不执行 retry、update 或 source governance。所有正式页面
都应位于临时项目的 `vault/wiki/` 内。

## 5. 清理

确认没有需要保留的测试结果后，删除本次明确创建的临时目录：

```bash
rm -rf "$DEMO_ROOT"
```

不要把这条清理命令改成指向仓库、主目录或真实项目的路径。
