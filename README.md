# Telecom Customer Churn Analytics

A reproducible, modular analysis of the Telco customer churn dataset. The project validates the supplied data, derives safe typed records, analyzes churn in Python and SQLite, checks that both workflows agree, and writes inspectable CSV outputs.

## Project contents

```text
data/                 Original and supplied cleaned CSVs (preserved)
notebooks/            Existing exploratory analysis notebook (preserved)
src/churn_analytics/  CSV validation, analysis, SQLite workflow, CLI
tests/                pytest checks for data, metrics, and Python/SQL parity
sql/                  SQLite schema, validation, churn, and segmentation queries
reports/              Generated CSV outputs, database, and business/QA reports
```

## Setup and run

Requires Python 3.10 or newer. The analysis and SQLite workflow use the Python standard library.

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
PYTHONPATH=src python -m churn_analytics.cli
python -m pytest -q
```

The CLI reads `data/customer_churn.csv`, writes reproducible CSVs under `reports/`, and creates `reports/customer_churn.sqlite`. Generated outputs can be recreated at any time. Change the source or destinations with `--source`, `--reports`, and `--database`.

## Methodology

- The original CSV is the source of truth. The supplied cleaned CSV is independently validated and is not used to silently replace source data.
- Identifiers, categorical labels, numeric fields, ranges, duplicate IDs/rows, and missing values are checked before analysis.
- `TotalCharges` is parsed as a number. Its 11 blank values are retained as missing because they occur on zero-tenure records; no amount is imputed.
- `TenureGroup` is derived from tenure using explicit bands: 1–12, 13–24, 25–48, 49–60, and 61–72 months. The first band includes tenure zero to match the existing notebook's `pd.cut(..., include_lowest=True)` rule.
- Churn rate is churned customers divided by customers in each group. Python and SQL summaries are compared by overall and by segment.
- The project is descriptive; no predictive model is introduced. Segment associations are not causal effects.

## Findings from the supplied data

There are 7,043 customers; 1,869 churned (26.54%). Month-to-month customers have a 42.71% churn rate (1,655 of 3,875), versus 11.27% for one-year contracts and 2.83% for two-year contracts. Electronic check customers show 45.29% churn (1,071 of 2,365), and fiber optic customers 41.89% (1,297 of 3,096). See [business report](reports/business_report.md) and segment CSVs for counts and rates.

## Limitations

This is a single observational dataset and does not establish why customers churn. The dataset has no time-indexed history, so trends and retention intervention effects cannot be assessed. Segment comparisons can reflect overlapping characteristics. Blank `TotalCharges` values remain missing and should be excluded from charge-specific calculations unless a documented business rule is approved. Notebook outputs were created with a Colab path that is not available in this repository; the original notebook is retained unchanged.

## Data provenance

The input files and notebook are kept as supplied. No source records are deleted or overwritten. `reports/analysis_customers.csv` is a derived, typed export and not a replacement for either input dataset.
