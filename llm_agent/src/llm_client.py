from __future__ import annotations

import json
import os
import re
import socket
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    load_dotenv = None


ROOT_DIR = Path(__file__).resolve().parents[2]

DEFAULT_PROVIDER = "mock"
DEFAULT_SILICONFLOW_BASE_URL = "https://api.siliconflow.cn/v1"
DEFAULT_SILICONFLOW_MODEL = "Qwen/Qwen2.5-7B-Instruct"
MOCK_MODEL = "local-structured-mock-v3"
SILICONFLOW_TIMEOUT_SECONDS = 90
SILICONFLOW_MAX_READ_TIMEOUT_RETRIES = 2
SILICONFLOW_RETRY_SLEEP_SECONDS = 2

NUMBER_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_])(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?%?(?![A-Za-z0-9_])"
)
ALLOWED_STRUCTURAL_NUMBERS = {
    0.0,
    1.0,
    2.0,
    3.0,
    4.0,
    5.0,
    10.0,
    20.0,
    25.0,
    45.0,
    100.0,
}
BUSINESS_NUMBER_KEYWORDS = {
    "%",
    "aov",
    "average",
    "avg",
    "campaign",
    "churn",
    "count",
    "cny",
    "customer",
    "customers",
    "day",
    "days",
    "frequency",
    "login",
    "monetary",
    "percent",
    "percentage",
    "purchase",
    "recency",
    "revenue",
    "rfm",
    "row",
    "rows",
    "score",
    "share",
    "spending",
    "total",
    "user",
    "users",
    "value",
    "¥",
    "客户",
    "用户",
    "占比",
    "比例",
    "客单价",
    "加权客单价",
    "评分",
    "分数",
    "分群",
    "金额",
    "消费",
    "总消费",
    "购买",
    "频次",
    "复购",
    "活跃",
    "流失",
    "召回",
    "留存",
    "年龄",
    "岁",
    "天",
    "行",
    "数据",
    "指标",
    "价值",
    "收入",
    "贡献",
    "排名",
    "第",
}


@dataclass
class LLMResponse:
    text: str
    requested_provider: str
    provider: str
    model: str
    api_reached: bool
    validation_passed: bool
    fallback_used: bool
    error: str | None
    retry_count: int
    error_type: str | None


class LLMProviderError(RuntimeError):
    def __init__(
        self,
        message: str,
        api_reached: bool,
        error_type: str,
        retry_count: int = 0,
    ) -> None:
        super().__init__(message)
        self.api_reached = api_reached
        self.error_type = error_type
        self.retry_count = retry_count


def load_environment() -> None:
    if load_dotenv is None:
        return

    env_path = ROOT_DIR / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        load_dotenv()


def normalize_provider(provider: str | None) -> str:
    value = (provider or os.getenv("LLM_PROVIDER") or DEFAULT_PROVIDER).strip().lower()
    if value in {"", "none"}:
        return DEFAULT_PROVIDER
    return value


def get_siliconflow_config() -> tuple[str, str, str]:
    api_key = (os.getenv("SILICONFLOW_API_KEY") or "").strip()
    base_url = (os.getenv("SILICONFLOW_BASE_URL") or DEFAULT_SILICONFLOW_BASE_URL).strip().rstrip("/")
    model = (os.getenv("SILICONFLOW_MODEL") or DEFAULT_SILICONFLOW_MODEL).strip()

    if not api_key:
        raise LLMProviderError(
            "SILICONFLOW_API_KEY is not set.",
            api_reached=False,
            error_type="config_error",
        )

    return api_key, base_url, model


def is_timeout_error(exc: BaseException) -> bool:
    if isinstance(exc, (TimeoutError, socket.timeout)):
        return True

    if isinstance(exc, urllib.error.URLError):
        reason = exc.reason
        if isinstance(reason, (TimeoutError, socket.timeout)):
            return True
        return "timed out" in str(reason).lower()

    return "timed out" in str(exc).lower()


def call_siliconflow_once(request: urllib.request.Request) -> str:
    with urllib.request.urlopen(request, timeout=SILICONFLOW_TIMEOUT_SECONDS) as response:
        return response.read().decode("utf-8")


