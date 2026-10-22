-- Query 1: 90-day churn by segment
SELECT plan||' / '||channel AS segment, COUNT(*) AS customers,
 ROUND(100.0*SUM(CASE WHEN months_to_churn<=3 THEN 1 ELSE 0 END)/COUNT(*),1) AS churn_90d_pct,
 ROUND(AVG(mrr_usd),0) AS avg_mrr
FROM customers WHERE signup_month<='2025-09' GROUP BY 1 ORDER BY churn_90d_pct DESC;

-- Query 2: 90-day retention by signup cohort
SELECT signup_month, COUNT(*) AS customers,
 ROUND(100.0*SUM(CASE WHEN months_to_churn IS NULL OR months_to_churn>3 THEN 1 ELSE 0 END)/COUNT(*),1) AS retained_90d_pct
FROM customers WHERE signup_month<='2025-09' GROUP BY 1 ORDER BY 1;
