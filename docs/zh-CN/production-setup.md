# 生产部署

公开包的生产路径是“私有适配器生成证据 → Runner建立批次 → 人工或治理
Agent审阅 → dry-run/事务提交 → 验收”。公开仓库不会读取真实微信、Office
或模型服务。

## 项目隔离

- 仓库目录只放代码、文档和合成示例。
- 私有项目单独放置 `workspace/`、`vault/`、来源原件和模型配置。
- 原件保持原路径、内容、修改时间和哈希；不要把原件复制进 Git。
- 查询默认只看正式 `vault/wiki/`；Workspace 证据必须显式标注。

## 配置检查

```bash
python3 skills/topprismwiki/scripts/topprismwiki.py doctor \
  --capability all --project /path/to/private-wiki
```

`doctor` 会把核心 Python、Obsidian、WeChat适配器、Office提取器、视觉
端点和媒体工具分别列出。没有使用某类来源时，不要因为可选检查缺失就伪造
安装；使用对应能力前再用 `--strict` 检查该能力。

## 来源治理

来源批准、排除和重新准入必须是用户明确指令：

```bash
python3 skills/topprismwiki/scripts/topprismwiki.py source list \
  --project /path/to/private-wiki
python3 skills/topprismwiki/scripts/topprismwiki.py source approve \
  --id source-alias --path /path/to/approved-root --sensitivity internal \
  --project /path/to/private-wiki
```

公开 Runner会记录治理事件；完整的来源优先级、永久哈希拒绝和版本家族
执行属于生产适配器和治理层，见 [治理子Skill](../../skills/topprismwiki/subskills/topprismwiki-governance/SKILL.md)。

## Obsidian门禁

配置中的 `obsidian_cli_required_for_apply` 是生产部署声明，不代表公开
Runner已经自动调用 Obsidian CLI。若部署将其作为正式门禁，必须在外部验收
步骤中执行并保留结果，不能把 `doctor` 的可执行路径检查当作知识库验收。

## 视觉模型

图片、PDF和PPT需要同时具备 OCR、版式、表格、图表和流程图理解能力。仅能
提取文字的模型不能证明视觉证据已经理解。默认优先使用本地模型；任何云端
端点都必须经过单独的数据外发审批，且不允许传入凭证或无限制Workspace路径。

## 正式批次顺序

```text
approve source
  → adapter snapshot and hash
  → preview
  → inspect coverage and quarantines
  → review decision package
  → update --authorized
  → validate
  → inspect status/dashboard
```

失败、隔离或证据不足的单元不能被标记为成功；遇到异常先运行 `diagnose`，
不要直接编辑 `batches.json` 或正式 Vault。
