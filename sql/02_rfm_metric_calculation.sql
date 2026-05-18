-- 02_rfm_metric_calculation.sql
-- Purpose: Calculate customer-level RFM metrics from transaction records.

SELECT
    customer_id,
    DATEDIFF('2026-03-31', MAX(order_date)) AS recency_days,
    COUNT(DISTINCT order_id) AS frequency,
    SUM(amount) AS monetary
FROM sales_transactions
WHERE order_date BETWEEN '2025-01-01' AND '2026-03-31'
  AND amount > 0
GROUP BY customer_id;

