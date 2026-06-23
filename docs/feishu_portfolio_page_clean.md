# AI 辅助型客户分群与 BI 决策系统

## 01 项目一句话定位

这是一个面向电商客户运营场景的 AI-assisted BI Workflow。

它不是静态 BI 看板，而是从 raw 数据源切换、Python 自动处理、RFM 分群、中文 AI 洞察、Power BI 刷新，到 Agent 业务问答的完整分析闭环。

业务人员可以看到图表变化，也可以直接用自然语言追问当前数据。

## 02 我为什么做这个项目

我想解决的是：BI 看板能展示数据，但不一定能帮助业务人员快速理解原因和下一步动作。

- 传统 BI 只能展示指标，业务人员还要自己解释原因。
- 直接用 LLM 分析 CSV 容易编造数字，也缺少稳定指标口径。
- 所以我设计了一个工作流：Python 负责确定性计算，LLM 负责解释结构化结果，Agent 负责任务识别和编排。

## 03 最终效果

- 一键切换不同 raw 数据源。
- 自动生成 RFM 分群和用户级 scored fact table。
- Power BI 刷新后图表同步变化。
- Streamlit 页面支持业务人员自然语言提问。

【截图 1：Streamlit 经营总览】

【截图 2：Power BI 总览页】

## 04 系统工作流

数据源场景库
→ 当前 raw 数据
→ Python Pipeline
→ Skill Layer
→ LLM 中文经营洞察
→ Power BI / Streamlit / Agent Workbench
→ Eval Harness 验证

- 数据源场景库：保存不同 demo case，用于模拟业务数据变化。
- 当前 raw 数据：作为 pipeline 每次运行的输入。
- Python Pipeline：负责数据清洗、指标计算、分群和文件输出。
- Skill Layer：把数据质量、分群、洞察生成等能力拆成可复用模块。
- LLM 中文经营洞察：基于结构化 summary 生成业务建议，不直接算数。
- Power BI / Streamlit / Agent Workbench：分别用于 BI 展示、业务页面和自然语言问答。
- Eval Harness：用测试集验证 Router / Agent 行为是否稳定。

## 05 核心模块

- 数据源切换模块  
  说明：用于展示不同业务场景下，数据变化如何驱动 BI 和 AI 洞察变化。

- Python Pipeline  
  说明：负责数据清洗、指标计算和输出文件生成。

- RFM 分群与 Weighted AOV  
  说明：用于识别高价值用户、潜力用户和流失风险用户。

- LLM Insight  
  说明：基于结构化 summary 生成中文经营建议，不让模型自由编数字。

- Power BI 看板  
  说明：展示客户结构、分群占比、Weighted AOV 和经营洞察。

- Streamlit Agent Workbench  
  说明：给业务人员输入自然语言问题，例如“这个数据的用户 RFM 是多少？”

- Eval Harness  
  说明：用测试集验证 Router / Agent 行为可靠性，避免项目只是偶然跑通。

## 06 我的主要贡献

- 设计 AI + BI 工作流，把数据处理、客户分群、AI 洞察和 BI 展示串成闭环。
- 搭建 Python 数据处理 pipeline，实现 raw 数据读取、清洗和输出生成。
- 设计 RFM 分群和 Weighted AOV 指标口径，支持客户价值分层。
- 接入 Mock / SiliconFlow 双模式，兼顾稳定演示和真实 API 展示。
- 设计 numeric validation / fallback，降低 LLM 编造业务数字和 API 失败风险。
- 构建 Streamlit 中文业务展示页，让 HR 和业务面试官能快速理解项目。
- 构建 Eval Harness 测试集，验证 Router / Agent 行为稳定性。

## 07 技术亮点

业务层：

- RFM 客户分层。
- 业务洞察中文化。
- 不同数据场景可演示。

AI 应用层：

- LLM 只解释结构化 summary。
- Agent Router 负责问题识别。
- Skill Layer 负责确定性执行。

工程保障层：

- mock/API 双模式。
- fallback。
- numeric validation。
- Eval Harness。
- trace / metadata。

## 08 面试展示流程

1. 打开 Streamlit 经营总览。
2. 展示 baseline 数据。
3. 切换到 apparel_vip_shift 数据源。
4. 运行 pipeline。
5. 页面和 Power BI 刷新后结果变化。
6. 询问 Agent：“这个数据的用户 RFM 是多少？”
7. 展示 Eval Harness 100% pass rate。

## 09 项目价值

这个项目适合 HR 和面试官快速判断我是否具备从业务问题到 AI 应用 Demo 的完整落地能力。

- 体现数据分析能力：能做客户分层、指标设计和 BI 输出。
- 体现 AI 应用落地能力：能把 LLM 接入具体业务流程，而不是只做聊天。
- 体现业务理解能力：能把客户运营问题转成留存、转化、召回和培育动作。
- 体现工程化和风险控制意识：有 pipeline、fallback、numeric validation、Eval Harness 和 metadata。
- 适合 AI 解决方案、AI 售前、BI 数据分析、技术顾问岗位。

## 10 项目链接

- GitHub：
- 飞书作品集：
- Streamlit 截图：
- Power BI 截图：
- Demo 视频：
