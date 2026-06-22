# AI 辅助型客户分群与 BI 决策系统

## 项目概述

本项目是一个面向电商客户运营场景的 **AI 辅助型 BI 决策系统**。项目结合 Python 数据处理、RFM 客户价值分析、SiliconFlow API 大模型洞察生成，以及 Power BI 可视化报表。

V3 版本将项目从传统的客户分群 Dashboard，升级为一个可重复运行的 BI 决策工作流：当 `data/raw/` 下的原始电商数据被替换后，只需要运行一条 Pipeline 命令，即可重新生成客户分群结果、AI 营销洞察、Power BI 可读取的洞察 CSV，以及可审计的运行 metadata。

系统同时支持 **Mock 模式** 和 **SiliconFlow API 模式**。V3 Pipeline 已完成真实 SiliconFlow API 验收，验收结果如下：

```text
requested_provider = siliconflow
provider = siliconflow
model = deepseek-ai/DeepSeek-V4-Flash
api_reached = True
validation_passed = True
fallback_used = False
error = None
raw_row_count = 1001
processed_customer_count = 1000
```

## V3 核心升级

- 从 `data/raw/` 自动读取原始电商 CSV 数据。
- 清洗 raw data，并重新生成 `data/processed/customer_segments.csv`。
- 生成 `data/processed/fact_user_behavior_scored.csv`，作为 Power BI 主图表推荐读取的用户级评分明细表。
- 使用 Python 计算 RFM、Weighted AOV、Value Proxy Score、客户分群和跨维度洞察。
- 在调用 LLM 前，先由 Python 生成 structured summary，确保业务数字有来源。
- 支持 SiliconFlow API 模式，用真实大模型生成业务表达和营销建议。
- 保留 Mock 模式，用于本地演示、离线测试和 fallback 输出。
- 引入 Numeric Validation 数字校验，减少 LLM 编造业务数字的风险。
- 当 API 调用失败或数字校验失败时，自动 fallback 到 Mock 输出。
- 输出 `outputs/run_metadata.json`，记录 provider、model、fallback 状态、validation 状态、raw 行数、客户数和生成文件。

## 业务背景

很多电商团队已经有 BI Dashboard，但 Dashboard 往往停留在“看图”和“看指标”阶段。业务人员仍然需要人工解释图表、识别客户风险、撰写分析结论，并设计运营动作。

本项目解决的问题是：把 BI 指标和 AI 辅助决策层连接起来。Python 负责计算所有业务指标，LLM 只负责把结构化结果转化为业务可读的洞察和营销建议。

项目目标不是替代分析师，而是减少重复性报告工作，帮助业务团队从“查看 Dashboard”推进到“准备决策方案”。

## 当前客户分群结果

当前 V3 运行结果读取 **1,001 行 raw data**，生成 **1,000 个 processed customers**。

| Segment | Customers | Share | Weighted AOV | Avg RFM Score | Action Priority |
|---|---:|---:|---:|---:|---|
| High-value Customers | 122 | 12.2% | 523.72 | 13.02 | Stabilize |
| Potential Customers | 292 | 29.2% | 1319.66 | 8.47 | Convert |
| Churn-risk Customers | 188 | 18.8% | 812.10 | 8.80 | Recover |
| Regular Retained Customers | 307 | 30.7% | 253.79 | 9.16 | Upsell |
| Other Customers | 91 | 9.1% | 289.51 | 6.02 | Nurture |

当前跨维度洞察包括：

- 51 岁左右女性客户的 Weighted AOV 最高，为 1001.62。
- Suburban 地区 Apparel 品类客户的 Weighted AOV 为 681.24。
- Top 10% 用户贡献了约 18.6% 的总消费额。
- Churn-risk Customers 最强品类偏好是 Home & Kitchen。
- High-value Customers 最强品类偏好是 Apparel。

## 技术栈

| 层级 | 工具 / 方法 |
|---|---|
| 数据层 | CSV, Python, pandas |
| 指标层 | RFM, Weighted AOV, Value Proxy Score |
| AI 层 | Mock provider, SiliconFlow API, structured prompt |
| 校验层 | 基于 Python structured summary 的 Numeric Validation |
| 输出层 | Markdown 报告, Power BI insight CSV, run metadata JSON |
| BI 层 | Power BI, DAX, 可刷新的 CSV 输出 |
| 治理层 | Fallback 机制, Human-in-the-loop 人工复核 |

## 项目结构

