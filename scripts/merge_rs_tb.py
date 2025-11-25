import pandas as pd
import os
from pathlib import Path

processed_dir = 'data/processed'
merged_path = os.path.join(processed_dir, 'merged_rs_tb_state.csv')
os.makedirs(processed_dir, exist_ok=True)

print("Merging state-level RS TB data...")

state_files = [
    'rs_RS_Session_260_AU_618_A_to_B_i_clean.csv',  # cases 2020-23
    'rs_RS_Session_266_AU_1736_A_to_C_3 (1)_clean.csv',  # % cases age 23/24
    'rs_RS_Session_266_AU_1736_A_to_C_4_clean.csv',  # % deaths age 23/24
    'rs_RS_Session_266_AU_2511_1_clean.csv',  # cases/deaths 24 Jan-Oct
    'rs_RS_Session_267_AU_3467_1_clean.csv',  # notified/treated 23/24
]

dfs = {}
for f in state_files:
    fpath = os.path.join(processed_dir, f)
    if os.path.exists(fpath):
        df = pd.read_csv(fpath)
        state_col = next((c for c in df.columns if 'state' in c.lower()), df.columns[0])
        df['source_file'] = f
        dfs[f] = df
        print(f"Loaded {f} (shape: {df.shape}, states: {len(df[state_col].unique())})")
    else:
        print(f"Missing {f}")

# Simple merge on state (assume consistent state names)
if dfs:
    merged = dfs[list(dfs.keys())[0]].copy()
    for name, df in list(dfs.items())[1:]:
        merged = merged.merge(df, on=state_col, how='outer', suffixes=('', f'_{name}'))
    
    # Drop duplicates/NaNs if any
    merged = merged.drop_duplicates(subset=[state_col]).fillna(0)
    
    merged.to_csv(merged_path, index=False)
    print(f"\nMerged state data saved: {merged_path} (shape: {merged.shape})")
    print("Columns:", list(merged.columns))
    print("\nSample:")
    print(merged.head().to_string())
else:
    print("No state files found.")

print("Merge complete.")
