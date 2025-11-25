"""
Build WHO India time series from the offline WHO CSV exports placed in data/raw/.

Expected raw files (downloaded from the WHO TB data portal):
    - data/raw/TB_burden_countries_2025-11-23.csv
    - data/raw/TB_notifications_2025-11-23.csv

Outputs:
    - data/processed/who_india_ts.csv with columns:
        year, incidence, incidence_ci_low, incidence_ci_high, notifications,
        mortality, mortality_ci_low, mortality_ci_high, population,
        cdr (case detection ratio), cdr_ci_low, cdr_ci_high

Run:
    python scripts/07_process_who_resource_files.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"

BURDEN_PATH = RAW_DIR / "TB_burden_countries_2025-11-23.csv"
NOTIF_PATH = RAW_DIR / "TB_notifications_2025-11-23.csv"
OUTPUT_PATH = PROCESSED_DIR / "who_india_ts.csv"


def load_burden() -> pd.DataFrame:
    if not BURDEN_PATH.exists():
        raise FileNotFoundError(
            f"Missing WHO burden file at {BURDEN_PATH}. "
            "Place TB_burden_countries_2025-11-23.csv in data/raw/."
        )
    df = pd.read_csv(BURDEN_PATH)
    india = df[df["country"] == "India"].copy()
    keep_cols = {
        "year": "year",
        "e_pop_num": "population",
        "e_inc_num": "incidence",
        "e_inc_num_lo": "incidence_ci_low",
        "e_inc_num_hi": "incidence_ci_high",
        "e_mort_num": "mortality",
        "e_mort_num_lo": "mortality_ci_low",
        "e_mort_num_hi": "mortality_ci_high",
        "c_cdr": "cdr",
        "c_cdr_lo": "cdr_ci_low",
        "c_cdr_hi": "cdr_ci_high",
    }
    india = india[list(keep_cols.keys())].rename(columns=keep_cols)
    india["year"] = india["year"].astype(int)
    return india


def load_notifications() -> pd.DataFrame:
    if not NOTIF_PATH.exists():
        raise FileNotFoundError(
            f"Missing WHO notifications file at {NOTIF_PATH}. "
            "Place TB_notifications_2025-11-23.csv in data/raw/."
        )
    df = pd.read_csv(NOTIF_PATH)
    india = df[df["country"] == "India"].copy()
    if "c_newinc" not in india.columns:
        raise KeyError("Column 'c_newinc' not found in WHO notifications CSV.")
    return india[["year", "c_newinc"]].rename(columns={"c_newinc": "notifications"})


def main() -> None:
    burden = load_burden()
    notifications = load_notifications()
    merged = burden.merge(notifications, on="year", how="left")
    merged = merged.sort_values("year")
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    merged.to_csv(OUTPUT_PATH, index=False)
    print(f"[07_process_who_resource_files] Saved WHO India time series to {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
