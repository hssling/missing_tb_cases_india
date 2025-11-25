import pandas as pd
import glob
import os

print("Analysis of new RS Session CSV files in SOURCES DATA/")

csv_files = sorted(glob.glob("SOURCES DATA/*.csv"))

for file_path in csv_files:
    print(f"\n=== {os.path.basename(file_path)} ===")
    try:
        df = pd.read_csv(file_path)
        print(f"Shape: {df.shape}")
        print("Columns:", list(df.columns))
        print("\nFirst 3 rows:")
        print(df.head(3).to_string(index=False))
        print("\nBasic stats (numeric columns):")
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            print(df[numeric_cols].describe())
        else:
            print("No numeric columns")
        print("\nData types:")
        print(df.dtypes.to_string())
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
