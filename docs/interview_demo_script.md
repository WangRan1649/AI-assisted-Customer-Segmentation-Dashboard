# 5 分钟中文面试展示口播稿

## 1. 30 秒开场

我这个项目叫 AI 辅助型客户分群与 BI 决策系统。它不是一个静态 Power BI 看板，也不是一个普通聊天机器人，而是一个 AI-assisted BI Workflow。

它的核心思路是：Python 负责清洗数据和计算 RFM 分群，LLM 只负责把结构化结果转成业务洞察，Agent 负责让业务人员用自然语言追问，Power BI 和 Streamlit 负责展示，Eval Harness 负责验证 Agent 行为是否稳定。

这个项目主要模拟电商客户运营场景，目标是帮助业务人员快速判断哪些客户应该留存、转化、召回或培育。

## 2. 展示 Streamlit 首页

我先打开 Streamlit 工作台。首页可以看到几个核心 KPI：当前数据场景、总用户数、最大客户分群、高价值用户数和流失风险用户数。

下面是分群人数柱状图、分群占比图和 Weighted AOV by Segment。这里我故意把页面做成业务展示型，而不是 debug console，因为面向的是业务人员和面试官。

## 3. 切换 raw 数据源

左侧可以选择 demo case，比如 `baseline_original` 和 `apparel_vip_shift`。这模拟企业里 raw 数据源变化的情况。

我点击“应用数据源”，它只会切换 `data/raw/` 下的原始数据，不会自动调用真实 API，也不会执行危险操作。

## 4. 运行 pipeline

接下来点击“运行分析流水线”，这里我一般选择 `mock` provider 做稳定展示。

pipeline 会重新读取 raw 数据，生成用户级评分明细表、客户分群表、Power BI insight CSV、Markdown 洞察报告和 run metadata。

## 5. 展示 RFM 分群变化

运行完成后回到经营总览，可以看到分群人数、占比和 Weighted AOV 都会根据新数据更新。

这里的 RFM、Weighted AOV、Value Proxy Score 都是 Python 算出来的，不是 LLM 自己编的。LLM 只负责把这些结构化结果转成业务能读懂的建议。

## 6. 展示 Agent 业务问答

接着我切到“业务问答”，输入“这个数据的用户 RFM 是多少？”。

系统会通过 Router Agent 判断这是 RFM 摘要问题，然后 Orchestrator 读取 `customer_segments.csv`，生成面向业务负责人的总结：先给结论，再列关键数据，最后给建议。

这个回答不是让 LLM 自由发挥，而是基于 Python 生成的 CSV。

## 7. 展示 Power BI Refresh

然后我打开 Power BI。Power BI 主图表推荐读取 `data/processed/fact_user_behavior_scored.csv`，AI Insight Box 读取 `outputs/powerbi_llm_insights.csv`。

因为两个文件来自同一次 pipeline，所以刷新 Power BI 后，图表和 AI 洞察使用的是同一套分群结果，不会出现主图表和 Insight Box 数字不一致的问题。

## 8. 展示 Eval Harness

最后我展示 Eval Harness。它会测试 Router / Orchestrator 的 intent、tools、risk level、dry-run、refusal 和回答关键内容。

这个设计是为了说明 Agent 不是“刚好跑通一次”，而是可以用测试集系统性验证。

## 9. 总结项目价值

总结一下，这个项目展示了一个从 BI Dashboard 升级到 AI-assisted BI Workflow 的完整闭环：

Python 负责确定性计算，LLM 负责中文经营洞察，Agent 负责编排和问答，Power BI 和 Streamlit 负责展示，Eval Harness 负责可靠性验证。

它比较适合 AI 解决方案、AI 售前、技术顾问、BI 数据分析和 LLM 应用相关岗位，因为它同时体现了业务理解、数据分析、AI 应用落地和工程化意识。
