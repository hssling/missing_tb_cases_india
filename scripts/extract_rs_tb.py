import pandas as pd
import os
import glob
import re
from pathlib import Path

# Paths
raw_dir = 'SOURCES DATA'
processed_dir = 'data/processed'
os.makedirs(processed_dir, exist_ok=True)

# Name mapping from existing pipeline
name_mapping = {
    'bangalore': 'Bengaluru',
    'calcutta': 'Kolkata',
    'bombay': 'Mumbai',
    'madras': 'Chennai',
    # Add India-specific if needed
    'andaman and nicobar islands': 'Andaman and Nicobar Islands',
}

def apply_name_mapping(series):
    series = series.str.strip().str.title()
    for old, new in name_mapping.items():
        series = series.str.replace(old.title(), new, case=False)
    return series

def standardize_columns(df):
    df.columns = (df.columns.str.lower()
                  .str.replace(r'\s+', '_', regex=True)
                  .str.replace(r'[\(\)%\*]', '', regex=True)
                  .str.replace(r'[^\w\s]', '', regex=True)
                  .str.strip())
    return df

print("Extracting and cleaning RS TB data...")

# List all RS CSVs
csv_files = sorted(glob.glob(os.path.join(raw_dir, 'RS_Session_*.csv')))
extracted_files = []

for file_path in csv_files:
    filename = Path(file_path).stem
    print(f"\nProcessing {filename}...")
    
    df = pd.read_csv(file_path)
    df = standardize_columns(df)
    
    # Standardize state column (assume common names: 'state_ut', 'state/ut')
    state_col = next((col for col in df.columns if 'state' in col.lower()), None)
    if state_col:
        df[state_col] = apply_name_mapping(df[state_col])
    
    # Drop sl_no if present
    sl_col = next((col for col in df.columns if 'sl' in col.lower()), None)
    if sl_col:
        df = df.drop(columns=[sl_col])
    
    # Save cleaned individual file
    clean_path = os.path.join(processed_dir, f'rs_{filename}_clean.csv')
    df.to_csv(clean_path, index=False)
    extracted_files.append(clean_path)
    print(f"Saved: {clean_path} (shape: {df.shape})")

# Additional: Consolidate cases by year where possible
cases_files = [f for f in extracted_files if '260' in f or '2511' in f or '267' in f]
print("\nConsolidated cases data saved separately.")

print("Extraction complete. Files in data/processed/:")
for f in extracted_files:
    print(f"  - {Path(f).name}")
