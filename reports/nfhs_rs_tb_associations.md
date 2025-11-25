# TB Notification Data Processing and NFHS Associations Analysis

## Executive Summary
Processed 6 new Rajya Sabha (RS) session CSV files from SOURCES DATA/ containing state/UT-level TB notifications, cases, deaths, age distributions (2020-2024), and treatment success. Data cleaned, merged into consolidated state dataset. Aggregated NFHS-5 district factsheet (707 districts) to state-level risk factors (malnutrition, tobacco, sanitation). Computed Pearson correlations between 2023 TB cases and NFHS indicators across 31 matching states (r=0.077 to 0.447). Key: Positive with child malnutrition; negative with sanitation/clean fuel.

**Files produced:**
- Individual cleaned: data/processed/rs_*_clean.csv (6 files)
- RS merged: data/processed/merged_rs_tb_state.csv (36 states x 35 cols)
- NFHS state agg: data/processed/nfhs5_state_agg.csv (36 states x 10 indicators)
- Full merged: data/processed/nfhs_rs_tb_merged.csv (31 states x 45 cols)
- This report.

## Methods

### 1. New CSV Identification & Inspection
- Listed SOURCES DATA/: 6 RS_Session_*.csv (36 states each except 1 national).
- Inspection script (`scripts/inspect_rs_csvs.py`): Pandas read_csv, shape/cols/head/dtypes/describe stats.

### 2. RS Data Extraction & Cleaning (`scripts/extract_rs_tb.py`)
- Glob SOURCES DATA/RS_*.csv
- standardize_columns: lower, replace spaces/parens/% with _, strip.
- apply_name_mapping: title case, common variants (e.g., bangalore→Bengaluru).
- Drop 'sl_no' col.
- Save individual: data/processed/rs_[filename]_clean.csv

### 3. RS Data Merging (`scripts/merge_rs_tb.py`)
- Load 5 state-level cleaned files.
- Outer merge on state col (first matching 'state').
- Fill NaN=0, drop dups.
- Save: data/processed/merged_rs_tb_state.csv (36x35: cases 2020-24, %age cases/deaths, notified/treated).

### 4. NFHS-5 Processing (`scripts/process_nfhs_rs_merge.py`)
- pd.read_excel('SOURCES DATA/NFHS_5_India_Districts_Factsheet_Data.xls') → 707 districts x 109 cols.
- Standardize 'State/UT' → 'state_ut' (title/strip).
- Key TB-risk indicators (partial match):
  - Child malnutrition: stunted (height-age), underweight (weight-age), wasted (weight-height).
  - Anaemia: children 6-59m (<11g/dl).
  - Tobacco: men/women any kind.
  - Alcohol: men.
  - Sanitation: improved facility %.
  - Clean fuel cooking %.
- Agg: groupby 'state_ut', mean(numeric_only=True) → nfhs5_state_agg.csv (36x10).

### 5. Merge & Analysis
- TB 'stateut' → title 'state_ut'.
- pd.merge(inner) on 'state_ut' → 31 states match.
- Pearson corr: TB '2023' cases vs each NFHS indicator (pandas.corr).

### Scripts & Tools Used
- Pandas for all data ops.
- Installed xlrd for XLS.
- All in ACT MODE, step-by-step tool confirmation.

## Results

### Correlations Table (TB 2023 Cases vs NFHS State Avg %)
| Indicator | Correlation (r) |
|-----------|-----------------|
| Children under 5 stunted (height-for-age) | **0.432** |
| Children under 5 underweight (weight-for-age) | **0.447** |
| Children under 5 wasted (weight-for-height) | 0.298 |
| Children 6-59m anaemic (<11.0 g/dl) | 0.331 |
| Men ≥15y tobacco use | 0.077 |
| Women ≥15y tobacco use | -0.198 |
| Men ≥15y alcohol use | -0.385 |
| Improved sanitation households | -0.332 |
| Clean fuel cooking households | -0.208 |

### Key Insights
- **Strongest positive**: Child underweight (r=0.447), stunting (0.432) – malnutrition vulnerability aligns with TB susceptibility (compromised immunity).
- **Anaemia moderate positive** (0.331): Iron deficiency exacerbates TB risk.
- **Tobacco weak**: Men low positive; women inverse (possibly lower prevalence states have higher TB?).
- **Protective factors negative**: Sanitation (-0.332), clean fuel (-0.208) – better WASH/socioecon reduces transmission.
- Alcohol inverse: Possibly collinear with development.

**Data Coverage**: 31/36 states matched (UT mismatches e.g., Ladakh). National RS file not merged.

## Limitations & Next Steps
- State-level agg loses district granularity.
- NFHS-5 (2019-21); RS up to 2024 – temporal mismatch.
- Simple Pearson (linear); consider regression/models (scripts/03_analysis_models.py).
- Visualize: Add matplotlib scatters/top states tables.
- Integrate census/pop for rates (per 100k).

Run `python scripts/process_nfhs_rs_merge.py` to regenerate.

**Date**: 2025-11-23
