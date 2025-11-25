import pandas as pd
import os
import numpy as np
from pathlib import Path

# Paths
processed_dir = 'data/processed'
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

# Load cleaned datasets
tb_df = pd.read_csv(Path(processed_dir) / 'tb_district_clean.csv')
nfhs_df = pd.read_csv(Path(processed_dir) / 'nfhs5_district_clean.csv')
census_df = pd.read_csv(Path(processed_dir) / 'census2011_district_clean.csv')

print("Loaded datasets:")
print(f"TB: {tb_df.shape[0]} rows, {tb_df.shape[1]} cols")
print(f"NFHS: {nfhs_df.shape[0]} rows, {nfhs_df.shape[1]} cols")
print(f"Census: {census_df.shape[0]} rows, {census_df.shape[1]} cols")

# Assume TB data has year; filter to latest year or specific year (e.g., 2020-2021)
# User can adjust this; here assuming we take the most recent year available
if 'year' in tb_df.columns:
    latest_year = tb_df['year'].max()
    tb_df = tb_df[tb_df['year'] == latest_year]
    print(f"Filtered TB data to year {latest_year}: {tb_df.shape[0]} districts")

# Get unique districts before merge
tb_districts = set(zip(tb_df['state'], tb_df['district']))
nfhs_districts = set(zip(nfhs_df['state'], nfhs_df['district']))
census_districts = set(zip(census_df['state'], census_df['district']))

print(f"\nUnique (state, district) pairs before merge:")
print(f"TB: {len(tb_districts)}")
print(f"NFHS: {len(nfhs_districts)}")
print(f"Census: {len(census_districts)}")

# Merge step 1: Merge TB with Census (for population)
merged = pd.merge(tb_df, census_df, on=['state', 'district'], how='inner', suffixes=('', '_census'))
print(f"After merging TB and Census: {merged.shape[0]} districts")

# Merge with NFHS
final_df = pd.merge(merged, nfhs_df, on=['state', 'district'], how='inner', suffixes=('', '_nfhs'))
print(f"After final merge (TB + Census + NFHS): {final_df.shape[0]} districts")

# Log unmatched districts
log_path = Path(output_dir) / 'merge_log.txt'
with open(log_path, 'w') as f:
    f.write("Merge Log\n")
    f.write(f"Final merged districts: {final_df.shape[0]}\n\n")
    
    # Unmatched from TB
    unmatched_tb = tb_districts - set(zip(final_df['state'], final_df['district']))
    if unmatched_tb:
        f.write("Districts in TB but not in final merge:\n")
        for state, dist in sorted(unmatched_tb):
            f.write(f"{state} - {dist}\n")
    else:
        f.write("No unmatched districts from TB.\n")
    
    f.write("\n")
    
    # Unmatched from NFHS
    unmatched_nfhs = nfhs_districts - set(zip(final_df['state'], final_df['district']))
    if unmatched_nfhs:
        f.write("Districts in NFHS but not in final merge:\n")
        for state, dist in sorted(unmatched_nfhs):
            f.write(f"{state} - {dist}\n")
    else:
        f.write("No unmatched districts from NFHS.\n")
    
    f.write("\n")
    
    # Unmatched from Census
    unmatched_census = census_districts - set(zip(final_df['state'], final_df['district']))
    if unmatched_census:
        f.write("Districts in Census but not in final merge:\n")
        for state, dist in sorted(unmatched_census):
            f.write(f"{state} - {dist}\n")
    else:
        f.write("No unmatched districts from Census.\n")

print(f"Merge log saved to {log_path}")

# Derive variables
# Ensure numeric types
final_df['tb_cases_total'] = pd.to_numeric(final_df['tb_cases_total'], errors='coerce')
final_df['population'] = pd.to_numeric(final_df['population'], errors='coerce')

# TB rate per 100,000 population
final_df['tb_rate'] = (final_df['tb_cases_total'] / final_df['population']) * 1e5

# Log population for offset
final_df['log_population'] = np.log(final_df['population'])

# Optional: Create region variable (simple mapping; expand as needed)
north_states = {
    'delhi', 'haryana', 'himachal pradesh', 'jammu and kashmir', 'punjab',
    'rajasthan', 'uttar pradesh', 'uttarakhand'
}
south_states = {
    'andhra pradesh', 'karnataka', 'kerala', 'tamil nadu', 'telangana'
}
east_states = {'bihar', 'jharkhand', 'odisha', 'west bengal'}
west_states = {
    'chhattisgarh', 'goa', 'gujarat', 'madhya pradesh', 'maharashtra'
}
ne_states = {
    'arunachal pradesh', 'assam', 'manipur', 'meghalaya', 'mizoram',
    'nagaland', 'sikkim', 'tripura'
}

regions = {
    'north': north_states,
    'south': south_states,
    'east': east_states,
    'west': west_states,
    'northeast': ne_states
}

def get_region(state):
    state_lower = state.lower()
    for region, states in regions.items():
        if state_lower in states:
            return region
    return 'other'

final_df['region'] = final_df['state'].apply(get_region)

# Select final columns (all for now, but can filter)
# Keep key columns: state, district, tb_cases_total, tb_rate, log_population, population, and all predictors from NFHS/Census

# Save final analysis dataset
final_path = Path(processed_dir) / 'district_tb_determinants.csv'
final_df.to_csv(final_path, index=False)
print(f"\nFinal analysis dataset saved to {final_path}")
print(f"Final dataset shape: {final_df.shape}")
print("Derived variables: tb_rate, log_population, region")
print("Merging and derivation completed successfully.")
print("Note: Adjust year filter for TB data and state-to-region mapping as needed.")
