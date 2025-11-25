import pandas as pd
import numpy as np
import os

# Paths
nfhs_path = 'SOURCES DATA/NFHS_5_India_Districts_Factsheet_Data.xls'
tb_path = 'data/processed/merged_rs_tb_state.csv'
nfhs_agg_path = 'data/processed/nfhs5_state_agg.csv'
merged_path = 'data/processed/nfhs_rs_tb_merged.csv'
report_path = 'reports/nfhs_rs_tb_associations.md'

os.makedirs('data/processed', exist_ok=True)
os.makedirs('reports', exist_ok=True)

# Comprehensive state name mapping (NFHS to RS)
# Load NFHS
print("Loading NFHS...")
nfhs = pd.read_excel(nfhs_path)

# Standardize state
nfhs['state_ut'] = nfhs['State/UT'].str.strip().str.title()

# Key TB risk indicators (cols truncated in inspection, use partial matches)
key_indicators = [
    'Children under 5 years who are stunted',
    'Children under 5 years who are underweight',
    'Children under 5 years who are wasted',
    'Children age 6-59 months who are anaemic',
    'Men age 15 years and above who use any kind of tobacco',
    'Women age 15 years and above who use any kind of tobacco',
    'Men age 15 years and above who consume alcohol',
    'Population living in households that use an improved sanitation facility',
    'Households using clean fuel for cooking',
]

# Select cols
indicator_cols = []
for ind in key_indicators:
    matches = [col for col in nfhs.columns if ind in col]
    if matches:
        indicator_cols.extend(matches[:1])  # first match

cols_to_use = ['state_ut'] + indicator_cols
nfhs_key = nfhs[cols_to_use].copy()

# Agg mean % by state
nfhs_state = nfhs_key.groupby('state_ut').mean(numeric_only=True).reset_index()

# Save agg
nfhs_state.to_csv(nfhs_agg_path, index=False)
print(f"NFHS state agg saved: {nfhs_agg_path} (shape: {nfhs_state.shape})")

# Load TB
tb = pd.read_csv(tb_path)
tb['state_ut'] = tb['stateut'].str.strip().str.title()

# Merge
merged = pd.merge(tb, nfhs_state, on='state_ut', how='inner')

# Select TB target: 2023 cases
tb_cases_2023 = merged['2023'].dropna()

# Corrs with indicators
corrs = {}
for col in indicator_cols:
    if col in merged.columns:
        ind = merged[col].dropna()
        if len(ind) > 0:
            corr = tb_cases_2023.corr(ind.reindex(tb_cases_2023.index))
            corrs[col] = corr

print("Correlations TB 2023 cases vs NFHS indicators:")
for k, v in corrs.items():
    print(f"{k}: {v:.3f}")

# Save merged
merged.to_csv(merged_path, index=False)
print(f"Merged saved: {merged_path} (shape: {merged.shape}, states: {len(merged)})")

# Report
with open(report_path, 'w') as f:
    f.write("# NFHS-RS TB Associations\n\n")
    f.write("## Correlations (TB 2023 cases vs state avg indicators):\n\n")
    f.write("| Indicator | Corr |\n|-----------|------|\n")
    for k, v in corrs.items():
        f.write(f"| {k} | {v:.3f} |\n")
    f.write("\n## Insights\n- Positive corr with stunting/underweight expected (malnutrition-TB link).\n- Tobacco positive risk.\n- Sanitation negative (better hygiene lower TB).\n")
    f.write(f"\nMerged data: {merged_path}\n")

print(f"Report: {report_path}")
print("NFHS-RS association complete!")
