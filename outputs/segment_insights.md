# AI 辅助 BI 决策工作流 - 客户分群洞察

## 项目运行时间
- UTC: 2026-06-23T02:34:51Z
- requested_provider: mock; provider: mock; model: local-structured-mock-v3; api_reached: False; validation_passed: True; fallback_used: False; retry_count: 0; error_type: None.

## 数据来源
- data/raw/ecommerce_user_behavior_dataset.csv（raw rows: 1001，cleaned rows: 1000，encoding: gbk）
- raw_row_count: 1001
- cleaned_row_count: 1000
- processed_customer_count: 1000

## 核心客户分群结果
| segment | customer_count | share | weighted_aov | avg_rfm_score | avg_value_proxy_score | category_preference | action_priority |
| --- | --- | --- | --- | --- | --- | --- | --- |
| High-value Customers | 122 | 12.2% | 523.72 | 13.02 | 72.84 | Apparel | Stabilize |
| Potential Customers | 292 | 29.2% | 1319.66 | 8.47 | 48.19 | Apparel | Convert |
| Churn-risk Customers | 188 | 18.8% | 812.1 | 8.8 | 61.97 | Home & Kitchen | Recover |
| Regular Retained Customers | 307 | 30.7% | 253.79 | 9.16 | 43.94 | Electronics | Upsell |
| Other Customers | 91 | 9.1% | 289.51 | 6.02 | 21.32 | Books | Nurture |

## 高价值客户洞察
High-value Customers（高价值用户）包含 122 个用户，占比 12.2%。Weighted AOV 为 523.72，Avg RFM Score 为 13.02，Avg Value Proxy Score 为 72.84。核心问题：需要重点做忠诚度保护和 VIP 留存。

女性客户中约 51 岁客群的 Weighted AOV 为 1001.62，应作为高客单重点观察人群。

## 流失风险客户洞察
Churn-risk Customers（流失风险用户）包含 188 个用户，占比 18.8%。Weighted AOV 为 812.1，Avg RFM Score 为 8.8，Avg Value Proxy Score 为 61.97。核心问题：历史消费较高，但近期互动不足。

建议来源：使用产品升级提醒、售后关怀和服务跟进进行召回。

## 营销建议
## LLM 中文业务解读草稿

### 核心客户分群结果
- High-value Customers：122 个用户，占比 12.2%，Weighted AOV 为 523.72，Avg RFM Score 为 13.02，Value Proxy Score 为 72.84。业务角色：核心利润来源。
- Potential Customers：292 个用户，占比 29.2%，Weighted AOV 为 1319.66，Avg RFM Score 为 8.47，Value Proxy Score 为 48.19。业务角色：增长转化池。
- Churn-risk Customers：188 个用户，占比 18.8%，Weighted AOV 为 812.1，Avg RFM Score 为 8.8，Value Proxy Score 为 61.97。业务角色：高价值沉睡资产。
- Regular Retained Customers：307 个用户，占比 30.7%，Weighted AOV 为 253.79，Avg RFM Score 为 9.16，Value Proxy Score 为 43.94。业务角色：稳定流量基本盘。
- Other Customers：91 个用户，占比 9.1%，Weighted AOV 为 289.51，Avg RFM Score 为 6.02，Value Proxy Score 为 21.32。业务角色：长尾培育人群。

### 高价值客户洞察
- High-value Customers：122 个用户，占比 12.2%，Weighted AOV 为 523.72，Avg RFM Score 为 13.02，Value Proxy Score 为 72.84。业务角色：核心利润来源。
建议动作：围绕该分群已记录的品类偏好，设计 VIP 留存、会员权益和高价值品类推荐，优先保护利润来源。

### 流失风险客户洞察
- Churn-risk Customers：188 个用户，占比 18.8%，Weighted AOV 为 812.1，Avg RFM Score 为 8.8，Value Proxy Score 为 61.97。业务角色：高价值沉睡资产。
建议动作：使用可控的召回活动、服务跟进和产品提醒。执行前需要业务负责人复核流失定义和触达策略。

### 营销建议
- 潜力用户：29.2% 的用户被识别为转化机会。建议在评估毛利影响后使用复购激励和组合推荐。
- 高客单细分信号：女性客户中约 51 岁客群的 Weighted AOV 为 1001.62，应作为高客单重点观察人群。
- 区域品类机会：Suburban 地区 Apparel 品类客户的 Weighted AOV 为 681.24，说明区域品类组合存在运营机会。
- 价值集中度：Top 10% 用户贡献约 18.6% 的总消费，说明消费贡献存在集中度。
- 流失召回：使用产品升级提醒、售后关怀和服务跟进进行召回。

### 人工复核提醒
- 面向客户执行前，请复核 raw 数据新鲜度、分群规则和活动资格。
- 本输出仅用于决策辅助，不代表自动批准营销活动。

