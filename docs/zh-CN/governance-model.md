# 治理模型

TopprismWiki 将正式发布视为受控状态转换：

~~~text
来源批准
  → 证据抽取与哈希
  → 实体与关系审核
  → 审核后的决策包
  → dry-run 或 preview
  → 明确授权的原子提交
  → 提交后验收
~~~

正式事实需要来源身份、证据锚点、内容哈希、主体和客体或值、时间或适用范围，以及相应的审阅决定。共同群名、文件名、共同出现或品牌提及不能单独证明客户、项目、人物或交付关系。

状态包括：formalized、duplicate、conflicting、relation_candidate、evidence_insufficient 和 non_durable。

Preview、query、context、graph、status 和 dashboard 对正式 Vault 只读；update 必须具备明确授权和审阅包。原子提交失败时不得推进相关水位。

原始证据保存在私有 Workspace，公开示例使用合成身份、路径和哈希。凭证和模型端点不得写入 Markdown、日志、Issue 或投影。
