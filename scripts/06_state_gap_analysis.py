"""
State-wise TB missed-case estimation using system-strength proxies and WHO totals.

Steps:
1. Load Ni-kshay/India TB Report exports (notifications, age/death distributions, 2024 partial tallies).
2. Merge NFHS-5 risk indicators and TB comorbidity programme metrics (diabetes, tobacco, alcohol).
3. Construct system and risk scores to inform detection probabilities.
4. Calibrate detection probabilities per state-year (2020–2023) so that national totals match WHO incidence.
5. Derive incidence, missed cases, scenario gaps, and generate outputs (tables, charts, maps, summary).

Run:
    python scripts/06_state_gap_analysis.py
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, Tuple

import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
OUTPUT_TABLES = ROOT / "output" / "tables"
OUTPUT_FIGURES = ROOT / "output" / "figures"
SUMMARY_PATH = ROOT / "reports" / "analysis_summary.md"
SPATIAL_PATH = ROOT / "data" / "spatial" / "india_states.geojson"

STATE_REPLACEMENTS: Dict[str, str] = {
    "andaman and nicobar islands": "Andaman & Nicobar Islands",
    "andaman & nicobar islands": "Andaman & Nicobar Islands",
    "dadra and nagar haveli and daman and diu": "Dadra & Nagar Haveli and Daman & Diu",
    "nct of delhi": "Delhi",
    "jammu & kashmir": "Jammu and Kashmir",
    "jammu and kashmir": "Jammu and Kashmir",
    "pondicherry": "Puducherry",
    "uttaranchal": "Uttarakhand",
    "odisha": "Odisha",
}


def standardize_state(name: str) -> str:
    if not isinstance(name, str):
        return name
    key = name.strip().lower()
    return STATE_REPLACEMENTS.get(key, name.strip())


def tidy_numeric(series: pd.Series) -> pd.Series:
    return (
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
        .replace({"": np.nan, "NA": np.nan, "N/A": np.nan})
        .astype(float)
    )


def read_notifications() -> pd.DataFrame:
    path = RAW_DIR / "RS_Session_260_AU_618_A_to_B_i.csv"
    df = pd.read_csv(path)
    df["state"] = df["State/UT"].apply(standardize_state)
    value_cols = [col for col in df.columns if col.isdigit()]
    notif = df[["state"] + value_cols].melt(id_vars="state", var_name="year", value_name="notifications")
    notif["year"] = notif["year"].astype(int)
    notif["notifications"] = tidy_numeric(notif["notifications"])
    notif = notif.dropna(subset=["notifications"])
    return notif


def read_age_distribution() -> pd.DataFrame:
    path = RAW_DIR / "RS_Session_266_AU_1736_A_to_C_3 (1).csv"
    df = pd.read_csv(path)
    df["state"] = df["State/UT"].apply(standardize_state)
    rename_map = {
        "percentage_of_tb_cases_out_of_the_total_tb_cases_notified_in_2023_januarydecember__0_to_14_years": "pct_cases_0_14_2023",
    }
    df = df.rename(columns=lambda c: c.strip())
    # Already in tidy format; keep as-is
    return df


def read_death_distribution() -> pd.DataFrame:
    path = RAW_DIR / "RS_Session_266_AU_1736_A_to_C_4.csv"
    df = pd.read_csv(path)
    df["state"] = df["State/UT"].apply(standardize_state)
    return df


def read_partial_notifications() -> pd.DataFrame:
    path = RAW_DIR / "RS_Session_266_AU_2511_1.csv"
    df = pd.read_csv(path)
    df["state"] = df["State/UT"].apply(standardize_state)
    df = df.rename(
        columns={
            "TB Cases Notification in 2024 (January to October)": "notif_jan_oct_2024",
            "TB Deaths - 2024 (January to October)": "deaths_jan_oct_2024",
        }
    )
    df["notif_jan_oct_2024"] = tidy_numeric(df["notif_jan_oct_2024"])
    df["deaths_jan_oct_2024"] = tidy_numeric(df["deaths_jan_oct_2024"])
    return df[["state", "notif_jan_oct_2024", "deaths_jan_oct_2024"]]


def read_treatment_outcomes() -> pd.DataFrame:
    path = RAW_DIR / "RS_Session_267_AU_3467_1.csv"
    df = pd.read_csv(path)
    df["state"] = df["State/UT"].apply(standardize_state)
    df = df.rename(
        columns={
            "2023 - TB Patients Notified": "notif_2023_report",
            "2023 - Treated Successfully": "treated_success_2023",
            "2024 - TB Patients Notified": "notif_2024_report",
        }
    )
    df["treatment_success_rate_2023"] = df["treated_success_2023"] / df["notif_2023_report"]
    return df[["state", "treatment_success_rate_2023", "notif_2024_report"]]


def read_nfhs_state_agg() -> pd.DataFrame:
    path = RAW_DIR / "nfhs5_state_agg.csv"
    df = pd.read_csv(path)
    df["state"] = df["state_ut"].apply(standardize_state)
    df = df.rename(
        columns={
            "Children under 5 years who are stunted (height-for-age)18 (%)": "stunting_pct",
            "Children under 5 years who are underweight (weight-for-age)18 (%)": "underweight_pct",
            "Children under 5 years who are wasted (weight-for-height)18 (%)": "wasting_pct",
            "Children age 6-59 months who are anaemic (<11.0 g/dl)22 (%)": "anemia_pct",
            "Men age 15 years and above who use any kind of tobacco (%)": "male_tobacco_pct",
            "Women age 15 years and above who use any kind of tobacco (%)": "female_tobacco_pct",
            "Men age 15 years and above who consume alcohol (%)": "male_alcohol_pct",
            "Population living in households that use an improved sanitation facility2 (%)": "sanitation_pct",
            "Households using clean fuel for cooking3 (%)": "cleanfuel_pct",
        }
    )
    cols = [
        "stunting_pct",
        "underweight_pct",
        "wasting_pct",
        "anemia_pct",
        "male_tobacco_pct",
        "female_tobacco_pct",
        "male_alcohol_pct",
        "sanitation_pct",
        "cleanfuel_pct",
    ]
    for col in cols:
        df[col] = tidy_numeric(df[col])
    return df[["state"] + cols]


def read_comorbidity(filename: str, pattern_map: Dict[str, str]) -> pd.DataFrame:
    path = RAW_DIR / filename
    df = pd.read_csv(path)
    df["state"] = df["State/Uts"].apply(standardize_state)

    def find_column(pattern: str) -> str:
        for col in df.columns:
            if pattern in col:
                return col
        raise KeyError(f"Column containing '{pattern}' not found in {filename}")

    subset = {"state": df["state"]}
    for new_name, pattern in pattern_map.items():
        col = find_column(pattern)
        values = tidy_numeric(df[col])
        subset[new_name] = values / 100.0
    return pd.DataFrame(subset)


def load_comorbidity_tables() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    dm = read_comorbidity(
        "2.10_TB_Diabetes.csv",
        {
            "dm_known_pct": "Percentage of TB - Diabetes-TB patients with known DM status",
            "dm_diagnosed_pct": "Percentage  of TB - Diabetes-  Patients diagnosed among tested",
            "dm_treated_pct": "Percentage of TB - Diabetes- patients initiated on Anti-diabetic treatment",
        },
    )
    tob = read_comorbidity(
        "2.11_TB_Tobacco.csv",
        {
            "tob_known_pct": "% of Tobacco-TB patients with known Tobacco usage status",
            "tob_user_pct": "Percentage  of Tobacco users identified amongst screened",
            "tob_linkage_pct": "Percentage  of Tobacco users linked with Tobacco cessation centres",
        },
    )
    alc = read_comorbidity(
        "2.12_TB_Alcohol.csv",
        {
            "alc_known_pct": "% of TB - Alcohol-TB patients with known Alcohol usage status",
            "alc_user_pct": "Percentage  of TB - Alcohol-Alcohol users identified amongst screened",
            "alc_linkage_pct": "Percentage  of No of TB - Alcohol-Alcohol users linked with Deaddiction centres",
        },
    )
    return dm, tob, alc


def build_features() -> pd.DataFrame:
    notif = read_notifications()
    nfhs = read_nfhs_state_agg()
    dm, tob, alc = load_comorbidity_tables()
    partial = read_partial_notifications()
    treatment = read_treatment_outcomes()

    latest_attrs = notif[notif["year"] == notif["year"].max()].copy()
    latest_attrs = latest_attrs.rename(columns={"notifications": "notifications_latest"})

    base = latest_attrs[
        ["state", "notifications_latest"]
    ].merge(nfhs, on="state", how="left")
    base = base.merge(dm, on="state", how="left")
    base = base.merge(tob, on="state", how="left")
    base = base.merge(alc, on="state", how="left")
    base = base.merge(partial, on="state", how="left")
    base = base.merge(treatment, on="state", how="left")

    # System-strength composite
    base["system_score"] = (
        0.3 * base["dm_known_pct"]
        + 0.15 * base["dm_treated_pct"]
        + 0.2 * base["tob_known_pct"]
        + 0.1 * base["tob_linkage_pct"]
        + 0.15 * base["alc_known_pct"]
        + 0.1 * base["alc_linkage_pct"]
    )
    base["system_score"] = base["system_score"].fillna(base["system_score"].median())

    # Risk composite: higher = higher TB burden
    risk_cols = [
        "stunting_pct",
        "underweight_pct",
        "wasting_pct",
        "anemia_pct",
        "male_tobacco_pct",
        "female_tobacco_pct",
        "male_alcohol_pct",
    ]
    protective_cols = ["sanitation_pct", "cleanfuel_pct"]
    for col in risk_cols + protective_cols:
        base[col] = base[col].fillna(base[col].median())
    for col in risk_cols + protective_cols:
        base[f"{col}_z"] = (base[col] - base[col].mean()) / (base[col].std(ddof=0) or 1)
    base["risk_score"] = base[[f"{c}_z" for c in risk_cols]].mean(axis=1) - base[
        [f"{c}_z" for c in protective_cols]
    ].mean(axis=1)

    base["system_z"] = (base["system_score"] - base["system_score"].mean()) / (base["system_score"].std(ddof=0) or 1)
    base["risk_z"] = (base["risk_score"] - base["risk_score"].mean()) / (base["risk_score"].std(ddof=0) or 1)

    return notif.merge(base, on="state", how="left")


def load_who_timeseries() -> pd.DataFrame:
    path = PROCESSED_DIR / "who_india_ts.csv"
    df = pd.read_csv(path)
    return df


def solve_detection_intercept(
    total_incidence: float,
    notifications: np.ndarray,
    system_z: np.ndarray,
    risk_z: np.ndarray,
    b_system: float = 0.9,
    b_risk: float = 0.5,
) -> float:
    scores = b_system * system_z - b_risk * risk_z

    def total_cases(intercept: float) -> float:
        logits = intercept + scores
        p = 1.0 / (1.0 + np.exp(-logits))
        return np.sum(notifications / p)

    low, high = -10.0, 5.0
    for _ in range(200):
        mid = (low + high) / 2.0
        current = total_cases(mid)
        if abs(current - total_incidence) / total_incidence < 1e-4:
            return mid
        if current > total_incidence:
            low = mid
        else:
            high = mid
    return (low + high) / 2.0


def compute_detection_panel(features: pd.DataFrame, who_ts: pd.DataFrame) -> pd.DataFrame:
    years = sorted(features["year"].unique())
    records = []
    state_meta = features.drop_duplicates("state")[["state", "system_z", "risk_z", "system_score", "risk_score"]]
    notif_targets = who_ts.set_index("year")["notifications"].to_dict()
    for year in years:
        notif_year = features[features["year"] == year].copy()
        target_total = notif_targets.get(year)
        if target_total is not None and not pd.isna(target_total) and notif_year["notifications"].sum() > 0:
            notif_year = notif_year.copy()
            notif_year["notifications"] *= target_total / notif_year["notifications"].sum()
        total_inc = float(who_ts.loc[who_ts["year"] == year, "incidence"].values[0])
        intercept = solve_detection_intercept(
            total_inc, notif_year["notifications"].to_numpy(), notif_year["system_z"].to_numpy(), notif_year["risk_z"].to_numpy()
        )
        logits = intercept + 0.9 * notif_year["system_z"] - 0.5 * notif_year["risk_z"]
        detection = 1.0 / (1.0 + np.exp(-logits))

        incidence = notif_year["notifications"] / detection
        missed = incidence - notif_year["notifications"]
        enriched = notif_year.assign(
            year=year,
            detection_prob=detection.to_numpy(),
            incidence_est=incidence.to_numpy(),
            missed_cases=missed.to_numpy(),
        )
        records.append(
            enriched[["state", "year", "notifications", "detection_prob", "incidence_est", "missed_cases"]]
        )
    panel = pd.concat(records, ignore_index=True)
    panel = panel.merge(state_meta, on="state", how="left")
    panel["detection_prob"] = panel["detection_prob"].clip(0.2, 0.98)
    panel["incidence_est"] = np.maximum(panel["incidence_est"], panel["notifications"] / 0.98)
    panel["missed_cases"] = panel["incidence_est"] - panel["notifications"]
    return panel


def categorize_states(panel: pd.DataFrame) -> pd.DataFrame:
    latest_year = panel["year"].max()
    latest = panel[panel["year"] == latest_year].copy()
    bins = pd.cut(
        latest["detection_prob"],
        bins=[0, 0.75, 0.85, 1],
        labels=["High gap (<75%)", "Moderate gap (75-85%)", "Low gap (>85%)"],
    )
    latest["gap_category"] = bins
    return latest


def write_tables(panel: pd.DataFrame) -> None:
    OUTPUT_TABLES.mkdir(parents=True, exist_ok=True)
    panel.to_csv(OUTPUT_TABLES / "state_detection_panel.csv", index=False)
    latest = categorize_states(panel)
    latest.sort_values("missed_cases", ascending=False).to_csv(
        OUTPUT_TABLES / "state_missed_cases_latest.csv", index=False
    )

    national = panel.groupby("year").agg(
        notifications=("notifications", "sum"),
        incidence=("incidence_est", "sum"),
        missed=("missed_cases", "sum"),
    )
    national["detection_rate"] = national["notifications"] / national["incidence"]
    national.to_csv(OUTPUT_TABLES / "national_detection_trends.csv")

    # Scenario table
    scenario_rows = []
    for target in (0.8, 0.9, 0.95):
        needed = np.maximum(target * panel["incidence_est"] - panel["notifications"], 0)
        scenario_rows.append(
            panel.assign(target_detection=target, additional_notifications=needed)
        )
    scenario_df = pd.concat(scenario_rows, ignore_index=True)
    scenario_df.to_csv(OUTPUT_TABLES / "state_detection_scenarios.csv", index=False)


def plot_national_trends(panel: pd.DataFrame) -> Path:
    national = panel.groupby("year").agg(
        notifications=("notifications", "sum"),
        incidence=("incidence_est", "sum"),
        missed=("missed_cases", "sum"),
    ).reset_index()
    plt.figure(figsize=(8, 5))
    plt.plot(national["year"], national["incidence"], marker="o", label="Incidence (modeled)")
    plt.plot(national["year"], national["notifications"], marker="o", label="Notifications")
    plt.fill_between(
        national["year"],
        national["notifications"],
        national["incidence"],
        color="#f4a259",
        alpha=0.3,
        label="Missed cases",
    )
    plt.ylabel("Cases")
    plt.title("India TB incidence vs notifications (2020–2023)")
    plt.legend()
    plt.tight_layout()
    OUTPUT_FIGURES.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_FIGURES / "national_trend.png"
    plt.savefig(path, dpi=300)
    plt.close()
    return path


def plot_top_states(panel: pd.DataFrame) -> Path:
    latest = panel[panel["year"] == panel["year"].max()].copy()
    top = latest.sort_values("missed_cases", ascending=False).head(10)
    plt.figure(figsize=(9, 6))
    sns.barplot(data=top, y="state", x="missed_cases", palette="Reds_r")
    plt.xlabel("Missed cases (incidence – notifications)")
    plt.ylabel("")
    plt.title(f"States with highest missed TB cases ({panel['year'].max()})")
    plt.tight_layout()
    path = OUTPUT_FIGURES / "top_states_missed.png"
    plt.savefig(path, dpi=300)
    plt.close()
    return path


STATE_TO_GEO = {
    "Andaman & Nicobar Islands": ["Andaman and Nicobar"],
    "Dadra & Nagar Haveli and Daman & Diu": ["Dadra and Nagar Haveli", "Daman and Diu"],
    "Odisha": ["Orissa"],
    "Uttarakhand": ["Uttaranchal"],
}


def plot_detection_map(panel: pd.DataFrame) -> Path:
    if not SPATIAL_PATH.exists():
        raise FileNotFoundError(f"GeoJSON not found at {SPATIAL_PATH}")
    latest = panel[panel["year"] == panel["year"].max()].copy()
    rows = []
    for _, row in latest.iterrows():
        state = row["state"]
        geo_names = STATE_TO_GEO.get(state, [state])
        for geo in geo_names:
            rows.append(
                {
                    "geo_name": geo,
                    "state": state,
                    "detection_prob": row["detection_prob"],
                }
            )
    geo_df = pd.DataFrame(rows)
    with SPATIAL_PATH.open() as fh:
        geojson = json.load(fh)
    fig = px.choropleth(
        geo_df,
        geojson=geojson,
        locations="geo_name",
        color="detection_prob",
        featureidkey="properties.NAME_1",
        color_continuous_scale="YlGnBu",
        range_color=(0.6, 0.95),
        labels={"detection_prob": "Detection"},
        title=f"Estimated TB detection coverage ({latest['year'].iloc[0]})",
    )
    fig.update_geos(fitbounds="locations", visible=False)
    html_path = OUTPUT_FIGURES / "state_detection_map.html"
    png_path = OUTPUT_FIGURES / "state_detection_map.png"
    fig.write_html(html_path)
    fig.write_image(png_path, scale=2)
    return png_path


def update_summary(panel: pd.DataFrame, figures: Dict[str, Path]) -> None:
    latest_year = panel["year"].max()
    latest = panel[panel["year"] == latest_year]
    national = latest.agg({"incidence_est": "sum", "notifications": "sum", "missed_cases": "sum"})
    detection_rate = national["notifications"] / national["incidence_est"]
    top_states = latest.sort_values("missed_cases", ascending=False).head(5)
    lines = [
        "# Analysis Summary: Missed TB Cases in India",
        "",
        f"*Updated automatically from scripts/06_state_gap_analysis.py on latest run.*",
        "",
        f"**Latest year ({latest_year})**",
        f"- Modeled incidence: {national['incidence_est']:,.0f} cases",
        f"- Notifications: {national['notifications']:,.0f} cases",
        f"- Missed cases: {national['missed_cases']:,.0f} (detection {detection_rate:.1%})",
        "",
        "**Highest missed-case burden**",
    ]
    for _, row in top_states.iterrows():
        lines.append(f"- {row['state']}: {row['missed_cases']:,.0f} missed (detection {row['detection_prob']:.0%})")
    lines.extend(
        [
            "",
            "See the generated figures for quick reference:",
        ]
    )
    for label, path in figures.items():
        rel = path.relative_to(ROOT)
        lines.append(f"- {label}: `{rel.as_posix()}`")
    SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    sns.set_style("whitegrid")
    features = build_features()
    who_ts = load_who_timeseries()
    panel = compute_detection_panel(features, who_ts)
    write_tables(panel)
    fig_paths = {
        "National trend": plot_national_trends(panel),
        "Top states": plot_top_states(panel),
        "Detection map": plot_detection_map(panel),
    }
    update_summary(panel, fig_paths)
    print("[06_state_gap_analysis] Analysis complete.")


if __name__ == "__main__":
    main()
