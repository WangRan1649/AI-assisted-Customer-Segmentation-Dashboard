# AI-assisted BI Decision Workflow - Segment Insights

## Project Run Time
- UTC: 2026-06-22T07:30:37Z
- Requested provider: siliconflow; actual provider: siliconflow; model: deepseek-ai/DeepSeek-V4-Flash; api reached: True; validation passed: True; fallback used: False; retry count: 1; error type: None.

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
## Core Customer Segment Results

- **High-value Customers** – 12.2% share (122 customers). Core profit engine. Avg total spending CNY 3876.4, avg recency 9.05 days, avg RFM score 13.02, avg value proxy score 72.84. Key issue: need loyalty protection and VIP retention. Action priority: Stabilize.
- **Potential Customers** – 29.2% share (292 customers). Growth engine. Avg total spending CNY 2661.92, avg recency 12.62 days, avg RFM score 8.47, avg value proxy score 48.19. Key issue: large base but low repurchase frequency. Action priority: Convert.
- **Churn-risk Customers** – 18.8% share (188 customers). Dormant premium assets. Avg total spending CNY 3866.1, avg recency 24.67 days, avg RFM score 8.8, avg value proxy score 61.97. Key issue: high historical spending but low recent engagement. Action priority: Recover.
- **Regular Retained Customers** – 30.7% share (307 customers). Traffic foundation. Avg total spending CNY 1706.25, avg recency 15.75 days, avg RFM score 9.16, avg value proxy score 43.94. Key issue: frequent buyers with relatively lower spending. Action priority: Upsell.
- **Other Customers** – 9.1% share (91 customers). Long-tail users. Avg total spending CNY 572.65, avg recency 14.54 days, avg RFM score 6.02, avg value proxy score 21.32. Key issue: low engagement and limited short-term value. Action priority: Nurture.

## High-value Customer Insight

- **Segment profile**: 122 customers (12.2% share) with avg total spending CNY 3876.4, avg recency 9.05 days, avg RFM score 13.02, avg value proxy score 72.84. Strongest category preference: Apparel.
- **Cross-dimensional finding**: Female customers around age 51 show the highest weighted AOV (1001.62) among sufficiently sized groups – treat as a priority profit-driving segment.
- **Pareto concentration**: The top 10% of users contribute approximately 18.6% of total spending, reinforcing the need to protect high-value customers.
- **Recommended action**: Design premium product campaigns, expert review content, and VIP service benefits for this segment. Use category-specific VIP bundles and loyalty benefits (Apparel focus).

## Churn-risk Customer Insight

- **Segment profile**: 188 customers (18.8% share) with avg total spending CNY 3866.1, avg recency 24.67 days, avg RFM score 8.8, avg value proxy score 61.97. Strongest category preference: Home & Kitchen.
- **Key issue**: High historical spending but low recent engagement – these are dormant premium assets, not low-value inactive users.
- **Cross-dimensional finding**: 18.8% of users are high-spending but inactive, with strongest preference in Home & Kitchen.
- **Recommended action**: Build win-back campaigns with product upgrade reminders, after-sales recovery, and service follow-up.

## Marketing Recommendations

- **High-value Customers (Stabilize)**: Launch VIP loyalty programs, exclusive Apparel previews, and personalized service to retain the 12.2% core profit engine.
- **Potential Customers (Convert)**: Increase repurchase frequency among the 29.2% growth engine through targeted Apparel campaigns, cross-sell bundles, and engagement incentives.
- **Churn-risk Customers (Recover)**: Execute win-back campaigns focused on Home & Kitchen product upgrades, after-sales service, and re-engagement offers for the 18.8% dormant premium assets.
- **Regular Retained Customers (Upsell)**: Encourage higher spending among the 30.7% traffic foundation (Electronics preference) with premium product recommendations and tiered rewards.
- **Other Customers (Nurture)**: Gradually engage the 9.1% long-tail users (Books preference) with low-commitment content and introductory offers.
- **Cross-segment actions**: Prioritize retention resources for top-value users (top 10% contribute ~18.6% of total spending). Create region-specific product bundles for suburban Apparel customers (weighted AOV 681.24). Design premium campaigns for the high-AOV female ~51 age group.

## Human Review Reminder

All numerical claims in this draft are copied directly from the provided structured summary. No metrics, percentages, segment sizes, customer counts, product categories, rankings, ages, AOV values, RFM scores, Value Proxy Scores, recency values, frequency values, spending amounts, campaign timing, discount rates, or model/provider details have been invented or extrapolated. This output is a draft for human review and must not trigger customer-facing campaigns automatically. Any missing business numbers or context not present in the summary require human investigation before use.

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
  "run_time_utc": "2026-06-22T07:30:37Z",
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
