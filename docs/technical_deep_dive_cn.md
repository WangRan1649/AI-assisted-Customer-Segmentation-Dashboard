# 技术深挖文档

## 1. Pipeline

`run_pipeline.py` 是项目主入口。它调用 `skills.workflow_skill.run_ai_bi_workflow()`，按顺序执行：

- raw 数据质量检查
- RFM 分群
- LLM / Mock 洞察生成
- Power BI 输出文件检查
- 写入 `outputs/run_metadata.json`

Pipeline 的核心目标是让 raw 数据源变化后，可以一键重新生成：

```text
data/processed/fact_user_behavior_scored.csv
data/processed/customer_segments.csv
outputs/powerbi_llm_insights.csv
outputs/segment_insights.md
outputs/run_metadata.json
```

## 2. Skill Layer

`skills/` 将确定性能力拆成独立模块：

- `data_quality_skill.py`：检查 raw 文件、字段和行数。
- `rfm_segmentation_skill.py`：运行 RFM 分群，生成 processed CSV。
- `insight_generation_skill.py`：生成 structured summary，调用 Mock / API，输出洞察文件。
- `powerbi_export_skill.py`：检查 Power BI 所需输出是否存在且可读。
- `workflow_skill.py`：编排整个 AI BI workflow。

这样做的价值是：未来 Agent 不需要直接改底层计算逻辑，而是调用边界清晰的 Skill。

## 3. Router Agent

`agents/router_agent.py` 是确定性 intent router，不调用 LLM。它根据用户问题识别：

- `list_demo_cases`
- `compare_demo_cases`
- `workflow_status`
- `run_workflow`
- `explain_powerbi_workflow`
- `rfm_summary_question`
- `unknown`

对于删除、清空、reset、覆盖等高风险请求，Router 会标记 high risk 或拒绝。

## 4. Orchestrator

`agents/orchestrator_agent.py` 根据 Router 的 AgentPlan 调用白名单能力。它支持：

- 列出 demo cases
- 对比两个 demo case 的 `customer_segments.csv`
- 读取 `outputs/run_metadata.json`
- 解释 Power BI 工作流
- 回答 RFM 摘要问题
- 在显式 execute 情况下运行受控 workflow

Orchestrator 不执行任意 shell 命令，不访问项目根目录外路径，默认 dry-run。

## 5. Numeric Validation

Numeric validation 的目标是降低 LLM 编造关键业务数字的风险。

核心规则：

- structured summary 中出现过的数字是允许的。
- 允许合理四舍五入和百分比 / 小数转换。
- 允许标题序号等非业务数字。
- 拦截明显新增的客户数、占比、AOV、RFM Score、消费金额等业务指标数字。

这样既保留 guardrail，又避免因为正常标题编号或格式化导致误判。

## 6. Fallback

LLM provider 支持 `mock` 和 `siliconflow`。

Fallback 触发场景：

- API key 缺失或配置错误
- 网络超时
- HTTP error
- response error
- numeric validation failed

Fallback 后系统仍然生成可用输出，并在 `outputs/run_metadata.json` 中记录：

```json
{
  "api_reached": true,
  "validation_passed": false,
  "fallback_used": true,
  "error_type": "validation_error"
}
```

## 7. Trace

`agents/trace_logger.py` 会把 Agent run 写入 `logs/agent_runs.jsonl`。Trace 记录 run_id、timestamp、question、intent、selected_tools、dry_run、status 和 error。

日志用于本地可观测性，不作为作品集提交内容。

## 8. Eval Harness

`eval/` 包含：

- `eval_dataset.csv`
- `run_eval.py`
- `metrics.py`
- `eval_results.csv`

Eval Harness 测试：

- intent accuracy
- tool selection accuracy
- risk level accuracy
- dry-run accuracy
- refusal accuracy
- answer contains accuracy
- overall pass rate

它验证的是本地 Agent / Orchestrator 行为，不测试真实 LLM API。

## 9. Streamlit Workbench

`streamlit_agent_app.py` 是业务展示型前端，包括：

- 经营总览：KPI cards、分群人数图、占比图、Weighted AOV 图
- 业务问答：自然语言输入，展示业务回答和关键指标
- 洞察输出：中文 AI insight cards
- 技术细节：折叠的开发者模式，展示 intent、tools、metadata、eval 和 trace

默认页面不展示 debug console 风格信息，适合 HR 和业务面试官快速理解项目价值。

## 10. Power BI Integration

Power BI 主图表推荐读取：

```text
data/processed/fact_user_behavior_scored.csv
```

AI Insight Box 读取：

```text
outputs/powerbi_llm_insights.csv
```

这样 BI 图表和 AI 洞察来自同一次 pipeline，避免分群人数不一致。

## 11. 为什么当前版本不用 LangChain / LangGraph

当前项目目标是作品集 Demo 和可解释的轻量 Agent workflow，不需要复杂框架。

不使用 LangChain / LangGraph 的原因：

- 当前 intent routing 可以用确定性规则稳定完成。
- Skill 调用边界简单，不需要复杂状态图。
- 避免引入大型依赖，降低面试现场运行风险。
- 重点展示业务闭环、工程边界和可评估性，而不是框架堆叠。

未来如果要做多步骤复杂 Agent、工具回调、任务状态管理和多人协作流程，可以再引入更完整的 Agent 框架。

## 12. Future Enterprise Upgrade

真实企业落地可以继续升级：

- FastAPI 服务化
- React 企业前端
- 用户权限和数据权限
- 任务调度和运行历史
- 数据质量规则管理
- SQL sandbox
- 指标口径中心
- Trace Viewer
- LLM evaluation dashboard
- 监控、告警和审计
- 对接 CRM / CDP / 数据仓库

当前版本定位是作品集原型系统，重点展示端到端 AI BI workflow 的方案能力。
