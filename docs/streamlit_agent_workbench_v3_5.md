# V3.5 Streamlit Agent Workbench

## 定位

V3.5 在现有 Router Agent、Orchestrator、Skill Layer 和 Eval Harness 之上，新增一个轻量级业务人员前端页面。

这个页面面向 HR 展示、面试讲解和作品集复盘。业务解释、页面说明和 Agent 回答以中文为主；`Provider`、`Intent`、`Tools`、`Risk Level`、`Dry Run`、`Trace`、命令、文件名和稳定字段保留英文，便于展示工程边界和系统可观测性。

## 页面功能

- 自然语言业务问答，例如：`这个数据的用户 RFM 是多少？`
- RFM 分群摘要展示，数据来自 `data/processed/customer_segments.csv`
- Demo Case 选择：`baseline_original`、`apparel_vip_shift`
- Provider 选择：`mock`、`siliconflow`，默认 `mock`
- 显式按钮触发数据源切换、pipeline 运行和 Eval Harness
- Power BI 输出预览：`outputs/powerbi_llm_insights.csv`
- run metadata 摘要：`outputs/run_metadata.json`
- Eval 结果摘要：`eval/eval_results.csv`
- 如本地存在 `logs/agent_runs.jsonl`，展示最近 5 条 Trace

## 启动命令

在项目根目录运行：

```cmd
.venv\Scripts\streamlit.exe run streamlit_agent_app.py
```

也可以使用：

```cmd
.venv\Scripts\python.exe -m streamlit run streamlit_agent_app.py
```

页面默认使用 `mock` provider。只有当用户选择 `siliconflow` 并点击 `运行分析流水线` 时，才会尝试真实 LLM API 调用。

## 页面风格

页面采用轻量咨询报告风格：

- 白底
- 深蓝 / 墨蓝作为主色
- 细灰色分割线
- 高密度但不花哨的信息布局
- 顶部 overview cards 展示当前数据源场景、Provider、Pipeline 状态和 Eval Pass Rate
- 卡片式区域用于说明工作流边界

目标是让面试官快速理解：这是一个可运行、可验证、可解释的 AI BI 决策工作流，而不是单纯的 Notebook 或静态 Dashboard。

## 面试展示流程

1. 打开 Streamlit 页面。
2. 在 `业务问答` 中询问：`这个数据的用户 RFM 是多少？`
3. 展示 `Intent = rfm_summary_question`，说明回答读取的是 Python 生成的 CSV，不由 LLM 计算数字。
4. 询问：`对比 baseline_original 和 apparel_vip_shift 的分群变化`
5. 展示 Orchestrator 读取 demo case 的汇总表并给出中文业务解释。
6. 询问：`如果我要切换到 apparel_vip_shift 并刷新 Power BI，需要执行什么？`
7. 展示默认 dry-run，不会修改文件，只给出计划命令。
8. 如需真实演示，再通过 sidebar 按钮应用数据源场景、运行 pipeline、运行 Eval Harness。
9. 切到 `Power BI 输出`，说明 Power BI refresh 后读取同一套 pipeline 输出。

## 安全边界

页面不会自动执行数据切换或 pipeline。会修改本地输出的操作只通过按钮触发：

- `应用数据源场景`
- `运行分析流水线`
- `运行评估测试集`

`业务问答` tab 中的 Agent 请求默认 `dry_run=True`，因此数据切换类问题只会解释将要执行什么，不会直接修改文件。

## 架构关系

- Router Agent 负责确定性 intent 识别，不调用 LLM。
- Orchestrator 负责任务编排和白名单能力调用。
- Skill Layer 负责确定性计算、RFM 分群、LLM 洞察生成和 Power BI 文件检查。
- Eval Harness 负责测试 Router / Orchestrator 的稳定性和安全边界。
- Streamlit 只是轻量展示层，不承载生产级服务治理。

LLM 不负责算数。RFM 指标、分群人数、Weighted AOV、Avg RFM Score 等业务数字都来自 Python 生成的 CSV 和 structured summary。

## 为什么使用 Streamlit

Streamlit 适合快速构建本地展示页面，便于作品集和面试演示。它不需要 React、FastAPI、数据库、Docker 或复杂前端工程。

如果未来企业落地，可以升级为：

- FastAPI service layer
- React frontend
- 权限与审计
- 持久化 Trace 存储
- 生产监控和告警

这些属于 future work，不是 V3.5 已实现能力。
