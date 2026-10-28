"""SQLite import, SQL execution, and Python/SQL parity checks."""
from __future__ import annotations
import csv, sqlite3
from pathlib import Path
from .data import EXPECTED_COLUMNS, clean_rows, load_csv, validate_rows

ROOT = Path(__file__).resolve().parents[2]


def build_database(source: str | Path, db_path: str | Path) -> sqlite3.Connection:
    raw = load_csv(source); issues = validate_rows(raw)
    if issues: raise ValueError("Source data validation failed: " + "; ".join(issues[:10]))
    rows = clean_rows(raw)
    db = sqlite3.connect(db_path)
    db.executescript((ROOT / "sql" / "schema.sql").read_text(encoding="utf-8"))
    fields = EXPECTED_COLUMNS + ["TenureGroup"]
    cols = ",".join('"' + x + '"' for x in fields)
    marks = ",".join("?" for _ in fields)
    db.executemany(f"INSERT INTO customers ({cols}) VALUES ({marks})", [tuple(r[x] for x in fields) for r in rows])
    db.commit()
    return db


def run_sql(db: sqlite3.Connection, script: str) -> list[tuple]:
    return db.execute((ROOT / "sql" / script).read_text(encoding="utf-8")).fetchall()


def verify_parity(rows: list[dict[str, object]], db: sqlite3.Connection) -> list[str]:
    issues = []
    sql_total = db.execute("SELECT COUNT(*), SUM(Churn='Yes'), AVG(Churn='Yes') FROM customers").fetchone()
    py_total = (len(rows), sum(r["Churn"] == "Yes" for r in rows), sum(r["Churn"] == "Yes" for r in rows) / len(rows))
    if sql_total[:2] != py_total[:2] or abs(sql_total[2] - py_total[2]) > 1e-12: issues.append("overall churn differs between Python and SQL")
    for dim in ["Contract", "TenureGroup", "PaymentMethod", "InternetService", "Dependents", "Partner", "SeniorCitizen"]:
        actual = db.execute(f'SELECT "{dim}", COUNT(*), SUM(Churn=\'Yes\'), AVG(Churn=\'Yes\') FROM customers GROUP BY "{dim}"').fetchall()
        expected = {}
        for r in rows:
            key = str(r[dim]); agg = expected.setdefault(key, [0, 0]); agg[0] += 1; agg[1] += r["Churn"] == "Yes"
        got = {str(k): (n, c, rate) for k,n,c,rate in actual}
        for k, (n,c) in expected.items():
            if k not in got or got[k][:2] != (n,c) or abs(got[k][2] - c/n) > 1e-12:
                issues.append(f"Python/SQL mismatch for {dim}={k}")
    return issues
