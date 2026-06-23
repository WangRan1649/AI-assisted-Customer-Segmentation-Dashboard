# AI 应用层求职作品集｜Ran Wang

## 1｜个人定位

我是一名软件工程专业本科生，目标方向是：

* AI 解决方案 / AI Solutions
* AI 售前 / AI Pre-sales
* LLM 应用开发 / LLM Application
* 技术顾问 / Technical Consultant
* AI 产品运营 / AI Product Operations
* BI / 数据分析相关岗位

我关注的不是底层大模型训练，而是 **如何把 AI 接入真实业务流程**，让它成为可用、可评估、可解释、可复盘的业务系统。

我目前重点积累的能力包括：

* RAG 知识库问答
* LLM API 调用
* Source Grounding
* Evaluation / Eval Harness
* Guardrails
* Tracing / Trace Viewer
* Human Review
* AI + BI 业务洞察
* Power BI 数据可视化
* Agent Workflow / Agent Workbench
* Skill Layer / Tool Registry
* Fallback / Error Handling

我的作品集重点展示：
**我如何把大模型能力转化为真实业务场景中的 AI 应用工作流，而不是只做一个简单的 ChatGPT 包装。**

---

## 2｜项目导航

## 01｜AI Pre-sales Copilot

### 基于 RAG + Agent Workbench 的 B2B SaaS 售前知识库助手

这是一个面向 B2B SaaS 售前场景的 AI 应用项目。系统可以基于产品文档检索资料，生成带来源的客户回答，并通过 Guardrails、Tracing、Eval 和 Agent Workflow 提升回答可靠性。

### 项目关键词

* RAG
* Chroma
* sentence-transformers
* LLM Client
* Source Grounding
* Guardrails
* Tracing
* Evaluation
* Agent Workbench
* Tool Registry
* Safe Executor
* Risk Review
* Critic Agent
* Memory Compression
* Human Review
* Streamlit Demo

### 项目解决的问题

售前团队经常需要回答客户关于产品功能、部署方式、集成能力、安全合规、价格、SLA 和客户案例的问题。

传统方式下，售前人员需要反复查产品文档，效率低；如果直接问大模型，又容易出现无依据回答、编造价格、虚构客户案例等风险。

### 我的解决方案

我构建了一个 AI Pre-sales Copilot：

客户问题
→ 检索产品文档
→ 生成带来源回答
→ Guardrails 拦截高风险问题
→ Risk Review / Critic 检查回答风险
→ Email Agent 生成跟进草稿
→ Trace 记录完整链路
→ Eval 验证系统可靠性
→ Streamlit 页面展示 Agent 工作流

### 项目亮点

* 不是简单调用 LLM，而是基于 RAG 的售前知识库问答系统
* 使用 Chroma + sentence-transformers 实现语义检索
* 支持 source-grounded answer，回答可追溯到产品文档
* 用 Retrieval Eval、Answer Eval、Guardrail Eval 评估系统质量
* 用 Guardrails 拦截价格、合规、SLA、客户案例等高风险问题
* 用 Tracing 记录 question、sources、raw answer、guardrail rule、final answer 和 latency
* 升级 Agent Workbench 后，支持 Planner、Retrieval、Risk Review、Critic、Email、Memory 等模块展示
* 具备 Tool Registry、Safe Executor、Memory Compression、Trace Viewer、Human Review 等 Agentic Workflow 设计
* Retrieval source hit rate 从 93.33% 提升到 100%
* Guarded answer eval pass rate 从 60% 提升到 80%
* Refusal accuracy 从 40% 提升到 80%
* Agent Eval 已完成稳定测试，验证多 Agent 工作流可运行、可追踪、可评估

### 项目链接

01｜AI Pre-sales Copilot 项目 Case Study

---

## 02｜AI 辅助型客户分群与 BI 决策系统

### 基于 RFM、Power BI、中文 AI 洞察与 Agent Workbench 的经营分析工作流

这是一个面向电商客户运营场景的 AI + BI 作品集项目。系统支持切换不同 raw 数据源，通过 Python Pipeline 自动生成 RFM 分群、用户级 scored fact table、中文 AI 洞察，并联动 Power BI 和 Streamlit Agent Workbench 展示业务结果。

### 项目关键词

* Power BI
* Python
* Pandas
* RFM
* Customer Segmentation
* Weighted AOV
* LLM Insight
* AI Insight Box
* Human-in-the-loop
* Streamlit Agent Workbench
* Skill Layer
* Router Agent
* Orchestrator
* Eval Harness
* Numeric Validation
* Fallback
* Mock / SiliconFlow API

### 项目解决的问题

传统 BI 看板可以展示指标，但业务人员仍然需要自己解释原因、整理洞察和设计下一步运营动作。

