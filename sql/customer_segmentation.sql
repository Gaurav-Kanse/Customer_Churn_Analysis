SELECT 'Contract' AS dimension, Contract AS segment, COUNT(*) AS customers,
       SUM(Churn = 'Yes') AS churned, ROUND(AVG(Churn = 'Yes'), 8) AS churn_rate
FROM customers GROUP BY Contract
UNION ALL
SELECT 'TenureGroup', TenureGroup, COUNT(*), SUM(Churn = 'Yes'), ROUND(AVG(Churn = 'Yes'), 8)
FROM customers GROUP BY TenureGroup
UNION ALL
SELECT 'PaymentMethod', PaymentMethod, COUNT(*), SUM(Churn = 'Yes'), ROUND(AVG(Churn = 'Yes'), 8)
FROM customers GROUP BY PaymentMethod
UNION ALL
SELECT 'InternetService', InternetService, COUNT(*), SUM(Churn = 'Yes'), ROUND(AVG(Churn = 'Yes'), 8)
FROM customers GROUP BY InternetService
UNION ALL
SELECT 'Dependents', Dependents, COUNT(*), SUM(Churn = 'Yes'), ROUND(AVG(Churn = 'Yes'), 8)
FROM customers GROUP BY Dependents
UNION ALL
SELECT 'Partner', Partner, COUNT(*), SUM(Churn = 'Yes'), ROUND(AVG(Churn = 'Yes'), 8)
FROM customers GROUP BY Partner
UNION ALL
SELECT 'SeniorCitizen', CAST(SeniorCitizen AS TEXT), COUNT(*), SUM(Churn = 'Yes'), ROUND(AVG(Churn = 'Yes'), 8)
FROM customers GROUP BY SeniorCitizen;
