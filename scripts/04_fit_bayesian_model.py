"""
Hierarchical Bayesian model for state-wise TB incidence and detection probabilities.

Usage:
    python scripts/04_fit_bayesian_model.py --draws 1000 --tune 1000 --chains 2
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import List

import arviz as az
import numpy as np
import pandas as pd
import pymc as pm


ROOT = Path(__file__).resolve().parents[1]
PANEL_PATH = ROOT / "data" / "processed" / "state_year_panel.csv"
MODEL_PATH = ROOT / "models" / "tb_state_model.nc"

BASE_COLUMNS = {
    "state",
    "year",
    "notifications",
    "incidence_est",
    "missed",
    "detection_cov",
    "cascade_registration_frac",
    "detection_prior_mean",
    "detection_prior_sd",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fit Bayesian model for missed TB cases.")
    parser.add_argument("--draws", type=int, default=1000, help="Posterior draws per chain.")
    parser.add_argument("--tune", type=int, default=1000, help="Tuning steps per chain.")
    parser.add_argument("--chains", type=int, default=4, help="Number of MCMC chains.")
    parser.add_argument("--target-accept", type=float, default=0.9, help="Sampler target_accept.")
    return parser.parse_args()


def prepare_data() -> pd.DataFrame:
    if not PANEL_PATH.exists():
        raise FileNotFoundError(f"State-year panel not found at {PANEL_PATH}. Run script 03 first.")
    df = pd.read_csv(PANEL_PATH)
    df = df.dropna(subset=["state", "year", "notifications"])
    if df.empty:
        raise ValueError("State-year panel is empty after dropping NaNs.")
    df["state"] = df["state"].astype(str)
    df["year"] = df["year"].astype(int)
    df["notifications"] = df["notifications"].fillna(0).clip(lower=0)
    df["incidence_est"] = df["incidence_est"].fillna(df["notifications"] * 1.2 + 1)
    df["incidence_est"] = df["incidence_est"].clip(lower=1)
    return df


def detect_covariates(df: pd.DataFrame) -> List[str]:
    covariates: List[str] = []
    for col in df.columns:
        if col in BASE_COLUMNS:
            continue
        if df[col].dtype.kind not in {"i", "u", "f"}:
            continue
        if df[col].isna().all():
            continue
        covariates.append(col)
    return covariates


def logit(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, 1e-6, 1 - 1e-6)
    return np.log(x / (1 - x))


def build_and_sample(df: pd.DataFrame, args: argparse.Namespace) -> az.InferenceData:
    states = sorted(df["state"].unique())
    state_index = {state: idx for idx, state in enumerate(states)}
    df["state_idx"] = df["state"].map(state_index)
    years = df["year"].values.astype(float)
    year_scaled = (years - years.mean()) / (years.std() or 1)
    covariate_cols = detect_covariates(df)
    cov_matrix = None
    if covariate_cols:
        cov_matrix = df[covariate_cols].apply(lambda col: (col - col.mean()) / (col.std() or 1), axis=0).to_numpy()

    incidence_prior = df["incidence_est"].to_numpy(dtype=float)
    notif_obs = df["notifications"].to_numpy(dtype=float)
    state_idx = df["state_idx"].to_numpy(dtype=int)

    detection_prior_mean = df.get("detection_prior_mean")
    detection_prior_sd = df.get("detection_prior_sd")
    has_prior = detection_prior_mean is not None and detection_prior_mean.notna().any()
    if has_prior:
        prior_mask = detection_prior_mean.notna().to_numpy()
        prior_indices = np.nonzero(prior_mask)[0]
        prior_targets = logit(detection_prior_mean.fillna(0.5).to_numpy())
        prior_sd_vals = detection_prior_sd.fillna(0.35).to_numpy()

    coords = {
        "obs": np.arange(len(df)),
        "state": states,
    }
    if covariate_cols:
        coords["covariate"] = covariate_cols

    with pm.Model(coords=coords) as model:
        sigma_state = pm.Exponential("sigma_state", 1.0)
        state_offset = pm.Normal("state_offset", mu=0, sigma=sigma_state, dims="state")
        time_slope = pm.Normal("time_slope", mu=0, sigma=0.5)
        base_logit = pm.Normal("base_logit", mu=0, sigma=1.5)

        if covariate_cols:
            beta = pm.Normal("beta", mu=0, sigma=0.5, dims="covariate")
            cov_term = pm.math.dot(cov_matrix, beta)
        else:
            cov_term = 0

        logit_p = (
            base_logit
            + time_slope * year_scaled
            + state_offset[state_idx]
            + cov_term
        )
        detection_prob = pm.Deterministic("detection_prob", pm.math.sigmoid(logit_p), dims="obs")

        log_incidence = pm.Normal(
            "log_incidence",
            mu=np.log(incidence_prior),
            sigma=0.35,
            dims="obs",
        )
        incidence = pm.Deterministic("incidence", pm.math.exp(log_incidence), dims="obs")

        pm.Poisson("notifications", mu=incidence * detection_prob, observed=notif_obs, dims="obs")

        if has_prior and prior_indices.size:
            pm.Normal(
                "detection_prior_constraint",
                mu=prior_targets[prior_indices],
                sigma=prior_sd_vals[prior_indices],
                observed=logit_p[prior_indices],
            )

        trace = pm.sample(
            draws=args.draws,
            tune=args.tune,
            chains=args.chains,
            target_accept=args.target_accept,
            progressbar=True,
        )

    return trace


def main() -> None:
    args = parse_args()
    df = prepare_data()
    trace = build_and_sample(df, args)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    az.to_netcdf(trace, MODEL_PATH)
    print(f"[04_fit_bayesian_model] Saved posterior draws to {MODEL_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
