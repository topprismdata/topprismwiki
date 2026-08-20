# TopprismWiki

## 面向 Agentic AI 的企业知识治理层

[![Python](https://img.shields.io/badge/python-3.11%2B-3776AB.svg)](https://www.python.org/)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF.svg)](.github/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-%24topprismwiki-6E56CF.svg)](skills/topprismwiki/SKILL.md)
[![Privacy](https://img.shields.io/badge/data-public%20examples%20only-0B7A75.svg)](docs/zh-CN/privacy.md)

TopprismWiki 是一个证据治理驱动的知识层，把经过批准的企业证据转化为可追溯的正式知识，供 AI Agent 受控使用。

传统检索解决“找到信息”；TopprismWiki 进一步治理“什么可以成为知识、为什么可信，以及知识如何被发布和使用”。

它以 Agent Skill 包和无外部依赖的 Python 参考 Runner 交付。长期方向是企业知识 Operating Layer；当前公开仓库提供的是可验证的治理合同和参考工作流，不把未来能力包装成现有能力。

## 为什么需要 TopprismWiki

Agentic 系统不仅检索文档，还会总结、推荐、更新记录并执行动作。因此，知识的来源、冲突、版本和发布权限都必须成为系统的一部分：

- 当前决策允许使用哪些来源？
- 一个事实或关系的证据是什么？
- 相互矛盾的陈述如何共存？
- 谁或什么可以发布变更？
- Agent 能否区分正式知识、候选关系和待核验来源？

TopprismWiki 在企业来源与 Agent 上下文之间提供治理发布层：

~~~text
企业证据
  ↓
来源适配器与证据合同
  ↓
审核、实体与关系治理
  ↓
确定性正式提交
  ↓
可信 Knowledge Vault
  ↓
面向 Agent 的查询、上下文和图谱投影
~~~

## 它是什么，不是什么

TopprismWiki 提供：

- 已批准来源和适配器记录的证据合同；
- 来源哈希、证据锚点、审阅包和冲突状态；
- 规范实体、类型化关系和独立的候选关系覆盖层；
- 经过审阅、哈希校验和原子事务保护的 Markdown Vault 发布；
- 有边界的查询、上下文、图谱、批次和诊断投影；
- 唯一公开入口 $topprismwiki，以及其内部子模块。

TopprismWiki 不是向量数据库、通用 RAG 框架、自动事实生成器，也不是内置的微信、Office 或 OCR 连接器。公开 Runner 将内置治理能力与部署方提供的适配器、模型服务严格分开。

## 企业知识生命周期

~~~mermaid
flowchart TB
    S[企业来源] --> A[来源适配器]
    A --> W[Evidence Workspace]
    W --> G[审核与治理]
    G --> C[确定性提交器]
    C --> V[Trusted Knowledge Vault]
    V --> R[查询、上下文和图谱]
    R --> AG[AI Agent]
    W -. 冲突、候选关系、状态 .-> R
~~~

系统分为三层：

| 层 | 作用 | 写入规则 |
| --- | --- | --- |
| Formal Vault | 已批准事实、规范实体、决定和类型化关系 | 只有确定性提交器可以写入 |
| Evidence Workspace | 原件、快照、哈希、证据包、审阅包、冲突、候选关系和账本 | 可变、可重建 |
| Interaction 投影 | 查询、上下文、图谱、状态、批次和看板 | 只读投影 |

共同出现、群名、成员名单、文件名和品牌提及不能单独建立正式关系。

## 当前能力

| 能力 | 公开状态 |
| --- | --- |
| 项目初始化、JSONL 预览和批次账本 | 内置 |
| 审阅门禁、Markdown 原子发布和回滚 | 内置 |
| 正式查询、预算受控上下文和 REL 图谱投影 | 内置 |
| 只读批次看板和诊断 | 内置 |
| 微信、Office、PDF、图片和媒体处理 | 需要适配器 |
| 生产级逐来源水位和 Obsidian 提交后验收 | 公开 Runner 尚未强制执行 |

完整边界见[能力矩阵](skills/topprismwiki/references/capability-matrix.md)。

## 60 秒合成 Demo

公开 Demo 只使用合成聊天事件，不包含真实企业资料。完整路径见[合成数据闭环](docs/zh-CN/synthetic-walkthrough.md)。

当前可复现结果：

~~~text
2 个处理单元
11 条输入消息
1 条正式化事实
1 个证据不足单元
1 个原子提交的正式页面
提交后验收 accepted
~~~

预览只生成 Workspace 证据，不写入正式 Vault；正式更新必须同时具备明确授权和审核后的决策包。

## 方案差异

以下是典型架构模式比较，不是对所有产品的 Benchmark 或绝对判断。

| 关注点 | 文档知识库 | 典型 RAG | 典型 GraphRAG | TopprismWiki |
| --- | --- | --- | --- | --- |
| 核心目标 | 存储和阅读文档 | 为生成检索片段 | 检索图谱与文本上下文 | 治理哪些内容可以成为正式知识 |
| 来源批准 | 通常由库外流程负责 | 由应用定义 | 由应用定义 | 有明确来源和准入合同 |
| 证据锚点 | 取决于实现 | 通常是段落级 | 通常是文档或边级 | 正式事实和操作必须具备 |
| 关系建立 | 通常人工或隐式 | 通常不属于检索层 | 往往由抽取流程驱动 | 类型化、有证据、候选关系分离 |
| 冲突处理 | 往往人工处理 | 由 Prompt 或应用负责 | 由图谱应用负责 | 显式保留冲突和待核验状态 |
| 正式发布 | 依赖工具或流程 | 依赖管线 | 依赖管线 | 审阅包、哈希校验和原子提交 |

## 证据、评估与文档

当前公开包验证的是治理参考工作流，不是生产规模的知识质量 Benchmark。当前测试覆盖：

- 8 个嵌套 Skill 模块的包校验；
- 授权、预览隔离、原子更新、回滚、查询、图谱、重试和诊断；
- 私有路径、凭证和未脱敏来源示例的公开安全扫描；
- 合成数据的预览、审阅更新、验收、查询、图谱和看板。

详见[评估说明](docs/zh-CN/evaluation.md)、[路线图](ROADMAP.md)和[英文文档](README.md)。

## 快速开始

先阅读[安装与首次运行](docs/zh-CN/getting-started.md)，再运行[合成数据闭环](docs/zh-CN/synthetic-walkthrough.md)。

~~~bash
git clone https://github.com/topprismdata/topprismwiki.git
cd topprismwiki
python3 skills/topprismwiki/scripts/topprismwiki.py init --project /path/to/my-wiki
python3 skills/topprismwiki/scripts/topprismwiki.py doctor --capability core --project /path/to/my-wiki
python3 skills/topprismwiki/scripts/topprismwiki.py preview --source all --project /path/to/my-wiki
~~~

遇到 blocked 或非零退出码时，先运行：

~~~bash
python3 skills/topprismwiki/scripts/topprismwiki.py diagnose --project /path/to/my-wiki
~~~

## 文档入口

- [核心概念](docs/zh-CN/concepts.md)
- [产品架构](docs/zh-CN/product-architecture.md)
- [治理模型](docs/zh-CN/governance-model.md)
- [适配器接入](docs/zh-CN/adapters.md)
- [命令与运维](docs/zh-CN/operations.md)
- [故障排查](docs/zh-CN/troubleshooting.md)
- [隐私合同](docs/zh-CN/privacy.md)
- [评估说明](docs/zh-CN/evaluation.md)
- [路线图](docs/zh-CN/roadmap.md)
- [English README](README.md)

## 隐私、贡献与许可证

仓库只包含合成联系人、聊天、客户、项目、文件名、哈希、路径和时间。真实聊天、业务文档、Vault、Workspace、账本、模型端点和凭证不得提交到 Git。

发布前运行：

~~~bash
python3 skills/topprismwiki/scripts/check_public_safety.py .
~~~

贡献前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 和 [SECURITY.md](SECURITY.md)。项目使用 Apache-2.0，见 [LICENSE](LICENSE)。
