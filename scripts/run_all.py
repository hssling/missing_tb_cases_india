#!/usr/bin/env python3
"""
Master runner script for TB determinants analysis.
Executes all scripts in sequence.
"""

import subprocess
import sys
import time

scripts = [
    'scripts/01_ingest_and_clean.py',
    'scripts/02_merge_and_derive.py',
    'scripts/03_analysis_models.py',
    'scripts/04_spatial_analysis.py',
    'scripts/05_generate_outputs.py'
]

print("Starting full TB determinants analysis pipeline...")

total_start = time.time()
for i, script in enumerate(scripts, 1):
    print(f"\n--- Step {i}/{len(scripts)}: Running {script} ---")
    start_time = time.time()
    try:
        result = subprocess.run([sys.executable, script], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Completed {script}")
        else:
            print(f"✗ Error in {script}: {result.stderr}")
            sys.exit(1)
    except Exception as e:
        print(f"✗ Failed to run {script}: {e}")
        sys.exit(1)
    elapsed = time.time() - start_time
    print(".2f")

total_elapsed = time.time() - total_start
print(".2f")
print("All steps completed successfully!")
print("Check output/ and reports/ directories for results.")
