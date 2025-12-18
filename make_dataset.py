from __future__ import annotations
import os
import pandas as pd
from sklearn.datasets import fetch_california_housing

def main():
    os.makedirs("data", exist_ok=True)

    data = fetch_california_housing(as_frame=True)
    df = data.frame  # includes target column: "MedHouseVal"

    out = "data/housing.csv"
    df.to_csv(out, index=False)
    print(f"✅ Saved: {out} rows={len(df)} cols={len(df.columns)}")

if __name__ == "__main__":
    main()
