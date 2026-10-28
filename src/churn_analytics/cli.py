"""Command line entry point for the reproducible analysis."""
import argparse, json, sqlite3
from pathlib import Path
from .analysis import run_analysis
from .data import load_csv, validate_rows
from .sql_workflow import build_database, run_sql, verify_parity


def main() -> None:
    p = argparse.ArgumentParser(description="Run telecom churn validation and analysis")
    p.add_argument("--source", default="data/customer_churn.csv")
    p.add_argument("--reports", default="reports")
    p.add_argument("--database", default="reports/customer_churn.sqlite")
    args = p.parse_args()
    raw = load_csv(args.source); issues = validate_rows(raw)
    if issues: raise SystemExit("Validation failed: " + "; ".join(issues[:10]))
    result = run_analysis(args.source, args.reports)
    db = build_database(args.source, args.database)
    parity = verify_parity(result["rows"], db)
    if parity: raise SystemExit("Parity failed: " + "; ".join(parity))
    for file in ["data_validation.sql", "churn_analysis.sql", "customer_segmentation.sql"]:
        name = Path(file).stem
        with (Path(args.reports) / f"{name}.csv").open("w", newline="", encoding="utf-8") as f:
            cur = db.execute((Path(__file__).resolve().parents[2] / "sql" / file).read_text(encoding="utf-8"))
            writer = __import__("csv").writer(f); writer.writerow([x[0] for x in cur.description]); writer.writerows(cur.fetchall())
    db.close()
    print(json.dumps({"validated_rows": len(raw), "issues": issues, "python_sql_parity": "PASS", "overall": result["overall"]}, indent=2))

if __name__ == "__main__": main()
