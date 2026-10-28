SELECT 'row_count' AS check_name, COUNT(*) AS result FROM customers
UNION ALL SELECT 'duplicate_customer_ids', COUNT(*) - COUNT(DISTINCT customerID) FROM customers
UNION ALL SELECT 'missing_customer_ids', SUM(customerID IS NULL OR TRIM(customerID) = '') FROM customers
UNION ALL SELECT 'missing_total_charges', SUM(TotalCharges IS NULL) FROM customers
UNION ALL SELECT 'missing_or_invalid_tenure_group', SUM(TenureGroup IS NULL OR TRIM(TenureGroup) = '') FROM customers
UNION ALL SELECT 'tenure_zero_with_charge', SUM(tenure = 0 AND TotalCharges IS NOT NULL) FROM customers
UNION ALL SELECT 'tenure_nonzero_without_charge', SUM(tenure > 0 AND TotalCharges IS NULL) FROM customers;
