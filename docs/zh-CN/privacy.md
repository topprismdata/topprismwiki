# 隐私与公开发布

公开仓库只允许出现合成联系人、会话、客户、项目、文件、哈希、路径和时间。
真实微信导出、业务文档、Vault、Workspace、状态账本、模型端点和凭证必须
放在私有项目中，并由 `.gitignore` 排除。

- 原始证据保持在私有 Workspace，正式 Vault只写经过审阅的派生事实。
- 密钥、令牌、密码、Authorization头和完整模型响应不得进入Markdown、日志、
  HTML看板、诊断包或Issue。
- 外部模型只能接收经过数据外发批准的最小证据；默认优先本地模型。
- Issue只提交版本、错误码、最小合成复现和脱敏 `diagnose` 输出。
- 安全问题不要公开创建Issue，按仓库 `SECURITY.md` 的私密流程处理。

发布前运行：

```bash
python3 skills/topprismwiki/scripts/check_public_safety.py .
```

安全扫描通过不等于数据配置安全；部署者仍需检查适配器、模型端点和私有
项目权限。