```text
AI-assisted-Customer-Segmentation-Dashboard/
|-- data/
|   |-- raw/
|   |-- processed/
|   `-- dictionary/
|-- docs/
|-- llm_agent/
|   |-- src/
|   |-- prompt_templates/
|   `-- outputs/
|-- outputs/
|-- portfolio/
|-- powerbi/
|-- sql/
|-- run_pipeline.py
|-- run_pipeline.ps1
|-- requirements.txt
|-- .env.example
|-- README.md
`-- README_CN.md
```

## 一键运行 Pipeline

V3 Pipeline 一次运行即可重新生成核心业务产物：

```text
data/raw/*.csv
        ->
Python 数据清洗与 RFM/value scoring
        ->
data/processed/fact_user_behavior_scored.csv
data/processed/customer_segments.csv
        ->
BI 主图表和 AI 洞察使用一致的分群人数
        ->
Structured summary
        ->
Mock provider 或 SiliconFlow API
        ->
outputs/segment_insights.md
outputs/powerbi_llm_insights.csv
outputs/run_metadata.json
```

生成文件包括：

- `data/processed/fact_user_behavior_scored.csv`
- `data/processed/customer_segments.csv`
- `outputs/segment_insights.md`
- `outputs/powerbi_llm_insights.csv`
- `outputs/run_metadata.json`

为了兼容早期 Power BI 原型，AI 洞察输出也会同步到 `llm_agent/outputs/`。

## Mock 模式与 SiliconFlow API 模式

系统支持两种 provider 模式。

**Mock 模式** 用于本地演示、稳定测试和 fallback 输出，不会调用任何外部 API。

```powershell
.venv\Scripts\python.exe run_pipeline.py --provider mock
```

**SiliconFlow API 模式** 会调用 `.env` 中配置的 SiliconFlow-compatible chat completion endpoint，并在接受结果前进行数字校验。

```powershell
.venv\Scripts\python.exe run_pipeline.py --provider siliconflow
```

## `.env` 配置方式

在项目根目录创建 `.env` 文件。不要提交 `.env`，因为其中包含 API Key。

SiliconFlow API 模式示例：

```env
LLM_PROVIDER=siliconflow
SILICONFLOW_API_KEY=your_api_key
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1
SILICONFLOW_MODEL=deepseek-ai/DeepSeek-V4-Flash
```

Mock 模式示例：

```env
LLM_PROVIDER=mock
```

也可以在运行时使用 `--provider mock` 或 `--provider siliconflow` 覆盖 `.env` 中的 provider。

## 本地运行方式

在 Windows PowerShell 或 Windows cmd 中运行：

```powershell
cd D:\chatgpt\AI-assisted-Customer-Segmentation-Dashboard
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

运行 Mock 模式：

```powershell
.venv\Scripts\python.exe run_pipeline.py --provider mock
```

运行 SiliconFlow API 模式：

```powershell
.venv\Scripts\python.exe run_pipeline.py --provider siliconflow
```

也可以使用 PowerShell helper：

```powershell
powershell -ExecutionPolicy Bypass -File run_pipeline.ps1
```

## 如何通过 `outputs/run_metadata.json` 判断是否真实调用 API

运行 Pipeline 后，打开 `outputs/run_metadata.json`。

真实 SiliconFlow API 调用成功时，应看到：

```json
{
  "requested_provider": "siliconflow",
  "provider": "siliconflow",
  "api_reached": true,
  "validation_passed": true,
  "fallback_used": false,
  "error": null
}
```

当前 V3 本机验收使用的模型和数据规模为：

```text
model = deepseek-ai/DeepSeek-V4-Flash
raw_row_count = 1001
processed_customer_count = 1000
```

如果 `requested_provider` 是 `siliconflow`，但 `provider` 变成了 `mock`，说明系统触发了 fallback。此时可以查看 `api_reached`、`validation_passed` 和 `error` 判断原因是 API 访问失败，还是 LLM 返回内容没有通过数字校验。

## AI 洞察输出

`data/processed/fact_user_behavior_scored.csv` 是 Power BI 主图表推荐读取的 fact 表。它每个用户一行，包含原始用户字段、RFM 分数、Weighted AOV、Value Proxy Score、英文分群名、中文分群名、业务角色和行动优先级。

`outputs/segment_insights.md` 包含：

- 项目运行时间
- 数据来源
- 核心客户分群结果
- 高价值客户洞察
- 流失风险客户洞察
- 营销建议
- Human Review 提醒
- Structured Summary Used By LLM

`outputs/powerbi_llm_insights.csv` 是 Power BI 可读取的洞察表，包含：

- `insight_title`
- `insight_text`
- `segment_name`
- `priority`
- `review_status`
- `generated_at`

`outputs/run_metadata.json` 记录：

- `run_time_utc`
- `raw_files`
- `raw_row_count`
- `processed_customer_count`
- `requested_provider`
- `provider`
- `model`
- `api_reached`
- `validation_passed`
- `fallback_used`
- `error`
- `retry_count`
- `error_type`
- `output_files`

## Power BI 联动

Power BI 应读取同一次 V3 Pipeline 重新生成的 CSV 输出：

- 主图表建议读取 `data/processed/fact_user_behavior_scored.csv`。
- AI Insight Box 继续读取 `outputs/powerbi_llm_insights.csv`。

这样可以保证饼图、柱状图、客户数和 AI 洞察文本使用同一套 pipeline 分群结果。

如果 Power BI 图表和 AI Insight Box 的分群人数不一致，通常说明 Power BI 主图表仍在读取旧表，例如 `Fact_User_Behavior`，或仍在使用旧分群字段。请将主图表数据源切换到 `data/processed/fact_user_behavior_scored.csv`，并使用其中的 `segment_name` 或 `segment_name_cn` 字段。

运行 Pipeline 后，打开：

```text
powerbi/AI_Customer_Segmentation_Dashboard.pbix
```

然后在 Power BI Desktop 中点击 **Home -> Refresh**。

AI 生成的内容用于辅助业务复核和决策准备，不用于自动执行营销活动。

## Numeric Validation 数字校验

Python 会先计算业务指标，并把 structured summary 传给 LLM。LLM 被要求只能使用 structured summary 中已有的业务数字。

Numeric Validation 会检查 LLM 返回内容中的业务数字，减少 unsupported business-number hallucination，也就是减少没有数据来源的业务数字编造。

当前数字校验设计包括：

- 允许章节编号和列表编号。
- 允许 structured summary 中已有数字的合理四舍五入。
- 允许百分比和小数形式在合理误差范围内转换。
- 重点检查客户数、占比、Weighted AOV、RFM Score、Value Proxy Score、Recency、Spending、Frequency 等业务数字上下文。
- 拦截明显不来自 Python 计算结果的新业务指标数字。

这个 guardrail 的目标是实用性：既降低 LLM 编造业务数字的风险，又不因为正常报告格式、标题编号或合理四舍五入而误判。

## Fallback 降级机制

即使 API 路径失败，Pipeline 仍然可以继续运行。

Fallback 可能发生在以下情况：

- API Key 缺失或无效。
- API endpoint 无法访问。
- Provider 返回无效响应。
- Numeric Validation 拒绝了不受支持的业务数字。

触发 fallback 时，`outputs/run_metadata.json` 会记录 `fallback_used = true`，并在 `error` 中保存原因。这样既保证 Power BI 和作品集演示仍有可用输出，也让 API 和校验状态可审计。

## Human-in-the-loop 人工复核

AI 生成的洞察和建议只作为决策辅助草稿。任何面向客户的营销活动执行前，都应由业务人员复核：

- 客户分群规则是否合理。
- raw data 是否新鲜、完整、可信。
- 推荐动作是否符合真实业务情况。
- 活动资格、合规要求和品牌表达是否正确。
- 库存、物流、客服和售后能力是否能支持活动。
- 最终活动方案应该通过、修改还是拒绝。

## 项目价值

本项目展示了 AI 如何增强 BI 决策工作流：

- 将静态 Dashboard 输出转化为可读的决策摘要。
- 减少人工撰写分析报告的重复劳动。
- 把客户分群结果连接到营销动作建议。
- 保证关键业务指标来自 Python 计算结果，而不是 LLM 自行编造。
- 让 API 调用、数字校验和 fallback 状态可追踪、可审计。
- 保留人工对最终业务决策的责任。

## 适配岗位

本项目适合用于 AI Solutions Intern、AI Product Intern、AI Pre-sales Intern、Data Analyst、BI Analyst、Technical Consultant 等岗位的作品集展示。

项目体现的能力包括：

- 数据清洗与客户分群流程设计。
- RFM 和客户价值指标建模。
- LLM API 集成与业务 guardrail 设计。
- Power BI 联动和可刷新洞察输出。
- Human-in-the-loop AI 治理意识。
- 用业务语言解释技术方案和项目价值。

## Future Work

以下内容是未来方向，不是 V3 已完成能力：

- RFM Skill Agent
- Safe SQL Skill
- Agentic BI workflow
- Evaluation Harness
- Trace Viewer
