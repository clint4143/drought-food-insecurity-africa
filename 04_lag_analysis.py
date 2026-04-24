import pandas as pd
import numpy as np

# ── 1. Load merged data ───────────────────────────────────────────────────────
df = pd.read_csv(r"C:\Users\user\Desktop\Projects\P1_Lag_analysis\Food_Security_Data\merged_clean.csv")

df = df.sort_values(["Area", "year"]).reset_index(drop=True)

# ── 2. Create lagged PoU columns ──────────────────────────────────────────────
# For each country, shift pou_pct forward by 1, 2, 3 years after drought
for lag in [1, 2, 3]:
    df[f"pou_lag_{lag}"] = df.groupby("Area")["pou_pct"].shift(-lag)

# ── 3. Change in PoU after drought ────────────────────────────────────────────
for lag in [1, 2, 3]:
    df[f"pou_change_{lag}yr"] = df[f"pou_lag_{lag}"] - df["pou_pct"]

# ── 4. Isolate drought-year rows only ─────────────────────────────────────────
drought_df = df[df["drought_occurred"] == 1].copy()

print("Drought events with valid lag data:")
for lag in [1, 2, 3]:
    valid = drought_df[f"pou_change_{lag}yr"].notna().sum()
    print(f"  Lag {lag} year: {valid} events")

# ── 5. Mean PoU change by lag and sub-region ──────────────────────────────────
print("\n--- Mean PoU change after drought by sub-region ---")
for lag in [1, 2, 3]:
    print(f"\nLag {lag} year:")
    result = drought_df.groupby("subregion")[f"pou_change_{lag}yr"].mean().round(2)
    print(result.to_string())

# ── 6. Overall mean PoU change by lag ─────────────────────────────────────────
print("\n--- Overall mean PoU change after drought (all Africa) ---")
for lag in [1, 2, 3]:
    mean_val = drought_df[f"pou_change_{lag}yr"].mean()
    print(f"  Lag {lag} year: {mean_val:.3f} percentage points")

# ── 7. Save analysis output ───────────────────────────────────────────────────
output_cols = [
    "Area", "iso3", "subregion", "year",
    "pou_pct", "drought_occurred", "total_affected",
    "pou_lag_1", "pou_lag_2", "pou_lag_3",
    "pou_change_1yr", "pou_change_2yr", "pou_change_3yr"
]

df[output_cols].to_csv(
    r"C:\Users\user\Desktop\Projects\P1_Lag_analysis\Food_Security_Data\lag_analysis.csv",
    index=False
)

drought_df[output_cols].dropna(subset=["pou_change_1yr"]).to_csv(
    r"C:\Users\user\Desktop\Projects\P1_Lag_analysis\Food_Security_Data\drought_events_only.csv",
    index=False
)

print("\nDone. Saved lag_analysis.csv and drought_events_only.csv")