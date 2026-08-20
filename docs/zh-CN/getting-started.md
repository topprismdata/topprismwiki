# 安装与首次运行

本指南面向会使用 Git 和终端、但不需要阅读 Python 源码的用户。首版
完整支持 macOS；Linux 可运行核心 Runner；Windows 尚未验证。

## 前置条件

- Python 3.11 或更高版本。
- Git。
- Codex。公开入口只有 `$topprismwiki`，子模块不会安装成并列 Skill。
- 真实来源接入另需兼容适配器；它们不包含在本仓库中。

检查环境：

```bash
python3 --version
git --version
```

## 安装 Skill

从 GitHub 克隆仓库，然后把公开入口链接到 Codex Skill 目录。链接方式便于
更新仓库后立即使用新版本：

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

如果目标路径已经存在，先确认它是不是旧版本的 Topprismwiki；不要覆盖
未知 Skill。安装或更新后，重新启动一个 Codex 会话，让 Skill 清单刷新。

## 建立私有项目

仓库只保存代码和合成示例。真实 Workspace、Vault、来源登记和状态账本
必须放在仓库外的私有项目目录：

```bash
PROJECT_ROOT="/path/to/my-private-wiki"
python3 skills/topprismwiki/scripts/topprismwiki.py init --project "$PROJECT_ROOT"
python3 skills/topprismwiki/scripts/topprismwiki.py doctor \
  --capability core --strict --project "$PROJECT_ROOT"
```

期望结果是 `state: accepted`，并出现 `.topprismwiki/config.json`、
`workspace/` 和 `vault/wiki/`。如果结果为 `blocked`，先按返回的 `code`、
`next_action` 和 [故障排查](troubleshooting.md) 处理。

## 运行合成闭环

继续阅读 [合成数据闭环](synthetic-walkthrough.md)。它不会接触真实聊天、
真实文档或正式公司知识，可以在临时目录中验证安装是否正确。

## 生产接入前

先阅读 [生产部署](production-setup.md)、[适配器协议](adapters.md) 和
[能力矩阵](../../skills/topprismwiki/references/capability-matrix.md)。
不要把真实原件、聊天导出、模型端点配置或凭证复制进 Git 仓库。
