# 截图清单

## 1. GitHub README 首页

- 截图内容：README 顶部标题、一句话介绍、架构图和功能亮点。
- 用途：让 HR 或面试官 30 秒内理解项目定位。
- 放在飞书哪一节：项目标题 / 项目定位。

## 2. Power BI 总览页

- 截图内容：客户分群图表、Weighted AOV、筛选器和 AI Insight Box。
- 用途：证明项目有 BI 可视化输出，不只是 Python 脚本。
- 放在飞书哪一节：最终效果 / Power BI 联动。

## 3. Streamlit 经营总览

- 截图内容：顶部 KPI cards、分群人数柱状图、分群占比图、Weighted AOV 图。
- 用途：展示业务展示型 Agent Workbench。
- 放在飞书哪一节：最终效果 / 面试官可以如何体验。

## 4. Streamlit 业务问答

- 截图内容：输入“这个数据的用户 RFM 是多少？”后的业务回答、关键指标表或图表。
- 用途：展示自然语言入口和 Agent 编排能力。
- 放在飞书哪一节：核心模块 / 展示流程。

## 5. Streamlit 洞察输出

- 截图内容：中文 insight cards，包括标题、关联分群、复核状态和完整正文。
- 用途：展示 LLM 经营洞察的业务可读性。
- 放在飞书哪一节：最终效果 / 业务价值。

## 6. Eval Harness 运行结果

- 截图内容：命令行输出 Total cases、Intent accuracy、Overall pass rate。
- 用途：证明 Agent 行为可测试，不是一次性跑通。
- 放在飞书哪一节：技术亮点 / Eval Harness。

## 7. CMD pipeline 成功输出

- 截图内容：`run_pipeline.py --provider mock` 成功输出，包括 Generated files。
- 用途：证明 raw 数据变化后可以一键重新生成结果。
- 放在飞书哪一节：展示流程 / 技术亮点。

## 8. demo case 切换前后对比

- 截图内容：baseline_original 和 apparel_vip_shift 两次运行后的分群人数或 Streamlit KPI 对比。
- 用途：证明项目不是静态截图，数据源变化会带来输出变化。
- 放在飞书哪一节：为什么做这个项目 / 最终效果。

## 9. run_metadata 摘要

- 截图内容：`outputs/run_metadata.json` 中 provider、api_reached、validation_passed、fallback_used、raw_row_count、processed_customer_count。
- 用途：展示可审计性和 API / fallback 状态。
- 放在飞书哪一节：技术亮点 / 风险控制。

## 10. 技术细节开发者模式

- 截图内容：Streamlit 底部折叠的开发者模式，展示 Intent、Tools、Risk Level、Eval 详细结果。
- 用途：面向技术面试官说明 Agent 和 Eval 的可观测性。
- 放在飞书哪一节：技术深挖 / 面试官可以如何体验。

## 截图建议

- 每张图尽量只表达一个信息点。
- 优先截中文业务页面，不要大面积截代码。
- CMD 截图保留关键命令和成功结果即可。
- Power BI 和 Streamlit 尽量使用同一份 demo 数据，避免数字不一致。
- GitHub / 飞书正文里配 4-6 张核心图即可，详细技术图可以放到附录。