如果直接用 LLM 分析 CSV，又容易出现编造数字、指标口径不清、结果不可评估的问题。

所以我设计了一个 AI-assisted BI Workflow：

raw 数据源切换
→ Python Pipeline 自动处理
→ RFM 分群与 Weighted AOV 计算
→ 用户级 scored fact table 输出
→ 中文 AI 经营洞察生成
→ Power BI 图表刷新
→ Streamlit Agent Workbench 业务问答
→ Eval Harness 验证 Agent 行为可靠性

### 项目亮点

* 不是静态 Power BI 看板，而是可刷新、可追问、可评估的 AI BI 工作流
* 支持 baseline_original 与 apparel_vip_shift 两套数据场景切换
* raw 数据变化后，RFM 分群、AI 洞察和 Power BI 图表可同步变化
* 使用 Python Pipeline 自动生成客户分群、用户级 scored fact table 和 Power BI 可读取 CSV
* 使用 RFM、Weighted AOV 等指标识别高价值用户、潜力用户和流失风险用户
* LLM 不直接计算业务数字，只基于 structured summary 生成中文经营洞察
* 保留 numeric validation，降低 LLM 编造业务数字的风险
* 支持 Mock / SiliconFlow API 双模式，兼顾稳定演示和真实 API 调用
* 构建 Skill Layer，将数据质量检查、RFM 分群、洞察生成、Power BI 输出封装成可复用能力
* 构建 Router Agent / Orchestrator，支持自然语言业务问题识别与流程编排
* 构建 Eval Harness，用测试集验证 Router / Agent 行为可靠性
* Streamlit 页面已中文化，并采用更适合业务展示的经营总览、业务问答、洞察输出结构

### 当前项目结果

数据源切换前后，分群结果可明显变化：

baseline_original 场景：

* 一般保持用户：307
* 潜力用户：292
* 流失风险用户：188
* 高价值用户：122
* 其他用户：91

apparel_vip_shift 场景：

* 高价值用户：320
* 流失风险用户：270
* 潜力用户：240
* 其他用户：160
* 一般保持用户：10

Eval Harness 当前结果：

* Total cases：15
* Intent accuracy：100%
* Tool selection accuracy：100%
* Risk level accuracy：100%
* Overall pass rate：100%

### 项目链接

02｜AI 辅助型客户分群与 BI 决策系统 Case Study

---

## 3｜我的 AI 应用层能力地图

我的能力不是单点技术，而是围绕“业务问题 → AI 应用工作流 → 可评估交付”的完整链路展开。

业务问题理解
↓
数据 / 文档处理
↓
RAG / BI / LLM API
↓
Skill Layer 确定性执行
↓
LLM 生成业务解释
↓
Guardrails / Numeric Validation / Fallback
↓
Trace / Eval Harness / Human Review
↓
业务决策支持

我希望长期深耕的方向是：

* AI Solutions
* AI Pre-sales
* LLM Application
* Technical Consultant
* AI Product / Operations
* BI + AI 业务分析

---

## 4｜作品集重点能力总结

### 业务理解能力

我不是只做技术 Demo，而是会先思考业务场景：

* 售前团队如何回答客户问题？
* 客户运营如何识别高价值用户和流失风险用户？
* BI 看板如何从“展示指标”升级为“辅助决策”？
* AI 输出如何被业务人员理解、复核和追踪？

### AI 应用落地能力

我重点关注 AI 如何接入真实流程：

* RAG 检索产品文档
* LLM 生成带来源回答
* LLM 生成中文经营洞察
* Agent 识别用户问题并编排工具
* Streamlit / Power BI 展示业务结果

### 工程化与可靠性意识

我没有只追求“能回答”，而是加入了：

* Eval Dataset
* Retrieval Eval
* Answer Eval
* Guardrail Eval
* Eval Harness
* Guardrails
* Fallback
* Numeric Validation
* Tracing
* Metadata
* Human Review

### 面试可讲亮点

我可以清楚解释：

* 为什么不能让 LLM 直接算业务数字
* 为什么 RAG 需要 Source Grounding
* 为什么 BI 看板需要 AI 洞察层
* 为什么 Agent 需要 Router / Orchestrator / Skill Layer
* 为什么 Demo 系统也需要 Eval Harness
* 如何把 AI 项目从“能跑”升级到“可评估、可保护、可诊断”

---

## 5｜一句话总结

我不是只会调用 ChatGPT，而是在学习如何把大模型接入真实业务流程。

我的作品集重点展示：
**如何通过 RAG、BI、LLM API、Agent Workflow、Evaluation、Guardrails、Tracing 和 Human Review，让 AI 应用更可靠、更可解释、更接近业务落地。**
