SELECT 'overall' AS dimension, 'All customers' AS segment, COUNT(*) AS customers,
       SUM(Churn = 'Yes') AS churned,
       ROUND(AVG(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END), 8) AS churn_rate
FROM customers
UNION ALL
SELECT 'contract', Contract, COUNT(*), SUM(Churn = 'Yes'),
       ROUND(AVG(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END), 8)
FROM customers GROUP BY Contract
UNION ALL
SELECT 'tenure_group', TenureGroup, COUNT(*), SUM(Churn = 'Yes'),
       ROUND(AVG(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END), 8)
FROM customers GROUP BY TenureGroup
UNION ALL
SELECT 'payment_method', PaymentMethod, COUNT(*), SUM(Churn = 'Yes'),
       ROUND(AVG(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END), 8)
FROM customers GROUP BY PaymentMethod
UNION ALL
SELECT 'internet_service', InternetService, COUNT(*), SUM(Churn = 'Yes'),
       ROUND(AVG(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END), 8)
FROM customers GROUP BY InternetService;
