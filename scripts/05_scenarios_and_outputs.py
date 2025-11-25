"""
Summarize posterior draws, build scenario tables, and render Markdown outputs.

Usage:
    python scripts/05_scenarios_and_outputs.py
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, List

import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PANEL_PATH = ROOT / "data" / "processed" / "state_year_panel.csv"
MODEL_PATH = ROOT / "models" / "tb_state_model.nc"
TABLE_DIR = ROOT / "output" / "tables"
FIG_DIR = ROOT / "output" / "figures"
REPORT_PATH = ROOT / "reports" / "analysis_summary.md"

SCENARIO_TARGETS = [0.8, 0.9, 0.95]


def load_inputs() -> tuple[pd.DataFrame, az.InferenceData]:
    if not PANEL_PATH.exists():
        raise FileNotFoundError(f"State-year panel missing at {PANEL_PATH}. Run script 03.")
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Posterior file missing at {MODEL_PATH}. Run script 04.")
    panel = pd.read_csv(PANEL_PATH)
    posterior = az.from_netcdf(MODEL_PATH)
    return panel, posterior


def summarize_posterior(panel: pd.DataFrame, posterior: az.InferenceData) -> pd.DataFrame:
    det = posterior.posterior["detection_prob"].stack(sample=("chain", "draw"))
    inc = posterior.posterior["incidence"].stack(sample=("chain", "draw"))
    det_mean = det.mean("sample").values
    det_lo = det.quantile(0.025, dim="sample").values
    det_hi = det.quantile(0.975, dim="sample").values

    inc_mean = inc.mean("sample").values
    inc_lo = inc.quantile(0.025, dim="sample").values
    inc_hi = inc.quantile(0.975, dim="sample").values

    notif = panel["notifications"].to_numpy()
    missed_mean = inc_mean - notif
    missed_lo = inc_lo - notif
    missed_hi = inc_hi - notif

    summary = panel[["state", "year"]].copy()
    summary["incidence_mean"] = inc_mean
    summary["incidence_lo"] = inc_lo
    summary["incidence_hi"] = inc_hi
    summary["detection_mean"] = det_mean
    summary["detection_lo"] = det_lo
    summary["detection_hi"] = det_hi
    summary["missed_mean"] = missed_mean
    summary["missed_lo"] = missed_lo
    summary["missed_hi"] = missed_hi
    summary["notifications"] = notif
    return summary


def build_scenarios(summary: pd.DataFrame) -> pd.DataFrame:
    rows: List[Dict[str, float]] = []
    for _, row in summary.iterrows():
        incidence = row["incidence_mean"]
        notifications = row["notifications"]
        for target in SCENARIO_TARGETS:
            needed = max(0.0, target * incidence - notifications)
            rows.append(
                {
                    "state": row["state"],
                    "year": row["year"],
                    "target_detection": target,
                    "additional_notifications_needed": needed,
                }
            )
    return pd.DataFrame(rows)


def plot_national_trend(summary: pd.DataFrame) -> None:
    national = summary.groupby("year").agg(
        incidence=("incidence_mean", "sum"),
        notifications=("notifications", "sum"),
        missed=("missed_mean", "sum"),
    ).sort_index()
    plt.figure(figsize=(8, 5))
    plt.plot(national.index, national["incidence"], label="Incidence (posterior mean)")
    plt.plot(national.index, national["notifications"], label="Notifications")
    plt.plot(national.index, national["missed"], label="Missed cases")
    plt.ylabel("Cases")
    plt.xlabel("Year")
    plt.title("India TB incidence vs notifications")
    plt.legend()
    plt.tight_layout()
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig_path = FIG_DIR / "national_trend.png"
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"[05_scenarios_and_outputs] Saved figure to {fig_path.relative_to(ROOT)}")


def write_tables(summary: pd.DataFrame, scenarios: pd.DataFrame) -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    summary.to_csv(TABLE_DIR / "state_summary.csv", index=False)
    scenarios.to_csv(TABLE_DIR / "state_scenarios.csv", index=False)
    print(f"[05_scenarios_and_outputs] Tables written to {TABLE_DIR.relative_to(ROOT)}")


def render_report(summary: pd.DataFrame, scenarios: pd.DataFrame) -> None:
    latest_year = summary["year"].max()
    latest = summary[summary["year"] == latest_year]
    national_incidence = latest["incidence_mean"].sum()
    national_notifications = latest["notifications"].sum()
    national_missed = latest["missed_mean"].sum()
    detection_rate = national_notifications / national_incidence if national_incidence else np.nan
    detection_rate_str = f"{detection_rate:.1%}" if np.isfinite(detection_rate) else "NA"

    high_gap_states = (
        latest.sort_values("missed_mean", ascending=False)
        .head(5)[["state", "missed_mean", "detection_mean"]]
    )

    report_lines = [
        "# Analysis Summary: Missed TB Cases in India",
        f"_Auto-generated on {datetime.utcnow().isoformat()}Z_",
        "",
        f"**Latest year ({latest_year}) highlights**",
        f"- Posterior incidence: {national_incidence:,.0f} cases",
        f"- Notifications: {national_notifications:,.0f} cases",
        f"- Estimated missed cases: {national_missed:,.0f} ({detection_rate_str} detection)",
        "",
        "**Top states by missed cases**",
    ]
    if high_gap_states.empty:
        report_lines.append("- Not enough data to rank states.")
    else:
        for _, row in high_gap_states.iterrows():
            det = row["detection_mean"]
            det_str = f"{det:.0%}" if det == det else "NA"
            report_lines.append(f"- {row['state']}: {row['missed_mean']:,.0f} missed, detection {det_str}")

    report_lines.extend(
        [
            "",
            "State-level scenario requirements (additional notifications to reach detection targets) "
            "are available in `output/tables/state_scenarios.csv`.",
        ]
    )

    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"[05_scenarios_and_outputs] Report updated at {REPORT_PATH.relative_to(ROOT)}")


def main() -> None:
    panel, posterior = load_inputs()
    summary = summarize_posterior(panel, posterior)
    scenarios = build_scenarios(summary)
    write_tables(summary, scenarios)
    plot_national_trend(summary)
    render_report(summary, scenarios)


if __name__ == "__main__":
    main()
