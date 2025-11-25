"""
Clean India TB Report / Ni-kshay state-wise notifications.

Usage:
    python scripts/02_ingest_india_tb_reports.py --input data/raw/india_tb_reports_statewise.xlsx
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, List

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DEFAULT = ROOT / "data" / "raw" / "india_tb_reports_statewise.xlsx"
OUTPUT_PATH = ROOT / "data" / "processed" / "india_tb_state_notif.csv"

STATE_REPLACEMENTS: Dict[str, str] = {
    "andaman & nicobar islands": "Andaman & Nicobar Islands",
    "andaman and nicobar islands": "Andaman & Nicobar Islands",
    "nct of delhi": "Delhi",
    "pondicherry": "Puducherry",
    "dadra & nagar haveli and daman & diu": "Dadra & Nagar Haveli and Daman & Diu",
    "uttaranchal": "Uttarakhand",
    "orissa": "Odisha",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Standardize India TB Report state notifications.")
    parser.add_argument("--input", type=Path, default=RAW_DEFAULT, help="Path to Excel export.")
    parser.add_argument("--sheet", help="Sheet name to read (defaults to first sheet).")
    return parser.parse_args()


def standardize_state(name: str) -> str:
    if not isinstance(name, str):
        return name
    normalized = name.strip()
    normalized = re.sub(r"\s+", " ", normalized)
    key = normalized.lower()
    normalized = STATE_REPLACEMENTS.get(key, normalized.title())
    return normalized


def find_state_column(columns: List[str]) -> str:
    for candidate in columns:
        lc = candidate.lower()
        if "state" in lc or "ut" in lc or "name" in lc:
            return candidate
    raise KeyError("State column not found. Please ensure the Excel file has a state/UT column.")


def reshape_notifications(df: pd.DataFrame, state_col: str) -> pd.DataFrame:
    year_cols = []
    for col in df.columns:
        if col == state_col:
            continue
        simplified = re.sub(r"\D", "", str(col))
        if simplified.isdigit() and len(simplified) == 4:
            year_cols.append(col)
    if not year_cols:
        raise ValueError("No year columns detected. Ensure columns are labeled with years (e.g., 2020).")

    tidy = (
        df.melt(id_vars=[state_col], value_vars=year_cols, var_name="year", value_name="notifications")
        .dropna(subset=["notifications"])
    )
    tidy["state"] = tidy[state_col].apply(standardize_state)
    tidy["year"] = tidy["year"].astype(str).str.extract(r"(\d{4})").astype(int)
    tidy = tidy[~tidy["state"].str.contains("total", case=False, na=False)]
    tidy = tidy.drop(columns=[state_col])
    tidy = tidy[["state", "year", "notifications"]]
    tidy = tidy.sort_values(["state", "year"]).reset_index(drop=True)
    return tidy


def main() -> None:
    args = parse_args()
    input_path = args.input
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    df = pd.read_excel(input_path, sheet_name=args.sheet or 0)
    if df.empty:
        raise ValueError("Input Excel sheet is empty.")

    state_col = find_state_column(df.columns.tolist())
    tidy = reshape_notifications(df, state_col)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    tidy.to_csv(OUTPUT_PATH, index=False)
    print(f"[02_ingest_india_tb_reports] Wrote cleaned notifications to {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
