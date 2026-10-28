# QA report

## Commands executed

- `python -m churn_analytics.cli` with `PYTHONPATH=src`
- `python -m pytest -q`

## Results

- CLI analysis completed successfully: 7,043 source rows validated; validation issue list was empty.
- Python/SQLite metric parity: PASS for overall churn and the configured segmentation dimensions.
- Overall results: 1,869 churned / 7,043 customers; churn rate 0.26536987; mean tenure 32.3711 months.
- `python -m pytest -q`: NOT RUN; this environment's Python does not have pytest installed (`No module named pytest`). `pip` is also unavailable here, so dependency installation could not be attempted.
- Manually invoked all five test functions from `tests/test_pipeline.py`: 5 passed, including SQL parity. This checks the assertions but does not replace running pytest itself.

## Dataset checks

- Original CSV: 7,043 rows, 21 columns, 7,043 unique IDs, no duplicate IDs or exact duplicate rows, 11 blank `TotalCharges`, zero nonblank unparseable `TotalCharges`, and only the documented blank-charge condition.
- Supplied cleaned CSV: 7,043 rows, 22 columns, 7,043 unique IDs, no duplicate IDs or exact duplicate rows; `TenureGroup` validates against the stated bands. Its 11 blank charges remain missing.
- The existing notebook has 36 cells with executed EDA outputs. Its input path points outside the repository (`/content/...`); it was retained without modification.

## Remaining issue

Automated pytest assertions have not executed because pytest is absent in this runtime. Install project dependencies and run `python -m pytest -q` to complete that check. The CSV/SQLite pipeline itself executed successfully.
