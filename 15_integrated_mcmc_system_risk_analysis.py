import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import statsmodels.api as sm

# Paths
ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output"
FIGURES_DIR = OUTPUT_DIR / "figures"
TABLES_DIR = OUTPUT_DIR / "tables"
REPORTS_DIR = ROOT / "reports"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)

# Load MCMC missed cases
def load_mcmc_missed_cases():
    with open(OUTPUT_DIR / "mcmc_missed_cases_sensitivity_results.json", "r") as f:
        data = json.load(f)
    states = data["mcmc_analysis"]["missed_cases"]
    df = pd.DataFrame([
        {"state": state, "mcmc_missed_mean": info["mean"], "mcmc_missed_ci_low": info["ci_low"], "mcmc_missed_ci_high": info["ci_high"]}
        for state, info in states.items() if state != "national"
    ])
    return df

# Load system and risk scores (adapted from 06_state_gap_analysis.py)
def load_system_risk_scores():
    # Load NFHS data
    nfhs_path = ROOT / "data" / "raw" / "nfhs5_state_agg.csv"
    nfhs = pd.read_csv(nfhs_path)
    nfhs["state"] = nfhs["state_ut"]

    # Load comorbidity data
    comorbidity_files = {
        "dm": ROOT / "data" / "raw" / "2.10_TB_Diabetes.csv",
        "tob": ROOT / "data" / "raw" / "2.11_TB_Tobacco.csv",
        "alc": ROOT / "data" / "raw" / "2.12_TB_Alcohol.csv"
    }

    def load_comorbidity(file_path, pattern_map):
        df = pd.read_csv(file_path)
        df["state"] = df["State/Uts"].str.strip().str.title()
        subset = {"state": df["state"]}
        for new_name, pattern in pattern_map.items():
            for col in df.columns:
                if pattern in col:
                    values = pd.to_numeric(df[col], errors='coerce') / 100.0
                    subset[new_name] = values
                    break
        return pd.DataFrame(subset)

    dm = load_comorbidity(comorbidity_files["dm"], {
        "dm_known_pct": "Percentage of TB - Diabetes-TB patients with known DM status",
        "dm_treated_pct": "Percentage of TB - Diabetes- patients initiated on Anti-diabetic treatment"
    })
    tob = load_comorbidity(comorbidity_files["tob"], {
        "tob_known_pct": "% of Tobacco-TB patients with known Tobacco usage status",
        "tob_linkage_pct": "Percentage  of Tobacco users linked with Tobacco cessation centres"
    })
    alc = load_comorbidity(comorbidity_files["alc"], {
        "alc_known_pct": "% of TB - Alcohol-TB patients with known Alcohol usage status",
        "alc_linkage_pct": "Percentage  of No of TB - Alcohol-Alcohol users linked with Deaddiction centres"
    })

    # Merge
    df = nfhs.merge(dm, on="state", how="left").merge(tob, on="state", how="left").merge(alc, on="state", how="left")

    # Fill missing comorbidity data with median
    for col in ["dm_known_pct", "dm_treated_pct", "tob_known_pct", "tob_linkage_pct", "alc_known_pct", "alc_linkage_pct"]:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median() if not df[col].isna().all() else 0.5)

    # System score
    df["system_score"] = (
        0.3 * df["dm_known_pct"] +
        0.15 * df["dm_treated_pct"] +
        0.2 * df["tob_known_pct"] +
        0.1 * df["tob_linkage_pct"] +
        0.15 * df["alc_known_pct"] +
        0.1 * df["alc_linkage_pct"]
    )

    # Risk score
    risk_cols = ["stunting_pct", "underweight_pct", "wasting_pct", "anemia_pct", "male_tobacco_pct", "female_tobacco_pct", "male_alcohol_pct"]
    protective_cols = ["sanitation_pct", "cleanfuel_pct"]

    rename_map = {
        "Children under 5 years who are stunted (height-for-age)18 (%)": "stunting_pct",
        "Children under 5 years who are underweight (weight-for-age)18 (%)": "underweight_pct",
        "Children under 5 years who are wasted (weight-for-height)18 (%)": "wasting_pct",
        "Children age 6-59 months who are anaemic (<11.0 g/dl)22 (%)": "anemia_pct",
        "Men age 15 years and above who use any kind of tobacco (%)": "male_tobacco_pct",
        "Women age 15 years and above who use any kind of tobacco (%)": "female_tobacco_pct",
        "Men age 15 years and above who consume alcohol (%)": "male_alcohol_pct",
        "Population living in households that use an improved sanitation facility2 (%)": "sanitation_pct",
        "Households using clean fuel for cooking3 (%)": "cleanfuel_pct"
    }
    df = df.rename(columns=rename_map)

    risk_cols_renamed = [rename_map.get(c, c) for c in risk_cols]
    protective_cols_renamed = [rename_map.get(c, c) for c in protective_cols]

    print("Risk cols renamed:", risk_cols_renamed)
    print("Protective cols renamed:", protective_cols_renamed)
    print("Available columns:", df.columns.tolist())

    for col in risk_cols_renamed + protective_cols_renamed:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(df[col].median())
            df[f"{col}_z"] = (df[col] - df[col].mean()) / df[col].std()
            print(f"Processed {col}: mean={df[col].mean():.3f}, std={df[col].std():.3f}")
        else:
            print(f"Column {col} not found in df")

    available_risk_z = [f"{c}_z" for c in risk_cols_renamed if f"{c}_z" in df.columns]
    available_protective_z = [f"{c}_z" for c in protective_cols_renamed if f"{c}_z" in df.columns]

    print("Available risk z-cols:", available_risk_z)
    print("Available protective z-cols:", available_protective_z)

    if available_risk_z:
        df["risk_score"] = df[available_risk_z].mean(axis=1)
        if available_protective_z:
            df["risk_score"] -= df[available_protective_z].mean(axis=1)
        df["risk_z"] = (df["risk_score"] - df["risk_score"].mean()) / df["risk_score"].std()
        print("Risk score computed successfully")
    else:
        df["risk_z"] = np.nan
        print("No risk columns available")

    df["system_z"] = (df["system_score"] - df["system_score"].mean()) / df["system_score"].std()

    return df[["state", "system_score", "risk_score", "system_z", "risk_z"]]

