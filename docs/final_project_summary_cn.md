# 最终项目总结

## 最终版本号

`v3.5.1-business-showcase-ui`

V4.0 本轮不是功能升级，而是中文作品集交付包装版：将当前最终技术版本整理成适合国内 HR、中文飞书作品集、中文简历和中文面试讲解的材料。

## 当前能力

- 支持 demo case raw 数据源切换。
- 支持一键运行 AI BI pipeline。
- 自动生成 RFM 客户分群和用户级 scored fact table。
- 自动生成中文 AI 经营洞察和 Markdown 报告。
- Power BI 主图表和 AI Insight Box 读取同一套 pipeline 输出。
- 支持 Mock / SiliconFlow 双模式。
- 使用 numeric validation 降低 LLM 编造关键业务数字风险。
- 使用 fallback 保证 API 失败时仍可生成可用输出。
- 提供 Router Agent / Orchestrator 支持自然语言业务问答。
- 提供 Eval Harness 验证 Agent 行为可靠性。
- 提供 Streamlit 业务展示型 Workbench。

## 已完成版本路线

- **V3.1 AI BI Pipeline**：完成 raw 数据处理、RFM 分群、LLM 洞察和输出文件生成。
- **V3.2 Skill Layer**：将确定性能力拆成可复用 Skill。
- **V3.3 Router Agent + Orchestrator + Trace**：新增轻量 Agent 编排和运行 trace。
- **V3.4 Eval Harness**：新增测试集和指标，验证 Router / Orchestrator。
- **V3.5 Streamlit Agent Workbench**：新增业务人员前端页面。
- **V3.5.1 中文化展示 + 咨询风格 UI**：优化中文业务表达和展示风格。
- **V4.0 中文作品集交付包装**：新增中文飞书、简历、面试和技术讲解材料。

## 不做什么

当前版本明确不做：

- 不声称生产上线。
- 不引入 LangChain / LangGraph / Docker / 数据库等大型依赖。
- 不让 LLM 直接计算业务指标。
- 不默认调用真实 API。
- 不自动执行危险文件操作。
- 不删除 demo cases。
- 不提交 `.env`、logs 或 `_case_switch_backup/`。

## 下一步企业化升级方向

如果继续向企业级系统升级，可以考虑：

- 将 pipeline 服务化为 FastAPI。
- 使用 React 构建企业级前端。
- 增加用户登录、角色权限和数据权限。
- 增加任务调度、运行历史和失败重试。
- 建立指标口径中心和数据质量规则中心。
- 增加 SQL sandbox 和查询权限控制。
- 建立 LLM evaluation dashboard。
- 增加 trace viewer、监控告警和审计日志。
- 对接企业 CRM、CDP、数据仓库和 BI 平台。

## 最终定位

这个项目最适合用来展示：

- 业务理解：能把客户分群问题转化为可执行分析流程。
- 数据分析能力：能构建 RFM、Weighted AOV 和用户分层。
- AI 应用能力：能让 LLM 服务于业务洞察，而不是自由编造。
- 工程化意识：有 pipeline、metadata、fallback、eval 和可演示前端。
- 表达能力：能向 HR、业务面试官和技术面试官分别说明项目价值。
