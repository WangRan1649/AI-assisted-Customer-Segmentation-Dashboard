-- 03_customer_segmentation_rules.sql
-- Purpose: Assign customer segments based on Frequency and Monetary value.

SELECT
    customer_id,
    recency_days,
    frequency,
    monetary,
    CASE
        WHEN frequency BETWEEN 5 AND 9 AND monetary BETWEEN 2500 AND 5000
            THEN 'High-value Customers'
        WHEN frequency BETWEEN 0 AND 4 AND monetary >= 1000
            THEN 'Potential Customers'
        WHEN recency_days > 90 AND monetary >= 3000
            THEN 'Churn-risk Customers'
        WHEN frequency >= 5 AND monetary < 2500
            THEN 'Regular Retained Customers'
        ELSE 'Other Customers'
    END AS customer_segment
FROM customer_rfm_metrics;