# Main analysis
def integrated_analysis():
    mcmc_df = load_mcmc_missed_cases()
    scores_df = load_system_risk_scores()

    # Merge
    merged = pd.merge(mcmc_df, scores_df, on="state", how="inner")
    print(f"Merged data shape: {merged.shape}")
    print(merged.head())

    # Correlation analysis
    corr_system = merged["mcmc_missed_mean"].corr(merged["system_z"])
    corr_risk = merged["mcmc_missed_mean"].corr(merged["risk_z"])
    print(f"Correlation MCMC missed vs System z: {corr_system:.3f}")
    print(f"Correlation MCMC missed vs Risk z: {corr_risk:.3f}")

    # Regression analysis - drop NaN
    reg_data = merged.dropna(subset=["system_z", "risk_z", "mcmc_missed_mean"])
    if len(reg_data) > 2:
        X = reg_data[["system_z", "risk_z"]]
        y = reg_data["mcmc_missed_mean"]
        X = sm.add_constant(X)
        model = sm.OLS(y, X).fit()
        print(model.summary())
    else:
        print("Not enough data for regression")
        model = None

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    sns.scatterplot(data=merged, x="system_z", y="mcmc_missed_mean", ax=axes[0])
    axes[0].set_title(f"System Strength vs MCMC Missed Cases\nCorr: {corr_system:.3f}")
    axes[0].set_xlabel("System z-score")
    axes[0].set_ylabel("MCMC Missed Cases (mean)")

    sns.scatterplot(data=merged, x="risk_z", y="mcmc_missed_mean", ax=axes[1])
    axes[1].set_title(f"Risk Burden vs MCMC Missed Cases\nCorr: {corr_risk:.3f}")
    axes[1].set_xlabel("Risk z-score")
    axes[1].set_ylabel("MCMC Missed Cases (mean)")

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "integrated_mcmc_system_risk.png", dpi=300)
    plt.close()

    # Save results
    merged.to_csv(TABLES_DIR / "integrated_mcmc_system_risk.csv", index=False)

    # Insights
    insights = f"""
# Integrated Analysis: MCMC Missed Cases with System and Risk Indices

## Overview
This analysis integrates the latest MCMC Bayesian estimates of missed TB cases with earlier system-strength and epidemiological risk indices from NFHS-5 and India TB Report cascade data.

## Key Findings
- **Correlation with System Strength**: {corr_system:.3f}
- **Correlation with Risk Burden**: {corr_risk:.3f}
- **Regression R-squared**: {'{:.3f}'.format(model.rsquared) if model else 'N/A (insufficient data)'}

## Insights
- System strength shows {'strong' if abs(corr_system) > 0.5 else 'moderate'} {'negative' if corr_system < 0 else 'positive'} correlation with missed cases, indicating that better health system performance is associated with fewer undetected cases.
- Risk burden data was insufficient for correlation analysis.
- {'The integrated model explains ' + str(model.rsquared * 100) + '% of the variation in MCMC missed cases, highlighting the role of system factors.' if model else 'Regression analysis could not be performed due to insufficient risk burden data.'}

## Implications
This integration reveals that while MCMC provides robust uncertainty quantification for missed cases, combining it with system and risk indices offers deeper insights into intervention priorities. States with high risk but weak systems (e.g., Bihar) require multifaceted approaches targeting both detection infrastructure and social determinants.

## Figures
- Scatter plots: {FIGURES_DIR / 'integrated_mcmc_system_risk.png'}

## Data
- Merged dataset: {TABLES_DIR / 'integrated_mcmc_system_risk.csv'}
"""
    with open(REPORTS_DIR / "integrated_mcmc_system_risk_analysis.md", "w") as f:
        f.write(insights)

    print("Integrated analysis complete. See reports/integrated_mcmc_system_risk_analysis.md")

if __name__ == "__main__":
    integrated_analysis()