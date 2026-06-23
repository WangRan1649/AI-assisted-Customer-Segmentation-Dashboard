# 项目 Pitch 中文版

## 一句话版

这是一个把 Power BI 客户分群看板升级成 AI-assisted BI Workflow 的作品集项目：Python 负责 RFM 和业务指标计算，LLM 负责中文经营洞察，Agent 负责自然语言问答和流程编排，Eval Harness 负责验证可靠性。

## 30 秒版

这个项目模拟电商客户运营场景。传统 BI 只能展示图表，业务人员还要自己解释结果；直接用 LLM 又容易编造数字。我的方案是用 Python pipeline 先完成数据清洗、RFM 分群、Weighted AOV 和用户级 scored fact table，再让 LLM 只基于 structured summary 生成中文经营洞察。Power BI 和 Streamlit 读取同一套输出，业务人员还可以通过 Agent Workbench 用自然语言追问。最后用 Eval Harness 验证 Router 和 Orchestrator 的行为稳定性。

## 2 分钟业务版

我做这个项目的出发点是：很多 BI 看板能回答“发生了什么”，但很难直接帮助业务人员回答“下一步应该做什么”。

在电商客户运营里，运营团队经常需要区分高价值客户、潜力客户、流失风险客户和普通客户。传统做法是数据分析师先清洗数据、算指标、出图表，再人工写分析结论。这个流程重复、慢，而且每次 raw 数据变化后都要重新整理。

我的项目把这个流程做成一个自动化闭环。raw 数据源变化后，运行 pipeline 就会重新生成 RFM 分群、用户级评分明细表、Power BI insight CSV、中文 Markdown 报告和 run metadata。Power BI 刷新后，主图表和 AI Insight Box 会同步变化。

同时，我加了一个 Streamlit Agent Workbench，业务人员可以输入“这个数据的用户 RFM 是多少？”或者“对比两个 demo case 的分群变化”。系统会通过 Router Agent 识别问题类型，由 Orchestrator 调用对应 Skill 或 CSV 输出，给出业务化回答。

关键是，LLM 不直接算数。所有客户数、占比、Weighted AOV、RFM Score 都来自 Python 计算后的 structured summary。LLM 只负责把这些数据转成经营语言，numeric validation 和 fallback 会降低编造数字和 API 不稳定带来的风险。

## 技术深讲版

这个项目的技术核心是把 BI 分析拆成三层：确定性计算层、AI 表达层和 Agent 编排层。

第一层是 Python Pipeline。它读取 `data/raw/`，清洗电商用户行为数据，计算 RFM、Weighted AOV、Value Proxy Score，并输出 `fact_user_behavior_scored.csv` 和 `customer_segments.csv`。Power BI 主图表读取用户级 scored fact table，AI Insight Box 读取 insight CSV，确保图表和洞察来自同一套 pipeline。

第二层是 Skill Layer。数据质量检查、RFM 分群、洞察生成、Power BI 输出检查都封装成 Skill。这样未来即使接入更复杂的 Agent，也不会让 Agent 直接改底层计算逻辑，而是调用边界清晰的确定性能力。

第三层是 Router Agent / Orchestrator。Router 是确定性 intent router，不调用 LLM，识别 list_demo_cases、compare_demo_cases、workflow_status、run_workflow、rfm_summary_question 等意图。Orchestrator 根据 intent 调用白名单能力，默认 dry-run，不执行任意 shell 命令。

LLM 部分支持 Mock / SiliconFlow 双模式。真实 API 输出会经过 numeric validation，校验业务数字是否来自 structured summary。如果 API 失败或校验失败，就 fallback 到 mock，并在 metadata 记录 api_reached、validation_passed、fallback_used、error_type 等信息。

最后是 Eval Harness。它用 CSV 测试集批量验证 intent、tools、risk、dry-run、refusal 和回答关键内容。这样可以证明 Agent 层不是偶然跑通，而是可系统性测试。

整体来说，这个项目展示的是从 BI dashboard 到 AI-assisted BI workflow 的升级：Python Skill 算数，LLM 解释，Agent 编排，Eval 验证。
