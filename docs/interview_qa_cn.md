# 中文面试常见问答

## 1. 这个项目和普通 Power BI 看板有什么区别？

普通 Power BI 看板主要展示指标和图表，本项目把看板升级成 AI-assisted BI Workflow。它不仅能展示分群结果，还能在 raw 数据变化后重新生成分群、输出中文 AI 洞察，并允许业务人员用自然语言追问当前数据。Power BI 是展示层之一，不是全部。

## 2. 为什么要接 LLM？

LLM 的价值不是替代指标计算，而是把结构化数据转成业务人员更容易理解的经营语言，例如高价值客户该如何留存、流失风险客户该如何召回。这样可以减少人工写报告和整理洞察的时间。

## 3. 为什么不用纯 LLM 直接分析 CSV？

纯 LLM 直接分析 CSV 容易出现三个问题：数据量稍大时上下文不稳定；指标口径不清；模型可能编造数字。本项目让 Python 先完成确定性计算，再把 structured summary 给 LLM，LLM 只负责解释，不负责算数。

## 4. RFM 是怎么计算的？

RFM 通常从三个维度衡量客户价值：Recency 表示最近活跃或购买时间，Frequency 表示购买频次，Monetary 表示消费金额。本项目基于这些字段计算 r_score、f_score、m_score，再汇总为 rfm_score，并结合价值指标形成客户分群。

## 5. Weighted AOV 为什么不能直接求平均？

如果直接对 Average Order Value 求平均，可能忽略不同用户购买频次和总消费差异。Weighted AOV 使用 `Total_Spending / Purchase_Frequency`，更贴近用户真实消费贡献，避免被简单均值误导。

## 6. Mock 和 API 有什么区别？

Mock 模式使用本地模板生成稳定输出，不依赖网络，适合面试和作品集演示。API 模式会调用 SiliconFlow，展示真实 LLM 接入能力。两者都使用同一套 Python structured summary，区别在于文本生成来源。

## 7. 为什么要做 Skill Layer？

Skill Layer 的目的是把确定性能力封装清楚，例如数据质量检查、RFM 分群、洞察生成和 Power BI 输出检查。未来如果引入更复杂 Agent，Agent 只需要选择和调用 Skill，而不是直接改底层计算代码。

## 8. Router Agent 有什么价值？

Router Agent 把自然语言问题映射到具体意图，例如列出 demo cases、对比分群变化、查看 workflow 状态、解释 Power BI 流程或回答 RFM 摘要。它不调用 LLM，行为稳定，可测试，也更适合当前作品集项目的安全边界。

## 9. Eval Harness 怎么证明可靠性？

Eval Harness 维护一组测试问题和预期结果，检查 intent、selected tools、risk level、dry-run、refusal 和回答中是否包含关键内容。它证明 Agent 不是只在某一次演示中跑通，而是可以被系统性测试。

## 10. 如何防止 AI 幻觉？

项目有三层控制：第一，LLM 只接收 Python 生成的 structured summary；第二，prompt 明确要求不能编造数字；第三，numeric validation 检查输出中的关键业务数字是否来自 summary。如果校验失败，会 fallback 到 mock。

## 11. 如果 API 失败怎么办？

如果 API key 缺失、网络超时、接口失败或 numeric validation 不通过，系统会自动 fallback 到 mock 输出，并在 `outputs/run_metadata.json` 中记录 `api_reached`、`validation_passed`、`fallback_used` 和 `error_type`。

## 12. Power BI 如何和 Python pipeline 联动？

Python pipeline 输出 `data/processed/fact_user_behavior_scored.csv` 和 `outputs/powerbi_llm_insights.csv`。Power BI 主图表读取 scored fact table，AI Insight Box 读取 insight CSV。这样刷新 Power BI 后，图表和 AI 洞察使用同一套分群结果。

## 13. 为什么用 Streamlit？

Streamlit 适合快速构建本地可演示页面，不需要 React、FastAPI、数据库或 Docker。它适合作品集和面试展示，让非技术人员直观看到 KPI、图表、洞察和自然语言问答。

## 14. 真实企业落地还需要补什么？

需要补充权限控制、数据权限、任务调度、运行历史、服务化 API、监控告警、审计日志、数据质量规则、指标口径管理和更完整的 LLM evaluation。当前项目是 Demo 系统，不夸大为生产上线系统。

## 15. 这个项目适合迁移到哪些行业？

凡是有客户分层、经营指标和 BI 报表的场景都可以迁移，例如零售、电商、金融客户运营、SaaS 客户成功、教育用户运营、会员体系、汽车售后和本地生活服务。核心方法是：确定性指标计算 + AI 经营解释 + Agent 编排 + Eval 验证。
