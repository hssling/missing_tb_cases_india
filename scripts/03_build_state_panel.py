"""
Merge notifications, incidence estimates, and covariates into a state-year panel.

Usage:
    python scripts/03_build_state_panel.py
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Optional

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

NOTIF_PATH = PROCESSED_DIR / "india_tb_state_notif.csv"
INCIDENCE_PATH = RAW_DIR / "india_tb_burden_model_state.xlsx"
NFHS_PATH = RAW_DIR / "nfhs_state_indicators.csv"
CENSUS_PATH = RAW_DIR / "census_state_indicators.csv"
PREVALENCE_PATH = RAW_DIR / "tb_prevalence_survey.xlsx"
PRIOR_PATH = RAW_DIR / "priors_cascade_inventory.csv"
OUTPUT_PATH = PROCESSED_DIR / "state_year_panel.csv"


def read_csv_or_none(path: Path, **kwargs) -> Optional[pd.DataFrame]:
    if not path.exists():
        print(f"[03_build_state_panel] Optional file missing: {path.name}")
        return None
    return pd.read_csv(path, **kwargs)


def read_excel_or_none(path: Path, **kwargs) -> Optional[pd.DataFrame]:
    if not path.exists():
        print(f"[03_build_state_panel] Optional file missing: {path.name}")
        return None
    return pd.read_excel(path, **kwargs)


def load_notifications() -> pd.DataFrame:
    if not NOTIF_PATH.exists():
        raise FileNotFoundError(
            f"Notification file not found at {NOTIF_PATH}. Run scripts/02_ingest_india_tb_reports.py first."
        )
    notif = pd.read_csv(NOTIF_PATH)
    notif["state"] = notif["state"].astype(str)
    notif["year"] = notif["year"].astype(int)
    return notif


def load_incidence() -> pd.DataFrame:
    if not INCIDENCE_PATH.exists():
        raise FileNotFoundError(
            f"Incidence file missing: {INCIDENCE_PATH}. Drop the indigenous TB burden model export there."
        )
    inc = pd.read_excel(INCIDENCE_PATH)
    inc.columns = [c.strip().lower() for c in inc.columns]
    state_col = next((c for c in inc.columns if "state" in c), None)
    year_col = next((c for c in inc.columns if "year" in c), None)
    value_col = next(
        (c for c in inc.columns if "incidence" in c or "cases" in c or "estimate" in c),
        None,
    )
    if not all([state_col, year_col, value_col]):
        raise KeyError("Incidence file must contain state, year, and incidence columns.")
    inc = inc[[state_col, year_col, value_col]].rename(
        columns={state_col: "state", year_col: "year", value_col: "incidence_est"}
    )
    inc["state"] = inc["state"].astype(str)
    inc["year"] = inc["year"].astype(int)
    inc["incidence_est"] = inc["incidence_est"].astype(float)
    return inc


def derive_cascade_fraction(prevalence_df: pd.DataFrame) -> pd.DataFrame:
    df = prevalence_df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    state_col = next((c for c in df.columns if "state" in c), None)
    registered_col = next((c for c in df.columns if "registered" in c or "ntep" in c), None)
    diagnosed_col = next((c for c in df.columns if "diagnosed" in c), None)
    if not state_col:
        raise KeyError("Prevalence survey sheet must include a state column.")

    outputs = []
    for _, row in df.iterrows():
        state = str(row[state_col])
        diag_frac = None
        if diagnosed_col and isinstance(row[diagnosed_col], (int, float)):
            diag_frac = row[diagnosed_col] / 100 if row[diagnosed_col] > 1 else row[diagnosed_col]
        reg_frac = None
        if registered_col and isinstance(row[registered_col], (int, float)):
            reg_frac = row[registered_col] / 100 if row[registered_col] > 1 else row[registered_col]
        cascade_frac = reg_frac or diag_frac
        if cascade_frac is None or math.isnan(cascade_frac):
            continue
        outputs.append({"state": state, "cascade_registration_frac": cascade_frac})
    return pd.DataFrame(outputs)


def merge_covariates(panel: pd.DataFrame, nfhs: Optional[pd.DataFrame], census: Optional[pd.DataFrame]) -> pd.DataFrame:
    out = panel.copy()
    if nfhs is not None:
        nfhs_cols = [c for c in nfhs.columns if c.lower() != "state"]
        out = out.merge(nfhs, on="state", how="left", validate="many_to_one")
        print(f"[03_build_state_panel] Merged NFHS indicators ({len(nfhs_cols)} columns).")
    if census is not None:
        out = out.merge(census, on="state", how="left", suffixes=("", "_census"))
        print(f"[03_build_state_panel] Merged Census indicators.")
    return out


def apply_detection_priors(panel: pd.DataFrame, priors: Optional[pd.DataFrame]) -> pd.DataFrame:
    out = panel.copy()
    if priors is None:
        out["detection_prior_mean"] = pd.NA
        out["detection_prior_sd"] = pd.NA
        return out

    priors.columns = [c.strip().lower() for c in priors.columns]
    state_col = next((c for c in priors.columns if "state" in c), None)
    mean_col = next((c for c in priors.columns if "mean" in c), None)
    sd_col = next((c for c in priors.columns if "sd" in c or "se" in c), None)
    if not state_col or not mean_col:
        raise KeyError("Priors file must include state and mean columns.")

    priors = priors.rename(columns={state_col: "state", mean_col: "detection_prior_mean"})
    if sd_col:
        priors = priors.rename(columns={sd_col: "detection_prior_sd"})
    else:
        priors["detection_prior_sd"] = 0.15

    out = out.merge(priors, on="state", how="left")
    return out


def main() -> None:
    notifications = load_notifications()
    incidence = load_incidence()
    prevalence = read_excel_or_none(PREVALENCE_PATH)
    nfhs = read_csv_or_none(NFHS_PATH)
    census = read_csv_or_none(CENSUS_PATH)
    priors = read_csv_or_none(PRIOR_PATH)

    panel = notifications.merge(incidence, on=["state", "year"], how="left", validate="many_to_one")
    if panel["incidence_est"].isna().any():
        missing_states = panel.loc[panel["incidence_est"].isna(), "state"].unique()
        print(f"[03_build_state_panel] Warning: missing incidence for states: {missing_states}")

    panel["missed"] = panel["incidence_est"] - panel["notifications"]
    panel["detection_cov"] = panel["notifications"] / panel["incidence_est"]

    if prevalence is not None:
        cascade = derive_cascade_fraction(prevalence)
        panel = panel.merge(cascade, on="state", how="left")

    panel = merge_covariates(panel, nfhs, census)
    panel = apply_detection_priors(panel, priors)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    panel.to_csv(OUTPUT_PATH, index=False)
    print(f"[03_build_state_panel] State-year panel saved to {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
