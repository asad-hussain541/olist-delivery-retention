-- 01_delivery_kpis.sql
-- Business question: How reliable is Olist's delivery promise overall, and is it getting better or worse?
-- Grain: one row per month of purchase (delivered orders only).
--
-- "Late" = delivered after the estimated delivery date the customer was shown at checkout.
-- That date is the promise, so it is the right yardstick (not raw delivery time).

WITH delivered AS (
    SELECT
        order_id,
        strftime('%Y-%m', order_purchase_timestamp)                       AS purchase_month,
        julianday(order_delivered_customer_date)
          - julianday(order_purchase_timestamp)                           AS days_to_deliver,
        julianday(order_delivered_customer_date)
          - julianday(order_estimated_delivery_date)                      AS days_vs_promise
    FROM orders
    WHERE order_status = 'delivered'
      AND order_delivered_customer_date IS NOT NULL
)
SELECT
    purchase_month,
    COUNT(*)                                             AS orders,
    ROUND(AVG(days_to_deliver), 1)                       AS avg_days_to_deliver,
    ROUND(100.0 * AVG(days_vs_promise > 0), 1)           AS pct_late,
    -- average lateness among late orders only (how bad is "late"?)
    ROUND(AVG(CASE WHEN days_vs_promise > 0 THEN days_vs_promise END), 1) AS avg_days_late_when_late
FROM delivered
-- the first and last few months have very few orders; drop them so trends aren't noise
WHERE purchase_month BETWEEN '2017-01' AND '2018-08'
GROUP BY purchase_month
ORDER BY purchase_month;
