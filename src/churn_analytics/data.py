"""CSV loading, safe normalization, and data quality checks."""
from __future__ import annotations

import csv
from pathlib import Path

EXPECTED_COLUMNS = [
    "customerID", "gender", "SeniorCitizen", "Partner", "Dependents", "tenure",
    "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
    "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies", "Contract",
    "PaperlessBilling", "PaymentMethod", "MonthlyCharges", "TotalCharges", "Churn",
]
CATEGORICAL_VALUES = {
    "gender": {"Female", "Male"}, "SeniorCitizen": {"0", "1"},
    "Partner": {"Yes", "No"}, "Dependents": {"Yes", "No"},
    "PhoneService": {"Yes", "No"}, "MultipleLines": {"Yes", "No", "No phone service"},
    "InternetService": {"DSL", "Fiber optic", "No"},
    "OnlineSecurity": {"Yes", "No", "No internet service"},
    "OnlineBackup": {"Yes", "No", "No internet service"},
    "DeviceProtection": {"Yes", "No", "No internet service"},
    "TechSupport": {"Yes", "No", "No internet service"},
    "StreamingTV": {"Yes", "No", "No internet service"},
    "StreamingMovies": {"Yes", "No", "No internet service"},
    "Contract": {"Month-to-month", "One year", "Two year"},
    "PaperlessBilling": {"Yes", "No"},
    "PaymentMethod": {"Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"},
    "Churn": {"Yes", "No"},
}


def load_csv(path: str | Path) -> list[dict[str, str]]:
    """Load CSV rows as strings; empty fields remain empty until explicitly normalized."""
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header: {path}")
        if reader.fieldnames != EXPECTED_COLUMNS and reader.fieldnames != EXPECTED_COLUMNS + ["TenureGroup"]:
            raise ValueError(f"Unexpected columns in {path}: {reader.fieldnames}")
        return [dict(row) for row in reader]


def clean_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    """Return normalized records. Missing TotalCharges remains None, never fabricated."""
    cleaned = []
    for row in rows:
        item: dict[str, object] = {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
        item["SeniorCitizen"] = int(item["SeniorCitizen"])
        item["tenure"] = int(item["tenure"])
        item["MonthlyCharges"] = float(item["MonthlyCharges"])
        total = str(item["TotalCharges"]).strip()
        item["TotalCharges"] = float(total) if total else None
        item["TenureGroup"] = tenure_group(item["tenure"])
        cleaned.append(item)
    return cleaned


def tenure_group(tenure: int) -> str:
    if 0 <= tenure <= 12: return "1–12 months"
    if tenure <= 24: return "13–24 months"
    if tenure <= 48: return "25–48 months"
    if tenure <= 60: return "49–60 months"
    if tenure <= 72: return "61–72 months"
    raise ValueError(f"tenure outside supported range: {tenure}")


def validate_rows(rows: list[dict[str, str]]) -> list[str]:
    """Return actionable validation issues; empty list means core checks pass."""
    issues: list[str] = []
    if not rows:
        return ["dataset is empty"]
    ids = [r.get("customerID", "") for r in rows]
    if any(not x for x in ids): issues.append("customerID contains missing values")
    if len(ids) != len(set(ids)): issues.append("customerID is not unique")
    if len({tuple(sorted(r.items())) for r in rows}) != len(rows): issues.append("duplicate records found")
    if set(rows[0]) - set(EXPECTED_COLUMNS) not in (set(), {"TenureGroup"}):
        issues.append("unexpected columns found")
    for i, row in enumerate(rows, start=2):
        for col in EXPECTED_COLUMNS:
            if col not in row or row[col] is None:
                issues.append(f"row {i}: missing column {col}"); continue
            value = row[col].strip()
            if col in CATEGORICAL_VALUES and value not in CATEGORICAL_VALUES[col]:
                issues.append(f"row {i}: invalid {col} value {value!r}")
        for col in ("tenure", "SeniorCitizen"):
            try: int(row[col])
            except (ValueError, TypeError): issues.append(f"row {i}: {col} is not an integer")
        for col in ("MonthlyCharges",):
            try:
                if float(row[col]) < 0: raise ValueError
            except (ValueError, TypeError): issues.append(f"row {i}: invalid {col}")
        total = row.get("TotalCharges", "").strip()
        if total:
            try:
                if float(total) < 0: raise ValueError
            except (ValueError, TypeError): issues.append(f"row {i}: invalid TotalCharges")
        if row.get("TotalCharges", "").strip() == "" and row.get("tenure") != "0":
            issues.append(f"row {i}: TotalCharges missing for nonzero tenure")
        if row.get("TenureGroup") and row["TenureGroup"] != tenure_group(int(row["tenure"])):
            issues.append(f"row {i}: incorrect TenureGroup")
        if len(issues) >= 100: return issues + ["additional validation issues omitted"]
    return issues


def write_csv(path: str | Path, rows: list[dict[str, object]], columns: list[str]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with Path(path).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({c: "" if row.get(c) is None else row.get(c, "") for c in columns})
