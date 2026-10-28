"""Deterministic churn summaries and CSV report generation."""
from __future__ import annotations
from collections import defaultdict
from pathlib import Path
import csv
from .data import EXPECTED_COLUMNS, clean_rows, load_csv, validate_rows, write_csv


def segment_summary(rows: list[dict[str, object]], dimension: str) -> list[dict[str, object]]:
    groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows: groups[str(row[dimension])].append(row)
    result = []
    for category in sorted(groups):
        members = groups[category]; churned = sum(r["Churn"] == "Yes" for r in members)
        result.append({"Segment": category, "Customers": len(members), "Churned": churned,
                       "ChurnRate": round(churned / len(members), 8)})
    return result


def overall_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    n = len(rows); churned = sum(r["Churn"] == "Yes" for r in rows)
    return {"Metric": "Overall", "Customers": n, "Churned": churned,
            "ChurnRate": round(churned / n, 8),
            "MeanTenureMonths": round(sum(r["tenure"] for r in rows) / n, 4)}


def run_analysis(source: str | Path = "data/customer_churn.csv", output_dir: str | Path = "reports") -> dict[str, object]:
    raw = load_csv(source)
    issues = validate_rows(raw)
    if issues: raise ValueError("Source data validation failed: " + "; ".join(issues[:10]))
    rows = clean_rows(raw); output = Path(output_dir); output.mkdir(parents=True, exist_ok=True)
    columns = EXPECTED_COLUMNS + ["TenureGroup"]
    write_csv(output / "analysis_customers.csv", rows, columns)
    overall = [overall_summary(rows)]
    write_csv(output / "overall_summary.csv", overall, list(overall[0]))
    dims = ["Contract", "TenureGroup", "PaymentMethod", "InternetService", "Dependents", "Partner", "SeniorCitizen"]
    for dim in dims:
        summary = segment_summary(rows, dim)
        write_csv(output / f"churn_by_{dim.lower()}.csv", summary, ["Segment", "Customers", "Churned", "ChurnRate"])
    return {"rows": rows, "overall": overall[0], "dimensions": dims}
