# 中文简历 Bullet

## AI 解决方案实习

- 设计并实现 AI-assisted BI Workflow 作品集项目，将电商 raw 数据处理、RFM 客户分群、LLM 中文洞察、Power BI 刷新和 Streamlit 业务问答串成可演示闭环。
- 构建 Mock / SiliconFlow 双模式 LLM 调用方案，通过 numeric validation 和 fallback 降低 AI 编造关键业务数字和 API 不稳定风险。
- 拆分数据质量、RFM 分群、洞察生成和 Power BI 输出检查为 Skill Layer，为未来 Agent 编排提供清晰能力边界。
- 实现 Router Agent / Orchestrator，用确定性路由支持 demo case 对比、workflow 状态查询、RFM 摘要和 Power BI 流程解释。
- 建立 Eval Harness，对 Agent intent、tools、risk level、dry-run 和回答关键内容进行测试，提升 Demo 系统可解释性和可靠性。

## AI 售前实习

- 搭建面向电商客户运营场景的 AI BI Demo 系统，展示从数据源切换、客户分群、AI 洞察到 Power BI 刷新的完整业务价值链路。
- 设计中文 Streamlit Agent Workbench，用 KPI cards、分群图表、洞察卡片和自然语言问答降低非技术面试官理解门槛。
- 梳理 Mock 稳定演示与 SiliconFlow API 真实调用两套展示路径，兼顾现场演示稳定性和 AI 能力呈现。
- 编写飞书作品集页、面试口播稿、HR 演示指南和常见问答，形成面向业务与技术面试官的完整项目讲解材料。
- 用 Eval Harness 和 run metadata 展示 Demo 系统的可验证性，避免只展示静态截图或一次性跑通结果。

## BI / 数据分析实习

- 基于电商用户行为数据实现 RFM 客户分群，输出高价值用户、潜力用户、流失风险用户、一般保持用户和其他用户等运营分层。
- 设计用户级 `fact_user_behavior_scored.csv`，包含原始用户字段、RFM 分数、Weighted AOV、Value Proxy Score 和分群标签，支持 Power BI 主图表刷新。
- 生成 `customer_segments.csv`、`powerbi_llm_insights.csv` 和中文 Markdown 报告，使 BI 图表、AI 洞察和业务问答使用同一套指标口径。
- 通过 demo case 切换模拟 raw 数据源变化，验证分群人数、图表和洞察能随 pipeline 重新生成。
- 将 Weighted AOV 与分群人数、占比、Avg RFM Score 结合展示，突出客户价值差异而非只看用户量。

## LLM 应用实习

- 实现 LLM 洞察生成链路，让模型只接收 Python structured summary，不直接接触用户级明细或自行计算指标。
- 设计 prompt 约束和 numeric validation，要求客户数、占比、AOV、RFM Score 等业务数字必须来自结构化结果。
- 支持 Mock / SiliconFlow provider 切换，并在 API 失败或数字校验失败时 fallback 到 mock 输出，保证 Demo 可运行。
- 构建中文 AI 经营洞察输出，包括 Power BI insight CSV 和 Markdown 报告，适配国内业务场景展示。
- 通过 Eval Harness 验证 Router / Orchestrator 的稳定性，将 LLM 应用从“能回答”推进到“可评估、可解释”。

## 技术顾问实习

- 从业务问题出发设计 AI BI 原型系统，覆盖客户分群、经营洞察、Power BI 联动、自然语言问答和风险控制。
- 将复杂分析流程拆解为 Pipeline、Skill Layer、Agent Orchestration、Eval Harness 和 Workbench 展示层，便于向业务和技术双方解释。
- 编写技术深挖文档，说明 numeric validation、fallback、trace、eval、Power BI integration 和未来企业级扩展路径。
- 在不引入大型框架的前提下，用 Python、pandas、Streamlit 和轻量 Agent 实现可运行 Demo，体现方案落地和成本控制意识。
- 明确作品集项目边界，不夸大为生产系统，同时提出权限、调度、监控、审计和服务化等企业级升级方向。
