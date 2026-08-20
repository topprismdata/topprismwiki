# 命令与运维

以下命令都需要显式传入私有项目根目录。省略 `--project` 时会使用
`TOPPRISMWIKI_PROJECT` 或当前目录，生产环境建议始终显式传入。

| 命令 | 作用 | 是否写正式Vault |
| --- | --- | --- |
| `init` | 创建项目骨架和默认配置 | 否 |
| `doctor` | 检查环境和适配器配置 | 否 |
| `preview` | 读取JSONL并建立覆盖批次 | 否 |
| `update` | 校验review并事务写入Markdown | 是，且需要`--authorized` |
| `query` | 查询正式Markdown | 否 |
| `context` | 生成正式页面上下文投影 | 否，写Workspace artifact |
| `graph` | 查看正式REL及候选覆盖层 | 否 |
| `status` | 查看批次摘要和正式页数量 | 否 |
| `batch list/show` | 查看批次或指定批次 | 否 |
| `dashboard build` | 生成脱敏静态HTML看板 | 否，写Workspace artifact |
| `retry` | 标记指定单元进入重试队列 | 不写Vault，但会写状态账本 |
| `validate` | 验收指定批次 | 否 |
| `source approve/exclude/readmit` | 写来源治理记录 | 不写Vault，但需要明确用户授权 |
| `diagnose` | 生成脱敏诊断结果 | 否，除非显式指定输出文件 |

## 更新门禁

推荐顺序：

```bash
python3 scripts/topprismwiki.py preview --source all --project /path/to/wiki
python3 scripts/topprismwiki.py batch list --project /path/to/wiki
python3 scripts/topprismwiki.py update --batch-id <batch-id> \
  --authorized --project /path/to/wiki
python3 scripts/topprismwiki.py validate --batch-id <batch-id> \
  --project /path/to/wiki
```

`update` 没有 `--authorized`、缺少 `review.json`、目标路径不安全或证据哈希
无效时都必须停止。不要为了让状态变成 `accepted` 而直接修改账本。

## 状态解释

`accepted` 表示该批次已有提交报告并通过当前Runner检查；`previewed`表示
只完成预览；`no_change`表示没有输入记录；`review_required`表示等待审阅；
`quarantined`和`blocked`表示存在隔离或门禁问题；`partial`表示独立单元
部分完成；`rolled_back`表示提交失败并已恢复；`retry_queued`表示请求重试。

## 退出码

- `0`：命令完成，包含 `no_change` 或只读诊断完成。
- `2`：门禁阻塞、审阅缺失、校验失败或可定位的运行错误。
- 其他非零值：检查终端输出中的 `code`，并运行 `diagnose`。
