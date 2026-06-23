# AI 辅助型客户分群与 BI 决策系统

副标题：基于 RFM、Power BI、中文 AI 洞察与 Agent Workbench 的经营分析工作流

一个面向电商客户运营场景的 AI + BI 作品集项目。系统支持切换不同 raw 数据源，通过 Python Pipeline 自动生成 RFM 分群、用户级 scored fact table、中文 AI 洞察，并联动 Power BI 和 Streamlit Agent Workbench 展示业务结果。

---

## 01｜面试官 30 秒速读版

### 项目一句话

这是一个把传统客户分群看板升级为 AI-assisted BI Workflow 的项目。

它让客户分群分析从“看图表”变成“可刷新、可解释、可追问、可评估”的经营分析流程。

### 解决的问题

- 传统 BI 只能展示指标，业务人员仍要自己解释原因和下一步动作。
- 直接用 LLM 分析 CSV 容易编造数字，指标口径不可控。
- 客户分群、AI 洞察、Power BI 展示和业务问答通常是割裂的。

### 我的解决方案

客户数据  
→ raw 数据源切换  
→ Python Pipeline 自动处理  
→ RFM 分群与 Weighted AOV 计算  
→ 中文 AI 经营洞察  
→ Power BI / Streamlit 展示  
→ Agent 业务问答  
→ Eval Harness 验证可靠性

### 核心结果

- 支持 baseline_original 与 apparel_vip_shift 两套数据场景切换。
- raw 数据变化后，RFM 分群、AI 洞察和 Power BI 图表可同步变化。
- Streamlit 页面支持业务人员提问：“这个数据的用户 RFM 是多少？”
- Eval Harness 覆盖 Router / Agent 测试，当前 Overall Pass Rate 为 100%。
- 系统支持 Mock / SiliconFlow API 双模式，并保留 fallback 与 numeric validation。

### 项目亮点

- 不是静态 BI 看板，而是可刷新、可追问的 AI BI 工作流。
- 不是简单 LLM 聊天，而是 Python Skill 负责确定性计算。
- Agent 负责识别问题和编排流程。
- Eval Harness 证明系统行为不是偶然跑通。
- 页面已中文化，更适合国内 HR 和业务面试官理解。

---

## 02｜项目截图

这里建议放 4 张核心截图，分别证明项目具备可视化、数据切换、业务问答和评估能力。

### 图 1：Streamlit 经营总览

【插入截图：Streamlit 经营总览】

说明：展示当前数据源场景、总用户数、最大客户分群、高价值用户数、流失风险用户数，以及分群柱状图 / 环形图 / Weighted AOV 图。

### 图 2：Agent 业务问答

【插入截图：业务问答：这个数据的用户 RFM 是多少？】

说明：展示业务人员可以直接用自然语言追问当前数据，系统基于 customer_segments.csv 生成中文经营分析，不让 LLM 自由编造数字。

### 图 3：Power BI 总览页

【插入截图：Power BI 总览页】

说明：展示 Power BI 读取 pipeline 输出文件后，客户分群、Weighted AOV、地区品类矩阵和 AI Insight Box 同步变化。

### 图 4：Eval Harness 结果

【插入截图：Eval Harness 100% pass rate】

说明：展示 Router / Agent 行为可通过测试集评估，不只是一次性 Demo。

---

## 03｜三张核心图

### 图 1：AI BI 工作流图

数据源场景库  
↓  
当前 raw 数据  
↓  
Python Pipeline  
↓  
Skill Layer  
↓  
RFM 分群 / Weighted AOV / Scored Fact Table  
↓  
中文 AI 洞察  
↓  
Power BI + Streamlit + Agent Workbench

说明：这张图说明系统如何从“原始业务数据”变成“可展示、可解释、可追问”的经营分析结果。

### 图 2：可靠性闭环图

Eval Dataset  
↓  
Router / Agent Eval  
↓  
Numeric Validation  
↓  
Fallback  
↓  
Trace / Metadata  
↓  
下一轮优化

说明：这张图说明项目不是只追求“能回答”，而是强调可评估、可降级、可复盘。

### 图 3：业务展示闭环图

业务人员问题  
↓  
Router Agent 判断意图  
↓  
Orchestrator 调用 Skill  
↓  
读取结构化数据  
↓  
生成中文经营回答  
↓  
页面展示回答与图表

说明：这张图说明业务人员不用理解代码，也可以通过页面问出经营问题。

---

## 04｜亮点卡片

### 亮点 1：不是静态 BI，而是 AI-assisted BI Workflow

说明：raw 数据变化后，pipeline 会重新生成分群、洞察和 BI 输出。  
为什么有价值：展示的是可复现工作流，不是截图型项目。

### 亮点 2：Python Skill 负责确定性计算

说明：RFM、Weighted AOV、分群人数等由 Python 计算。  
为什么有价值：避免 LLM 编造业务数字。

### 亮点 3：中文 AI 经营洞察

说明：LLM 只基于 structured summary 生成中文建议。  
为什么有价值：更适合国内 HR、业务人员和面试官理解。

### 亮点 4：Power BI 联动刷新

说明：Power BI 读取 processed CSV 和 insight CSV。  
为什么有价值：保留企业常用 BI 工具，同时增强解释能力。

### 亮点 5：Streamlit Agent Workbench

