# 故障排查

遇到问题时不要先编辑Vault或状态账本，按下面顺序保留现场：

```bash
python3 scripts/topprismwiki.py doctor --capability core --strict \
  --project /path/to/wiki
python3 scripts/topprismwiki.py status --project /path/to/wiki
python3 scripts/topprismwiki.py diagnose --project /path/to/wiki
```

命令输出中的 `code` 是查询入口。可将错误码传给 `diagnose --error-code`，
或在本页搜索同名标题。若仍不能解决，只提交脱敏诊断包，不提交原始消息、
文档、Vault、凭证或完整路径。

## 安装与环境

### <a id="python"></a>Python版本不满足

错误码：`CORE_PYTHON_MISSING`。确认 `python3 --version` 为3.11或更高，
并确认运行命令使用的是同一个解释器。不要把虚拟环境目录提交到仓库。

### <a id="obsidian"></a>Obsidian CLI缺失

错误码：`OBSIDIAN_CLI_MISSING`。公开Runner不会自动安装或调用Obsidian。
只有部署把它作为生产门禁时才需要处理；核心合成闭环不依赖它。

### <a id="wechat"></a>微信适配器缺失

错误码：`WECHAT_ADAPTER_MISSING`。安装兼容适配器，或按适配器协议生成
私有JSONL。不要把真实微信导出复制到公开仓库。

### <a id="office"></a>Office提取器缺失

错误码：`OFFICECLI_MISSING`。确认配置中的命令在PATH上；没有提取器时，
Office单元只能隔离或由用户提供符合协议的证据包。

### <a id="vision"></a>视觉模型未配置

错误码：`VISION_CONFIGURATION_MISSING`。配置本地或明确批准的图像端点，
并确认模型具备OCR、版式、表格、图表和流程图理解能力。

### <a id="media"></a>媒体工具缺失

错误码：`FFMPEG_MISSING`。安装ffmpeg或将音视频单元保持隔离；不能依据
文件名或不完整转写推断事实。

## 输入与审阅

### <a id="invalid-json"></a>JSON输入无法读取

错误码：`INVALID_JSON`。定位输出中提到的文件，确认UTF-8编码、每行JSONL
只有一个对象、引号和逗号正确，然后重复同一命令。

### <a id="authorization-required"></a>缺少正式写入授权

错误码：`EXPLICIT_UPDATE_AUTHORIZATION_REQUIRED`。先运行preview并检查
审阅包；只有用户明确要求正式入库时才追加 `--authorized`。

### <a id="review-file-missing"></a>审阅包不存在

错误码：`REVIEW_FILE_MISSING`。把 `review-template.json` 复制为同一批次
目录中的 `review.json`，补齐事实、目标路径、证据和哈希后重试。

### <a id="review-schema"></a>审阅包结构错误

错误码：`REVIEW_FACTS_MUST_BE_ARRAY`、`INVALID_TARGET` 或 `INCOMPLETE_FACT`。
参照 `examples/review.json.example`，确认 `facts` 是数组，目标是Vault
目录下的相对 `.md` 路径，正式事实有内容和证据对象。

### <a id="evidence-hash"></a>证据哈希缺失

错误码：`MISSING_SOURCE_SHA256`。不要手填哈希；从保持不变的原始快照重新
计算64位十六进制SHA-256，并检查审阅包引用的来源版本没有变化。

## 批次、状态与治理

### <a id="batch-not-found"></a>找不到批次

错误码：`BATCH_NOT_FOUND`。先运行 `batch list`，复制账本中完整的批次ID。
不要自行拼接ID或用新批次掩盖旧批次。

### <a id="unit-not-found"></a>找不到重试单元

错误码：`UNIT_NOT_FOUND`。用 `batch show` 查看 `retryable_units`；如果单元
不在其中，检查适配器是否输出了该单元以及是否写入了正确项目目录。

### <a id="commit-report-missing"></a>accepted批次缺少提交报告

错误码：`ACCEPTED_BATCH_MISSING_COMMIT_REPORT`。立即停止后续提交，保留
`workspace/runs/<batch-id>/`，运行diagnose并在修复账本前取得人工裁决。

### <a id="unknown-state"></a>未知批次状态

错误码：`UNKNOWN_BATCH_STATE`。不要直接改状态；保留账本和运行目录，提交
脱敏诊断结果。

### <a id="governance-reason"></a>治理操作缺少原因

错误码：`REASON_REQUIRED`。为exclude或readmit提供不含敏感信息的审计原因。

## 仍无法解决

```bash
python3 scripts/topprismwiki.py diagnose \
  --batch-id <batch-id> --output /tmp/topprismwiki-diagnosis.json \
  --project /path/to/wiki
```

确认诊断包中没有真实路径、聊天文本、文档内容、令牌或认证信息，再使用
GitHub Issue模板提交。安全事件不要公开提交，按 `SECURITY.md` 的私密渠道
处理。未知错误码统一记为 `UNKNOWN_ERROR`，并附上最小复现步骤。

<a id="unknown-error"></a>
