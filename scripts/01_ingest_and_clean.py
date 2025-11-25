import pandas as pd
import os
import re

# Paths
raw_dir = 'data/raw'
processed_dir = 'data/processed'
os.makedirs(processed_dir, exist_ok=True)

# Simple mapping dictionary for common district/state name variations
# This is a basic example; may need manual expansion based on actual data discrepancies
name_mapping = {
    'bangalore': 'bengaluru',
    'calcutta': 'kolkata',
    'bombay': 'mumbai',
    'madras': 'chennai',
    # Add more mappings as needed, e.g., 'orissa' -> 'odisha'
}

def apply_name_mapping(series):
    """Apply name mapping to a series."""
    series = series.str.strip().str.title()
    series = series.replace(name_mapping, regex=True)
    return series

def standardize_columns(df):
    """Convert columns to snake_case."""
    df.columns = (df.columns.str.lower()
                  .str.replace(' ', '_')
                  .str.replace(r'\(|\)|%|\*', '', regex=True)
                  .str.replace(r'[^\w\s]', '', regex=True))
    return df

# 1. Read and clean TB data
tb_path = os.path.join(raw_dir, 'tb_district.xlsx')
if not os.path.exists(tb_path):
    tb_path = os.path.join(raw_dir, 'tb_district.csv')
    if not os.path.exists(tb_path):
        raise FileNotFoundError("TB data file not found. Place 'tb_district.csv' or 'tb_district.xlsx' in data/raw/")

if tb_path.endswith('.xlsx'):
    tb_df = pd.read_excel(tb_path)
else:
    tb_df = pd.read_csv(tb_path)

tb_df = standardize_columns(tb_df)

# Ensure/rename key columns (handle possible variations)
column_mapping_tb = {
    'state_name': 'state',
    'district_name': 'district',
    'total_tb_cases': 'tb_cases_total',
    # Add more mappings if needed based on actual column names
}
tb_df = tb_df.rename(columns=column_mapping_tb)

# Ensure required columns exist
required_tb = ['state', 'district', 'year', 'tb_cases_total']
missing_tb = [col for col in required_tb if col not in tb_df.columns]
if missing_tb:
    print(f"Warning: Missing columns in TB data: {missing_tb}. Please check raw file.")

# Clean names
tb_df['state'] = apply_name_mapping(tb_df.get('state', pd.Series()))
tb_df['district'] = apply_name_mapping(tb_df.get('district', pd.Series()))

# Save cleaned TB data
tb_clean_path = os.path.join(processed_dir, 'tb_district_clean.csv')
tb_df.to_csv(tb_clean_path, index=False)
print(f"Cleaned TB data saved to {tb_clean_path}")
print(f"TB data shape: {tb_df.shape}")

# 2. Read and clean NFHS-5 data
nfhs_path = os.path.join(raw_dir, 'nfhs5_district.csv')
if not os.path.exists(nfhs_path):
    raise FileNotFoundError("NFHS-5 data not found. Place 'nfhs5_district.csv' in data/raw/")

nfhs_df = pd.read_csv(nfhs_path)
nfhs_df = standardize_columns(nfhs_df)

# Rename key columns (handle variations)
column_mapping_nfhs = {
    'state': 'state',
    'district': 'district',
    # Example relevant indicators; adjust based on actual names
    'children_0_59_months_stunted': 'stunting_pct',
    'children_0_59_months_wasted': 'wasting_pct',
    'children_0_59_months_underweight': 'underweight_pct',
    'households_with_three_or_more_persons_per_room': 'crowding_pct',
    'men_who_use_tobacco': 'smoking_men_pct',
    'men_who_consume_alcohol': 'alcohol_men_pct',
    'women_with_raised_blood_sugar': 'diabetes_women_pct',
    'men_with_raised_blood_sugar': 'diabetes_men_pct',
    # Add more as needed
}
nfhs_df = nfhs_df.rename(columns=column_mapping_nfhs)

# Select relevant columns (keep all for now, but filter to key ones; user can adjust)
relevant_nfhs_cols = ['state', 'district']
for col in nfhs_df.columns:
    if any(indicator in col for indicator in ['stunt', 'wast', 'underw', 'crowd', 'smok', 'alcohol', 'sugar', 'diabet']):
        relevant_nfhs_cols.append(col)
nfhs_df = nfhs_df[relevant_nfhs_cols]

# Clean names
nfhs_df['state'] = apply_name_mapping(nfhs_df.get('state', pd.Series()))
nfhs_df['district'] = apply_name_mapping(nfhs_df.get('district', pd.Series()))

# Save cleaned NFHS data
nfhs_clean_path = os.path.join(processed_dir, 'nfhs5_district_clean.csv')
nfhs_df.to_csv(nfhs_clean_path, index=False)
print(f"Cleaned NFHS data saved to {nfhs_clean_path}")
print(f"NFHS data shape: {nfhs_df.shape}")

# 3. Read and clean Census 2011 data
census_path = os.path.join(raw_dir, 'census2011_district.csv')
if not os.path.exists(census_path):
    raise FileNotFoundError("Census data not found. Place 'census2011_district.csv' in data/raw/")

census_df = pd.read_csv(census_path)
census_df = standardize_columns(census_df)

# Rename key columns (handle variations)
column_mapping_census = {
    'state': 'state',
    'district': 'district',
    'total_population': 'population',
    'literacy_rate': 'literacy_rate',
    'urban_population_percentage': 'urban_pct',
    'population_density': 'density',
    # Optional: 'sex_ratio': 'sex_ratio',
    # Add more as needed
}
census_df = census_df.rename(columns=column_mapping_census)

# Select relevant columns
relevant_census_cols = ['state', 'district', 'population', 'literacy_rate', 'urban_pct', 'density']
relevant_census_cols = [col for col in relevant_census_cols if col in census_df.columns]
census_df = census_df[relevant_census_cols]

# Ensure population is numeric and positive
census_df['population'] = pd.to_numeric(census_df['population'], errors='coerce')
census_df = census_df[census_df['population'] > 0]

# Clean names
census_df['state'] = apply_name_mapping(census_df.get('state', pd.Series()))
census_df['district'] = apply_name_mapping(census_df.get('district', pd.Series()))

# Save cleaned Census data
census_clean_path = os.path.join(processed_dir, 'census2011_district_clean.csv')
census_df.to_csv(census_clean_path, index=False)
print(f"Cleaned Census data saved to {census_clean_path}")
print(f"Census data shape: {census_df.shape}")

print("Data ingestion and cleaning completed successfully.")
print("Note: Adjust column mappings and name_dictionary in the script if actual data has different names/formats.")
