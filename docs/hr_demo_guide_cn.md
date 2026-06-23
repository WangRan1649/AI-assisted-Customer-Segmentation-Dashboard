# HR 演示指南

这份指南面向非技术 HR，帮助快速判断这个项目看什么、怎么看，以及它为什么不是一组静态截图。

## 1. 打开 Streamlit 看什么

先打开 Streamlit 页面，看三个地方：

- 顶部 KPI cards：当前数据场景、总用户数、最大客户分群、高价值用户数、流失风险用户数。
- 经营总览图表：分群人数、分群占比、Weighted AOV by Segment。
- AI 经营洞察卡片：每张卡都包含标题、关联分群、复核状态和完整洞察正文。

判断重点：页面展示的是业务结果，而不是代码或 debug 信息。

## 2. 切换数据源看什么

左侧选择不同 Demo Case，例如 `baseline_original` 和 `apparel_vip_shift`，点击“应用数据源”，再点击“运行分析流水线”。

看点：

- KPI 是否变化
- 分群图表是否变化
- AI 洞察是否重新生成
- Power BI 刷新后图表是否同步变化

这能说明项目不是静态截图，而是可以根据数据源变化重新生成结果。

## 3. 打开 Power BI 看什么

Power BI 主要看：

- 分群人数图
- 不同分群的 Weighted AOV
- 用户级明细或筛选器
- AI Insight Box

判断重点：主图表和 AI Insight Box 是否来自同一次 pipeline 输出。如果数据源切换后刷新，图表和 AI 洞察应该一起变化。

## 4. 问 Agent 什么问题

可以在 Streamlit 的业务问答里输入：

- 这个数据的用户 RFM 是多少？
- 对比 baseline_original 和 apparel_vip_shift 的分群变化
- 如果我要切换到 apparel_vip_shift 并刷新 Power BI，需要执行什么？
- 当前 workflow 状态如何？

看点：

- 回答是否像业务总结，而不是技术日志。
- 是否能给出关键数据和建议。
- 是否能说明数据来源。

## 5. 项目亮点总结

这个项目适合关注以下能力：

- 能把 BI 看板升级为 AI 辅助分析流程。
- 能把数据分析、LLM、Power BI 和前端展示连成闭环。
- 能用中文解释业务价值，不只是写代码。
- 有 Mock 稳定演示，也有真实 API 接入能力。
- 有 Eval Harness 验证 Agent 行为，不只是一次性演示。

一句话总结：这是一个面向国内 AI 解决方案、AI 售前、技术顾问、BI 分析和 LLM 应用实习岗位的完整作品集项目。
