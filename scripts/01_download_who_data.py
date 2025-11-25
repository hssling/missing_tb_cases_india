"""
Download and preprocess WHO Global TB data for India.

Usage:
    python scripts/01_download_who_data.py --url https://example.com/who_tb.csv

If --url is omitted, the script will look for an environment variable
WHO_TB_DATA_URL. When no URL is provided it assumes the raw CSV already exists
at data/raw/who_tb_global.csv and skips the download step.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "who_tb_global.csv"
PROCESSED_PATH = ROOT / "data" / "processed" / "who_india_ts.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download and clean WHO TB data for India.")
    parser.add_argument("--url", help="URL to WHO TB CSV. Overrides WHO_TB_DATA_URL environment variable.")
    return parser.parse_args()


def download_who_csv(url: str) -> None:
    print(f"[01_download_who_data] Downloading WHO TB data from {url}")
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    RAW_PATH.write_bytes(response.content)
    print(f"[01_download_who_data] Saved raw CSV to {RAW_PATH.relative_to(ROOT)}")


def load_who_data() -> pd.DataFrame:
    if not RAW_PATH.exists():
        raise FileNotFoundError(
            f"Raw WHO file not found at {RAW_PATH}. "
            "Provide --url or set WHO_TB_DATA_URL to download it."
        )

    print(f"[01_download_who_data] Reading {RAW_PATH.relative_to(ROOT)}")
    df = pd.read_csv(RAW_PATH)
    return df


def clean_india_series(df: pd.DataFrame) -> pd.DataFrame:
    country_col = None
    for candidate in ("country", "Country", "country_name"):
        if candidate in df.columns:
            country_col = candidate
            break
    if country_col is None:
        raise KeyError("Country column not found. Ensure WHO CSV has a 'country' field.")

    india_df = df[df[country_col].str.lower().eq("india")].copy()
    if india_df.empty:
        raise ValueError("No India rows detected in WHO dataset.")

    rename_map = {
        "year": "year",
        "e_inc_num": "incidence",
        "e_inc_num_lo": "incidence_ci_low",
        "e_inc_num_hi": "incidence_ci_high",
        "e_mort_num": "mortality",
        "notif_all_tb": "notifications",
    }

    selected_cols = {}
    for raw_name, new_name in rename_map.items():
        if raw_name in india_df.columns:
            selected_cols[new_name] = india_df[raw_name]
        else:
            selected_cols[new_name] = pd.Series([pd.NA] * len(india_df))

    cleaned = pd.DataFrame(selected_cols)
    if "year" not in cleaned.columns or cleaned["year"].isna().all():
        if "year" in india_df.columns:
            cleaned["year"] = india_df["year"]
        else:
            raise KeyError("Year column missing from WHO dataset.")

    cleaned = cleaned.sort_values("year").reset_index(drop=True)
    cleaned["missed_cases"] = cleaned["incidence"] - cleaned["notifications"]
    cleaned["detection_coverage"] = cleaned["notifications"] / cleaned["incidence"]

    return cleaned


def main() -> None:
    args = parse_args()
    url = args.url or os.environ.get("WHO_TB_DATA_URL")
    if url:
        try:
            download_who_csv(url)
        except Exception as exc:
            print(f"[01_download_who_data] Download failed: {exc}", file=sys.stderr)
            raise

    df = load_who_data()
    cleaned = clean_india_series(df)

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(PROCESSED_PATH, index=False)
    print(f"[01_download_who_data] Wrote cleaned India series to {PROCESSED_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
