# Customer churn: concise business readout

## Scope

Descriptive analysis of the 7,043 customer records in `data/customer_churn.csv`. The analysis was rerun through the project CLI; it does not rely on estimates from the notebook alone.

## Results

- Overall churn is **26.54%** (1,869 of 7,043 customers).
- Month-to-month contract churn is **42.71%** (1,655 / 3,875), compared with **11.27%** for one-year (166 / 1,473) and **2.83%** for two-year contracts (48 / 1,695).
- Electronic check churn is **45.29%** (1,071 / 2,365); fiber optic churn is **41.89%** (1,297 / 3,096).
- Average tenure is **32.37 months**.

## Business interpretation

The largest observed churn rates are concentrated in month-to-month contracts and electronic check payment, with fiber optic customers also above the overall rate. These are useful groups for further investigation and retention testing, but these descriptive associations do not show that contract type, payment method, or internet service causes churn.

## Data quality and caveats

The original dataset has 7,043 rows, unique customer IDs, no exact duplicate rows, and 11 blank `TotalCharges` values. All 11 are zero-tenure customers. The blanks are preserved as null rather than filled with assumed values. The supplied cleaned dataset matches original categorical/identifier/churn fields and amounts numerically, but is independently checked for validity. Its tenure group is consistent with the notebook's interval definition.

## Suggested next step

Investigate the customer journey and service experience for high-churn segments, then evaluate a clearly defined retention intervention with a time-based holdout or controlled experiment. Track incremental churn reduction and guard against simply shifting customers to longer contracts without improving retention.

## Reproducibility

Run `PYTHONPATH=src python -m churn_analytics.cli` to regenerate CSV outputs and verify Python/SQLite parity. See `QA_REPORT.md` for validation and test execution details.
