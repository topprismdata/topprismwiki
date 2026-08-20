# Topprismwiki

[![Python](https://img.shields.io/badge/python-3.11%2B-3776AB.svg)](https://www.python.org/)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF.svg)](.github/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
[![Skill](https://img.shields.io/badge/Codex-Skill-6E56CF.svg)](skills/topprismwiki/SKILL.md)
[![Privacy](https://img.shields.io/badge/data-public%20examples%20only-0B7A75.svg)](docs/privacy.md)

Topprismwiki 是一个公司级知识治理技能包：它把来源批准、证据、实体、关系、批次、水位、冲突和事务提交放在同一条可追溯流程中。

它只有一个公开入口 `$topprismwiki`，微信、文档、查询、上下文、图谱、状态和治理能力都作为其内部子技能，不会安装成并列 Skill。

完整英文说明见 [README.en.md](README.en.md)。

## 核心边界

```text
来源适配器 → Workspace 证据与批次 → review / dry-run → 原子提交器 → formal Vault
                                  ↘ 查询 / 上下文 / 图谱 / Batch Dashboard
```

- `Vault` 保存已经通过证据和关系门禁的正式知识。
- `Workspace` 保存原件快照、哈希、证据包、冲突、候选关系和运行状态。
- 只有确定性提交器可以修改正式 Vault；查询、看板和候选关系都是只读投影。
- 共同出现、群名、成员名单、文件名或品牌提及不能单独建立正式关系。
- 失败或隔离单元不推进水位，也不影响独立单元继续处理。

## 快速开始

```bash
git clone <your-repository-url> topprismwiki
cd topprismwiki
python3 skills/topprismwiki/scripts/topprismwiki.py init --project /path/to/my-wiki
python3 skills/topprismwiki/scripts/topprismwiki.py doctor --capability core --project /path/to/my-wiki
python3 skills/topprismwiki/scripts/topprismwiki.py preview --source all --project /path/to/my-wiki
python3 skills/topprismwiki/scripts/topprismwiki.py status --project /path/to/my-wiki
python3 skills/topprismwiki/scripts/topprismwiki.py dashboard build --project /path/to/my-wiki
```

`update` 是唯一允许提交正式知识的命令，并要求明确的 `--authorized` 和已审核的 `review.json`：

```bash
python3 skills/topprismwiki/scripts/topprismwiki.py update \
  --source documents --authorized --project /path/to/my-wiki
```

默认项目目录结构为：

```text
my-wiki/
├── .topprismwiki/config.json
├── vault/wiki/                 # formal knowledge
└── workspace/
    ├── inbox/                  # private adapter output
    ├── runs/                   # evidence and review packages
    ├── state/                  # ledgers and batch summaries
    └── artifacts/              # query, context, and dashboard projections
```

## 功能模块

| 模块 | 作用 | 典型依赖 |
| --- | --- | --- |
| 微信正式化 | 批准会话、消息、附件和水位 | `wechat-cli`、`officecli`、视觉/ASR适配器 |
| 文档正式化 | Office、PDF、图片和版本家族 | `officecli`、Poppler、视觉模型 |
| 查询 | 只查询正式 Vault | Python；Obsidian CLI 用于生产验收 |
| 上下文 | 生成预算受控的任务上下文 | Python |
| 图谱 | 正式 REL 与候选覆盖层 | Python |
| 状态与 Batch | 批次、隔离项、水位和健康状态 | Python |
| 治理 | 来源批准、排除、重新准入、重试和验收 | Python；明确用户授权 |

详细依赖和模型要求见 [dependencies-and-routing.md](skills/topprismwiki/references/dependencies-and-routing.md)。

## Agent 路由

公开包使用能力角色，而不是绑定某个厂商：编排器负责授权和批次，文本提取器负责普通材料，视觉复核器负责 OCR 和页面语义，批处理 Worker 负责低风险内容，裁决器负责实体/关系/冲突，治理复核器负责提交门禁，确定性提交器负责 Vault 写入。

视觉模型必须同时具备 OCR、表格、图表、流程和版式理解能力；仅能 OCR 的模型不能完成视觉证据验收。模型可以替换，证据契约和提交权限不能替换。

## Batch Dashboard

生成本地只读静态看板：

```bash
python3 skills/topprismwiki/scripts/topprismwiki.py batch list --project /path/to/my-wiki
python3 skills/topprismwiki/scripts/topprismwiki.py batch show <batch-id> --project /path/to/my-wiki
python3 skills/topprismwiki/scripts/topprismwiki.py dashboard build --project /path/to/my-wiki
```

看板展示批次状态、覆盖数量、隔离项、可重试单元和水位状态，不展示原始消息、秘密或未经脱敏的绝对路径。看板按钮只提供可复制命令，不直接执行写操作。

## 隐私与公开范围

仓库中的联系人、群聊、客户、项目、文件、哈希、路径和时间均为合成示例。真实聊天、业务文档、Vault、Workspace、状态账本、模型端点和凭证不得提交。发布前运行：

```bash
python3 skills/topprismwiki/scripts/check_public_safety.py .
```

完整规则见 [privacy.md](skills/topprismwiki/references/privacy.md) 和 [docs/privacy.md](docs/privacy.md)。

## 状态和错误处理

批次状态包括 `accepted`、`no_change`、`quarantined`、`blocked`、`partial`、`rolled_back` 和 `review_required`。`retry` 只处理指定单元，`validate` 只读验收；重复运行同一输入应产生零正式变更。

## 许可证

本项目使用 Apache-2.0，见 [LICENSE](LICENSE)。
