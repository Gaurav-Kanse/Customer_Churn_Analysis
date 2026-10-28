from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from churn_analytics.data import clean_rows, load_csv, tenure_group, validate_rows
from churn_analytics.analysis import overall_summary, segment_summary
from churn_analytics.sql_workflow import build_database, verify_parity


def test_original_dataset_validation_and_safe_total_charges():
    raw = load_csv(ROOT / "data/customer_churn.csv")
    assert len(raw) == 7043
    assert validate_rows(raw) == []
    cleaned = clean_rows(raw)
    missing = [r for r in cleaned if r["TotalCharges"] is None]
    assert len(missing) == 11
    assert all(r["tenure"] == 0 for r in missing)


def test_cleaned_file_tenure_groups_are_correct():
    rows = load_csv(ROOT / "data/customer_churn_cleaned.csv")
    assert validate_rows(rows) == []
    assert all(r["TenureGroup"] == tenure_group(int(r["tenure"])) for r in rows)


def test_known_overall_metrics():
    rows = clean_rows(load_csv(ROOT / "data/customer_churn.csv"))
    result = overall_summary(rows)
    assert result["Customers"] == 7043
    assert result["Churned"] == 1869
    assert abs(result["ChurnRate"] - 1869 / 7043) < 1e-8


def test_sql_python_parity(tmp_path):
    rows = clean_rows(load_csv(ROOT / "data/customer_churn.csv"))
    db = build_database(ROOT / "data/customer_churn.csv", tmp_path / "customers.sqlite")
    assert verify_parity(rows, db) == []
    db.close()


def test_contract_summary_known_results():
    rows = clean_rows(load_csv(ROOT / "data/customer_churn.csv"))
    result = {x["Segment"]: x for x in segment_summary(rows, "Contract")}
    assert result["Month-to-month"]["Customers"] == 3875
    assert result["Month-to-month"]["Churned"] == 1655
