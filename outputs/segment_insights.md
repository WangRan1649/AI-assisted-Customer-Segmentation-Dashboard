# AI-assisted BI Decision Workflow - Segment Insights

## Project Run Time
- UTC: 2026-06-22T03:23:25Z
- Requested provider: siliconflow; actual provider: siliconflow; model: deepseek-ai/DeepSeek-V4-Flash; api reached: True; validation passed: True; fallback used: False.

## Data Source
- data/raw/ecommerce_user_behavior_dataset.csv (raw rows: 1001, cleaned rows: 1000, encoding: gbk)
- Raw row count: 1001
- Cleaned row count: 1000
- Processed customer count: 1000

## Core Customer Segment Results
| segment | customer_count | share | weighted_aov | avg_rfm_score | avg_value_proxy_score | category_preference | action_priority |
| --- | --- | --- | --- | --- | --- | --- | --- |
| High-value Customers | 122 | 12.2% | 523.72 | 13.02 | 72.84 | Apparel | Stabilize |
| Potential Customers | 292 | 29.2% | 1319.66 | 8.47 | 48.19 | Apparel | Convert |
| Churn-risk Customers | 188 | 18.8% | 812.1 | 8.8 | 61.97 | Home & Kitchen | Recover |
| Regular Retained Customers | 307 | 30.7% | 253.79 | 9.16 | 43.94 | Electronics | Upsell |
| Other Customers | 91 | 9.1% | 289.51 | 6.02 | 21.32 | Books | Nurture |

## High-value Customer Insights
High-value Customers contains 122 customers (12.2%). Weighted AOV is 523.72, average RFM score is 13.02, and average Value Proxy Score is 72.84. Key issue: Need loyalty protection and VIP retention.

Female customers around age 51 show the highest weighted AOV (1001.62) among sufficiently sized groups.

## Churn-risk Customer Insights
Churn-risk Customers contains 188 customers (18.8%). Weighted AOV is 812.1, average RFM score is 8.8, and average Value Proxy Score is 61.97. Key issue: High historical spending but low recent engagement.

Recommended action source: Build win-back campaigns with product upgrade reminders, after-sales recovery, and service follow-up.

## Marketing Recommendations
# BI Decision Support Draft – Customer Segmentation Dashboard

## 1. Core Customer Segment Results

- **High-value Customers** – 12.2% share (122 customers). Avg total spending CNY 3876.4, avg RFM score 13.02, avg value proxy score 72.84. Category preference: Apparel. Action priority: Stabilize.
- **Potential Customers** – 29.2% share (292 customers). Avg total spending CNY 2661.92, avg RFM score 8.47, avg value proxy score 48.19. Category preference: Apparel. Action priority: Convert.
- **Churn-risk Customers** – 18.8% share (188 customers). Avg total spending CNY 3866.1, avg RFM score 8.8, avg value proxy score 61.97. Category preference: Home & Kitchen. Action priority: Recover.
- **Regular Retained Customers** – 30.7% share (307 customers). Avg total spending CNY 1706.25, avg RFM score 9.16, avg value proxy score 43.94. Category preference: Electronics. Action priority: Upsell.
- **Other Customers** – 9.1% share (91 customers). Avg total spending CNY 572.65, avg RFM score 6.02, avg value proxy score 21.32. Category preference: Books. Action priority: Nurture.

## 2. High-value Customer Insight

- **Segment profile**: 122 customers (12.2% of base) with avg total spending CNY 3876.4, avg RFM score 13.02, avg value proxy score 72.84. They show the strongest category preference for Apparel and have a key issue of needing loyalty protection and VIP retention.
- **Elite sub‑segment**: Female customers around age 51 exhibit the highest weighted AOV (1001.62) among sufficiently sized groups. This group should be treated as a priority profit‑driving segment.
- **Pareto concentration**: The top 10% of users contribute approximately 18.6% of total spending, reinforcing the need to prioritize retention and service resources for higher‑value customers.
- **Category focus**: High‑value customers’ Apparel preference can be used to design VIP bundles and loyalty benefits.

## 3. Churn-risk Customer Insight

- **Segment profile**: 188 customers (18.8% of base) with avg total spending CNY 3866.1, avg RFM score 8.8, avg value proxy score 61.97. Their avg recency is 24.67 days (low recency score 1.39), indicating high historical spending but low recent engagement. Category preference: Home & Kitchen.
- **Dormant premium assets**: These users are high‑spending but inactive. Their strongest category preference is Home & Kitchen, suggesting win‑back campaigns should leverage product upgrade reminders, after‑sales recovery, and service follow‑up.

## 4. Marketing Recommendations

- **High‑value customers (Stabilize)**: Implement loyalty protection and VIP retention programs. Use Apparel‑specific VIP bundles and loyalty benefits. Design premium product campaigns and expert review content for the elite female‑age‑51 sub‑segment.
- **Potential customers (Convert)**: Focus on increasing repurchase frequency. Leverage their Apparel preference with targeted conversion campaigns. Create region‑specific product bundles and content campaigns (e.g., suburban Apparel customers show strong weighted AOV of 681.24).
- **Churn‑risk customers (Recover)**: Build win‑back campaigns with Home & Kitchen product upgrade reminders, after‑sales recovery, and service follow‑up. Treat them as dormant premium assets rather than low‑value inactive users.
- **Regular retained customers (Upsell)**: Encourage higher spending through Electronics‑focused upsell offers and cross‑sell opportunities.
- **Other customers (Nurture)**: Develop low‑cost nurturing sequences to gradually increase engagement, starting with Books‑related content.

## 5. Human Review Reminder

- All numerical claims in this draft are copied directly from the provided structured summary. No metrics, percentages, segment sizes, or customer counts have been invented or recalculated.
- This output is a draft for human review and must not trigger customer‑facing campaigns automatically. Any missing business details (e.g., campaign timing, discount rates, specific product SKUs) require human input before execution.

Additional data-backed signals:
- Suburban customers in the Apparel category show strong weighted AOV (681.24).
- The top 10% users contribute approximately 18.6% of total spending.

## Human Review Reminder
- Review segment definitions, raw data freshness, and campaign eligibility before execution.
- Validate all AI-generated recommendations against margin, inventory, logistics, and compliance constraints.
- This report supports BI decision preparation only; it does not approve customer-facing actions.

## Structured Summary Used By LLM
```json
{
  "run_time_utc": "2026-06-22T03:23:25Z",
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