说明：业务人员可以输入“这个数据的用户 RFM 是多少？”  
为什么有价值：把 BI 从“看图表”升级为“可追问”。

### 亮点 6：Mock / API 双模式与 fallback

说明：mock 适合稳定展示，SiliconFlow 用于真实 LLM 调用。  
为什么有价值：现场演示稳定，同时具备真实 API 扩展能力。

### 亮点 7：Eval Harness

说明：用测试集验证 Router / Agent 行为。  
为什么有价值：证明项目不是偶然跑通，而是可评估。

---

## 05｜技术栈

数据处理：

- Python
- Pandas
- RFM segmentation
- Weighted AOV

AI 应用：

- LLM Insight
- Mock / SiliconFlow API
- Numeric validation
- Fallback

Agent 工作流：

- Router Agent
- Orchestrator
- Skill Layer
- Trace / Metadata

展示层：

- Power BI
- Streamlit Agent Workbench

评估：

- Eval Harness
- eval_dataset.csv
- eval_results.csv

---

## 06｜项目文件结构速览

data/demo_cases/  
保存不同业务数据场景，例如 baseline_original 和 apparel_vip_shift。

data/raw/  
pipeline 当前读取的 raw 数据源。

data/processed/  
保存 RFM 分群结果、用户级 scored fact table 和交叉洞察。

outputs/  
保存中文 AI 洞察、Power BI Insight CSV 和 run metadata。

skills/  
封装数据质量检查、RFM 分群、洞察生成和 Power BI 输出。

agents/  
封装 Router Agent、Orchestrator 和 Trace Logger。

eval/  
保存测试集、评估脚本和评估结果。

streamlit_agent_app.py  
面向业务展示的 Streamlit Agent Workbench 页面。

---

## 07｜项目结果

### 结果 1：数据源切换后，分群结果可变化

baseline_original 中：

- 一般保持用户：307
- 潜力用户：292
- 流失风险用户：188
- 高价值用户：122
- 其他用户：91

apparel_vip_shift 中：

- 高价值用户：320
- 流失风险用户：270
- 潜力用户：240
- 其他用户：160
- 一般保持用户：10

说明：这证明项目不是静态看板，而是可以通过 raw 数据变化驱动分析结果变化。

### 结果 2：AI 洞察中文化

示例：

- 高价值用户 - 稳定留存
- 潜力用户 - 转化提升
- 流失风险用户 - 召回修复

说明：洞察内容更适合中文业务展示，不再像技术调试输出。

### 结果 3：Eval Harness 通过率

当前测试集：

- Total cases：15
- Intent accuracy：100%
- Tool selection accuracy：100%
- Risk level accuracy：100%
- Overall pass rate：100%

说明：Eval Harness 用于验证 Agent 行为可靠性，避免项目只是一次性跑通。

---

## 08｜我在项目中负责的工作

- 设计电商客户运营场景下的 AI + BI 分析工作流。
- 构建 raw 数据源切换机制，支持多业务场景演示。
- 搭建 Python Pipeline，自动生成分群结果和 Power BI 输出文件。
- 设计 RFM 客户分群与 Weighted AOV 指标口径。
- 构建 Skill Layer，将确定性计算与 LLM 解释分离。
- 接入 Mock / SiliconFlow 双模式，并保留 fallback。
- 设计 numeric validation，降低 LLM 编造业务数字的风险。
- 构建 Router Agent / Orchestrator，实现自然语言业务问题识别。
- 构建 Eval Harness，用测试集验证 Agent 行为可靠性。
- 搭建中文 Streamlit Agent Workbench，面向 HR 和业务面试官展示。
- 整理 GitHub README、飞书作品集、简历 bullet 和面试问答文档。

---

## 09｜项目学习收获

这个项目让我真正理解到，AI 应用不是把大模型接到页面上就结束了。

如果要进入业务场景，系统必须同时具备：

- 稳定的数据处理链路。
- 清晰的指标口径。
- 可解释的业务洞察。
- 可追问的交互入口。
- 可评估的测试机制。
- 可降级的容错设计。

我的最大收获是：LLM 不应该直接替代所有计算，而应该和确定性工程模块协作。

Python 负责算得准，LLM 负责讲得清，Agent 负责编排流程，Eval Harness 负责验证可靠性。

---

## 10｜面试官 30 秒介绍稿

这是一个面向电商客户运营场景的 AI 辅助 BI 决策系统。它不是静态 Power BI 看板，而是一个从 raw 数据源切换、Python 自动处理、RFM 客户分群、中文 AI 洞察生成，到 Power BI 和 Streamlit 页面联动展示的完整分析工作流。

在这个项目里，我没有让 LLM 直接计算业务数字，而是用 Python Skill 负责 RFM、Weighted AOV 和分群统计，让 LLM 只解释结构化结果。同时我加入了 Router Agent、Eval Harness、fallback 和 numeric validation，让系统具备可追问、可评估、可降级的能力。这个项目主要体现的是 AI 应用落地、BI 数据分析和业务解决方案设计能力。

---

## 11｜一句话总结

AI 辅助型客户分群与 BI 决策系统，是一个将 raw 数据源切换、Python 数据处理、RFM 分群、中文 AI 洞察、Power BI 刷新和 Agent 业务问答串联起来的 AI-assisted BI Workflow 作品集项目。