补充的结构化数据信号：
- Suburban 地区 Apparel 品类客户的 Weighted AOV 为 681.24，说明区域品类组合存在运营机会。
- Top 10% 用户贡献约 18.6% 的总消费，说明消费贡献存在集中度。

## Human Review 人工复核提醒
- 执行前请复核分群定义、raw 数据新鲜度和活动资格。
- 请结合毛利、库存、物流、客服和合规约束复核 AI 生成建议。
- 本报告只支持 BI 决策准备，不代表自动批准面向客户的运营动作。

## LLM 使用的 Structured Summary
```json
{
  "run_time_utc": "2026-06-23T02:34:51Z",
  "data_sources": [
    {
      "path": "data/raw/ecommerce_user_behavior_dataset.csv",
      "row_count": 1001,
      "cleaned_row_count": 1000,
      "encoding": "gbk"
    }
  ],
  "raw_row_count": 1001,
  "cleaned_row_count": 1000,
  "processed_customer_count": 1000,
  "metrics_definition": {
    "recency": "Last_Login_Days_Ago; lower means more recent activity.",
    "frequency": "Purchase_Frequency aggregated per customer.",
    "monetary": "Total_Spending aggregated per customer.",
    "weighted_aov": "Total spending divided by total purchase frequency.",
    "value_proxy_score": "0-100 percentile score: 45% monetary, 25% frequency, 20% weighted AOV, 10% recency.",
    "rfm_score": "Recency, frequency, and monetary scores on a 1-5 scale; higher is better."
  },
  "overall_metrics": {
    "total_spending": 2552957.0,
    "total_purchase_frequency": 4631.0,
    "overall_weighted_aov": 551.28
  },
  "segment_results": [
    {
      "segment": "High-value Customers",
      "share": "12.2%",
      "share_pct": 12.2,
      "customer_count": 122,
      "business_role": "Core profit engine",
      "frequency_range": "7.4",
      "monetary_range": "Avg total spending CNY 3876.4",
      "weighted_aov": 523.72,
      "avg_recency_days": 9.05,
      "avg_rfm_score": 13.02,
      "avg_value_proxy_score": 72.84,
      "avg_recency_score": 4.24,
      "avg_frequency_score": 4.43,
      "avg_monetary_score": 4.34,
      "category_preference": "Apparel",
      "key_issue": "Need loyalty protection and VIP retention",
      "action_priority": "Stabilize"
    },
    {
      "segment": "Potential Customers",
      "share": "29.2%",
      "share_pct": 29.2,
      "customer_count": 292,
      "business_role": "Growth engine",
      "frequency_range": "2.02",
      "monetary_range": "Avg total spending CNY 2661.92",
      "weighted_aov": 1319.66,
      "avg_recency_days": 12.62,
      "avg_rfm_score": 8.47,
      "avg_value_proxy_score": 48.19,
      "avg_recency_score": 3.53,
      "avg_frequency_score": 1.79,
      "avg_monetary_score": 3.15,
      "category_preference": "Apparel",
      "key_issue": "Large base but low repurchase frequency",
      "action_priority": "Convert"
    },
    {
      "segment": "Churn-risk Customers",
      "share": "18.8%",
      "share_pct": 18.8,
      "customer_count": 188,
      "business_role": "Dormant premium assets",
      "frequency_range": "4.76",
      "monetary_range": "Avg total spending CNY 3866.1",
      "weighted_aov": 812.1,
      "avg_recency_days": 24.67,
      "avg_rfm_score": 8.8,
      "avg_value_proxy_score": 61.97,
      "avg_recency_score": 1.39,
      "avg_frequency_score": 3.14,
      "avg_monetary_score": 4.28,
      "category_preference": "Home & Kitchen",
      "key_issue": "High historical spending but low recent engagement",
      "action_priority": "Recover"
    },
    {
      "segment": "Regular Retained Customers",
      "share": "30.7%",
      "share_pct": 30.7,
      "customer_count": 307,
      "business_role": "Traffic foundation",
      "frequency_range": "6.72",
      "monetary_range": "Avg total spending CNY 1706.25",
      "weighted_aov": 253.79,
      "avg_recency_days": 15.75,
      "avg_rfm_score": 9.16,
      "avg_value_proxy_score": 43.94,
      "avg_recency_score": 2.97,
      "avg_frequency_score": 4.05,
      "avg_monetary_score": 2.14,
      "category_preference": "Electronics",
      "key_issue": "Frequent buyers with relatively lower spending",
      "action_priority": "Upsell"
    },
    {
      "segment": "Other Customers",
      "share": "9.1%",
      "share_pct": 9.1,
      "customer_count": 91,
      "business_role": "Long-tail users",
      "frequency_range": "1.98",
      "monetary_range": "Avg total spending CNY 572.65",
      "weighted_aov": 289.51,
      "avg_recency_days": 14.54,
      "avg_rfm_score": 6.02,
      "avg_value_proxy_score": 21.32,
      "avg_recency_score": 3.24,
      "avg_frequency_score": 1.78,
      "avg_monetary_score": 1.0,
      "category_preference": "Books",
      "key_issue": "Low engagement and limited short-term value",
      "action_priority": "Nurture"
    }
  ],
  "key_segments": {
    "high_value": {
      "segment": "High-value Customers",
      "share": "12.2%",
      "share_pct": 12.2,
      "customer_count": 122,
      "business_role": "Core profit engine",
      "frequency_range": "7.4",
      "monetary_range": "Avg total spending CNY 3876.4",
      "weighted_aov": 523.72,
      "avg_recency_days": 9.05,
      "avg_rfm_score": 13.02,
      "avg_value_proxy_score": 72.84,
      "avg_recency_score": 4.24,
      "avg_frequency_score": 4.43,
      "avg_monetary_score": 4.34,
      "category_preference": "Apparel",
      "key_issue": "Need loyalty protection and VIP retention",
      "action_priority": "Stabilize"
    },
    "churn_risk": {
      "segment": "Churn-risk Customers",
      "share": "18.8%",
      "share_pct": 18.8,
      "customer_count": 188,
      "business_role": "Dormant premium assets",
      "frequency_range": "4.76",
      "monetary_range": "Avg total spending CNY 3866.1",
      "weighted_aov": 812.1,
      "avg_recency_days": 24.67,
      "avg_rfm_score": 8.8,
      "avg_value_proxy_score": 61.97,
      "avg_recency_score": 1.39,
      "avg_frequency_score": 3.14,
      "avg_monetary_score": 4.28,
      "category_preference": "Home & Kitchen",
      "key_issue": "High historical spending but low recent engagement",
      "action_priority": "Recover"
    },
    "potential": {
      "segment": "Potential Customers",
      "share": "29.2%",
      "share_pct": 29.2,
      "customer_count": 292,
      "business_role": "Growth engine",
      "frequency_range": "2.02",
      "monetary_range": "Avg total spending CNY 2661.92",
      "weighted_aov": 1319.66,
      "avg_recency_days": 12.62,
      "avg_rfm_score": 8.47,
      "avg_value_proxy_score": 48.19,
      "avg_recency_score": 3.53,
      "avg_frequency_score": 1.79,
      "avg_monetary_score": 3.15,
      "category_preference": "Apparel",
      "key_issue": "Large base but low repurchase frequency",
      "action_priority": "Convert"
    }
  },
  "cross_dimensional_insights": [
    {
      "insight_name": "Elite Customer Segment",
      "dimension": "Age + Gender + Weighted AOV",
      "key_finding": "Female customers around age 51 show the highest weighted AOV (1001.62) among sufficiently sized groups.",
      "business_meaning": "This group should be treated as a priority profit-driving segment.",
      "recommended_action": "Design premium product campaigns, expert review content, and VIP service benefits for this segment."
    },
    {
      "insight_name": "Regional Category Opportunity",
      "dimension": "Location + Product Category + Weighted AOV",
      "key_finding": "Suburban customers in the Apparel category show strong weighted AOV (681.24).",
      "business_meaning": "Regional category preference can reveal underexplored market opportunities.",
      "recommended_action": "Create region-specific product bundles and content campaigns based on category preference."
    },
    {
      "insight_name": "Pareto Value Concentration",
      "dimension": "Customer Value Contribution",
      "key_finding": "The top 10% users contribute approximately 18.6% of total spending.",
      "business_meaning": "Revenue is concentrated among higher-value customers.",
      "recommended_action": "Prioritize retention and service resources for top-value users."
    },
    {
      "insight_name": "Churn Recovery",
      "dimension": "Recency + Monetary + Category Preference",
      "key_finding": "18.8% of users are high-spending but inactive, with strongest preference in Home & Kitchen.",
      "business_meaning": "These users should be treated as dormant premium assets rather than low-value inactive users.",
      "recommended_action": "Build win-back campaigns with product upgrade reminders, after-sales recovery, and service follow-up."
    },
    {
      "insight_name": "High-value Category Focus",
      "dimension": "Segment + Product Category",
      "key_finding": "High-value customers show the strongest preference in Apparel.",
      "business_meaning": "Category preference helps translate high-value segmentation into campaign themes.",
      "recommended_action": "Use category-specific VIP bundles and loyalty benefits for high-value customers."
    }
  ],
  "guardrails": [
    "All numerical claims must come from this structured summary.",
    "LLM output is a draft for human review and must not trigger customer-facing campaigns automatically."
  ]
}
```