def call_siliconflow(prompt: str) -> tuple[str, str, int]:
    api_key, base_url, model = get_siliconflow_config()
    url = f"{base_url}/chat/completions"

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "你是一个 BI 决策工作流助手，必须使用中文输出。只能使用用户提供的 "
                    "structured summary。不要编造指标、百分比、分群规模、客户数、品类、"
                    "年龄、AOV、RFM 分数、Value Proxy Score、频次、最近活跃、消费金额、"
                    "活动周期、折扣率或排名。业务数字必须从 structured summary 中复制，"
                    "不要估算、重算或补充。如果缺少某个细节，请说明需要人工复核。"
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
        "max_tokens": 1800,
    }

    request = urllib.request.Request(
        url=url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    response_body = ""
    retry_count = 0

    for attempt in range(SILICONFLOW_MAX_READ_TIMEOUT_RETRIES + 1):
        try:
            response_body = call_siliconflow_once(request)
            retry_count = attempt
            break
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise LLMProviderError(
                f"SiliconFlow HTTP {exc.code}: {detail}",
                api_reached=True,
                error_type="http_error",
                retry_count=attempt,
            ) from exc
        except urllib.error.URLError as exc:
            if is_timeout_error(exc) and attempt < SILICONFLOW_MAX_READ_TIMEOUT_RETRIES:
                time.sleep(SILICONFLOW_RETRY_SLEEP_SECONDS)
                continue

            raise LLMProviderError(
                f"SiliconFlow connection error: {exc.reason}",
                api_reached=False,
                error_type="timeout" if is_timeout_error(exc) else "connection_error",
                retry_count=attempt,
            ) from exc
        except (TimeoutError, socket.timeout) as exc:
            if attempt < SILICONFLOW_MAX_READ_TIMEOUT_RETRIES:
                time.sleep(SILICONFLOW_RETRY_SLEEP_SECONDS)
                continue

            raise LLMProviderError(
                f"SiliconFlow read timeout after {SILICONFLOW_TIMEOUT_SECONDS} seconds.",
                api_reached=False,
                error_type="timeout",
                retry_count=attempt,
            ) from exc
    else:
        raise LLMProviderError(
            "SiliconFlow request failed before receiving a response.",
            api_reached=False,
            error_type="connection_error",
            retry_count=SILICONFLOW_MAX_READ_TIMEOUT_RETRIES,
        )

    try:
        data = json.loads(response_body)
    except json.JSONDecodeError as exc:
        raise LLMProviderError(
            "SiliconFlow response was not valid JSON.",
            api_reached=True,
            error_type="response_error",
            retry_count=retry_count,
        ) from exc

    choices = data.get("choices") or []
    if not choices:
        raise LLMProviderError(
            f"SiliconFlow response did not include choices: {response_body[:500]}",
            api_reached=True,
            error_type="response_error",
            retry_count=retry_count,
        )

    message = choices[0].get("message") or {}
    content = (message.get("content") or "").strip()
    if not content:
        raise LLMProviderError(
            "SiliconFlow response content was empty.",
            api_reached=True,
            error_type="response_error",
            retry_count=retry_count,
        )

    return content, model, retry_count


def parse_number(token: str) -> float:
    return float(token.strip().rstrip("%").replace(",", ""))


def numeric_tokens(text: str) -> set[float]:
    values: set[float] = set()
    for match in NUMBER_PATTERN.findall(text):
        try:
            values.add(round(parse_number(match), 4))
        except ValueError:
            continue
    return values


def summary_numeric_tokens(summary: dict[str, Any]) -> set[float]:
    values = set(ALLOWED_STRUCTURAL_NUMBERS)
    summary_text = json.dumps(summary, ensure_ascii=False)
    summary_values = numeric_tokens(summary_text)

    for value in summary_values:
        values.add(value)
        values.add(round(value, 2))
        values.add(round(value, 1))
        values.add(round(value, 0))

        if 0 < value <= 100:
            values.add(round(value / 100, 4))
            values.add(round(value / 100, 3))
            values.add(round(value / 100, 2))
        if 0 < value <= 1:
            values.add(round(value * 100, 4))
            values.add(round(value * 100, 2))

    return values


def is_allowed_numeric_value(value: float, allowed_values: set[float]) -> bool:
    for allowed_value in allowed_values:
        tolerance = max(0.05, min(1.0, abs(allowed_value) * 0.005))
        if abs(value - allowed_value) <= tolerance:
            return True
    return False


def line_bounds(text: str, start: int, end: int) -> tuple[str, str, str]:
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", end)
    if line_end == -1:
        line_end = len(text)

    return text[line_start:start], text[start:end], text[end:line_end]


def is_title_or_list_number(text: str, start: int, end: int) -> bool:
    prefix, _, suffix = line_bounds(text, start, end)
    return bool(
        re.match(r"^\s*(?:#{1,6}\s*)?$", prefix)
        and re.match(r"^[.)]\s+", suffix)
    )


def mention_has_business_context(text: str, start: int, end: int, raw_number: str) -> bool:
    context_start = max(0, start - 48)
    context_end = min(len(text), end + 48)
    context = text[context_start:context_end].lower()

    if "%" in raw_number or "," in raw_number:
        return True

    return any(keyword in context for keyword in BUSINESS_NUMBER_KEYWORDS)


def unsupported_numeric_tokens(text: str, summary: dict[str, Any]) -> list[float]:
    allowed = summary_numeric_tokens(summary)
    unsupported: list[float] = []

    for match in NUMBER_PATTERN.finditer(text):
        if is_title_or_list_number(text, match.start(), match.end()):
            continue

        raw_number = match.group(0)
        if not mention_has_business_context(text, match.start(), match.end(), raw_number):
            continue

        value = round(parse_number(raw_number), 4)
        if is_allowed_numeric_value(value, allowed):
            continue

        if value not in unsupported:
            unsupported.append(value)

    return unsupported


def value_from_segment(summary: dict[str, Any], segment_key: str) -> dict[str, Any]:
    return dict((summary.get("key_segments") or {}).get(segment_key) or {})


def insight_by_name(summary: dict[str, Any], keyword: str) -> dict[str, Any]:
    for insight in summary.get("cross_dimensional_insights", []):
        if keyword.lower() in str(insight.get("insight_name", "")).lower():
            return dict(insight)
    return {}


def format_segment_line(segment: dict[str, Any]) -> str:
    if not segment:
        return "- 分群数据不可用，需要人工复核。"

    role_mapping = {
        "Core profit engine": "核心利润来源",
        "Growth engine": "增长转化池",
        "Dormant premium assets": "高价值沉睡资产",
        "Traffic foundation": "稳定流量基本盘",
        "Long-tail users": "长尾培育人群",
    }
    role = role_mapping.get(str(segment.get("business_role", "")), segment.get("business_role"))

    return (
        f"- {segment.get('segment')}：{segment.get('customer_count')} 个用户，"
        f"占比 {segment.get('share')}，Weighted AOV 为 {segment.get('weighted_aov')}，"
        f"Avg RFM Score 为 {segment.get('avg_rfm_score')}，Value Proxy Score 为 "
        f"{segment.get('avg_value_proxy_score')}。业务角色：{role}。"
    )


def insight_summary_cn(insight: dict[str, Any]) -> str:
    if not insight:
        return "当前没有可用的跨维度洞察，需要人工复核。"

    name = str(insight.get("insight_name", ""))
    key_finding = str(insight.get("key_finding", ""))
    numbers = NUMBER_PATTERN.findall(key_finding)

    if "Elite" in name and len(numbers) >= 2:
        return f"女性客户中约 {numbers[0]} 岁客群的 Weighted AOV 为 {numbers[1]}，应作为高客单重点观察人群。"
    if "Regional" in name and numbers:
        return f"Suburban 地区 Apparel 品类客户的 Weighted AOV 为 {numbers[-1]}，说明区域品类组合存在运营机会。"
    if "Pareto" in name and len(numbers) >= 2:
        return f"Top {numbers[0]} 用户贡献约 {numbers[1]} 的总消费，说明消费贡献存在集中度。"
    if "Churn" in name and numbers:
        return f"{numbers[0]} 的用户属于高消费但近期不活跃人群，且偏好 Home & Kitchen，应优先做召回。"
    if "High-value" in name:
        return "高价值用户对 Apparel 的偏好最强，可用于设计 VIP 品类包和会员权益。"

    return key_finding or "当前没有可用的跨维度洞察，需要人工复核。"


def recommended_action_cn(insight: dict[str, Any]) -> str:
    name = str(insight.get("insight_name", ""))
    if "Elite" in name:
        return "设计高价值商品、专家内容和 VIP 服务权益。"
    if "Regional" in name:
        return "围绕区域和品类偏好设计组合商品与内容活动。"
    if "Pareto" in name:
        return "优先把留存和服务资源投入到高价值用户。"
    if "Churn" in name:
        return "使用产品升级提醒、售后关怀和服务跟进进行召回。"
    if "High-value" in name:
        return "围绕 Apparel 品类设计 VIP 组合和忠诚度权益。"
    return "需要业务人员结合活动资源进一步复核。"


def build_mock_response(summary: dict[str, Any]) -> str:
    high_value = value_from_segment(summary, "high_value")
    churn = value_from_segment(summary, "churn_risk")
    potential = value_from_segment(summary, "potential")
    elite = insight_by_name(summary, "Elite")
    regional = insight_by_name(summary, "Regional")
    pareto = insight_by_name(summary, "Pareto")
    churn_recovery = insight_by_name(summary, "Churn")

    segment_lines = "\n".join(
        format_segment_line(segment) for segment in summary.get("segment_results", [])
    )

    return f"""## LLM 中文业务解读草稿

### 核心客户分群结果
{segment_lines}

### 高价值客户洞察
{format_segment_line(high_value)}
建议动作：围绕该分群已记录的品类偏好，设计 VIP 留存、会员权益和高价值品类推荐，优先保护利润来源。

### 流失风险客户洞察
{format_segment_line(churn)}
建议动作：使用可控的召回活动、服务跟进和产品提醒。执行前需要业务负责人复核流失定义和触达策略。

### 营销建议
- 潜力用户：{potential.get('share', 'N/A')} 的用户被识别为转化机会。建议在评估毛利影响后使用复购激励和组合推荐。
- 高客单细分信号：{insight_summary_cn(elite)}
- 区域品类机会：{insight_summary_cn(regional)}
- 价值集中度：{insight_summary_cn(pareto)}
- 流失召回：{recommended_action_cn(churn_recovery)}

### 人工复核提醒
- 面向客户执行前，请复核 raw 数据新鲜度、分群规则和活动资格。
- 本输出仅用于决策辅助，不代表自动批准营销活动。
"""


def call_llm(
    prompt: str,
    structured_summary: dict[str, Any],
    provider: str | None = None,
) -> LLMResponse:
    load_environment()
    requested_provider = normalize_provider(provider)

    if requested_provider == "mock":
        return LLMResponse(
            text=build_mock_response(structured_summary),
            requested_provider=requested_provider,
            provider="mock",
            model=MOCK_MODEL,
            api_reached=False,
            validation_passed=True,
            fallback_used=False,
            error=None,
            retry_count=0,
            error_type=None,
        )

    if requested_provider == "siliconflow":
        api_reached = False
        retry_count = 0
        try:
            text, model, retry_count = call_siliconflow(prompt)
            api_reached = True

            unsupported_numbers = unsupported_numeric_tokens(text, structured_summary)
            if unsupported_numbers:
                raise LLMProviderError(
                    "SiliconFlow response contained unsupported business numbers: "
                    + ", ".join(str(value) for value in unsupported_numbers[:10])
                    + ". Non-business numbering is allowed, but business metrics must come from the structured summary.",
                    api_reached=True,
                    error_type="validation_error",
                    retry_count=retry_count,
                )

            return LLMResponse(
                text=text,
                requested_provider=requested_provider,
                provider="siliconflow",
                model=model,
                api_reached=True,
                validation_passed=True,
                fallback_used=False,
                error=None,
                retry_count=retry_count,
                error_type=None,
            )
        except LLMProviderError as exc:
            api_reached = api_reached or exc.api_reached
            return LLMResponse(
                text=build_mock_response(structured_summary),
                requested_provider=requested_provider,
                provider="mock",
                model=MOCK_MODEL,
                api_reached=api_reached,
                validation_passed=False,
                fallback_used=True,
                error=str(exc),
                retry_count=exc.retry_count,
                error_type=exc.error_type,
            )
        except Exception as exc:
            return LLMResponse(
                text=build_mock_response(structured_summary),
                requested_provider=requested_provider,
                provider="mock",
                model=MOCK_MODEL,
                api_reached=api_reached,
                validation_passed=False,
                fallback_used=True,
                error=str(exc),
                retry_count=retry_count,
                error_type="timeout" if is_timeout_error(exc) else "unknown_error",
            )

    return LLMResponse(
        text=build_mock_response(structured_summary),
        requested_provider=requested_provider,
        provider="mock",
        model=MOCK_MODEL,
        api_reached=False,
        validation_passed=False,
        fallback_used=True,
        error=f"Unsupported LLM_PROVIDER: {requested_provider}",
        retry_count=0,
        error_type="unsupported_provider",
    )
