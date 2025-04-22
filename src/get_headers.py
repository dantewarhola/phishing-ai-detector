import os
import pandas as pd
from pathlib import Path
import pprint

# Python_REPL.py
# Quick script to summarize row counts and column names of all CSVs in data/raw

# 1) Define the data/raw directory relative to this script
base_dir = Path(__file__).parent / "data" / "raw"

# 2) List files to confirm path
print("Files in data/raw:", os.listdir(base_dir))

metadata = []
for f in os.listdir(base_dir):
    path = base_dir / f
    print(f"\nLoading {path} …")
    try:
        df = pd.read_csv(path)
    except Exception as e:
        print(f"Error reading {path}: {e}")
        continue
    metadata.append({
        "file": f,
        "rows": df.shape[0],
        "columns": list(df.columns)
    })

# 3) Print a concise summary
print("\nSummary of datasets:")
pprint.pprint(metadata)
