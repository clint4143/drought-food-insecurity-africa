import pandas as pd
import numpy as np

# ── 1. Load ───────────────────────────────────────────────────────────────────
raw_path = r"C:\Users\user\Desktop\Projects\P1_Lag_analysis\Food_Security_Data\emdat_drought_africa_raw.csv"

df = pd.read_csv(raw_path, encoding="utf-8-sig")

print("Raw shape:", df.shape)
print("\nColumns:", df.columns.tolist())

# ── 2. Keep only columns we need ──────────────────────────────────────────────
cols_needed = [
    "DisNo.", "Country", "ISO", "Subregion",
    "Start Year", "Start Month",
    "End Year", "End Month",
    "Total Affected"
]

df = df[cols_needed].copy()

# ── 3. Filter to 2000-2023 only ───────────────────────────────────────────────
df = df[df["Start Year"] >= 2000].copy()
df = df[df["Start Year"] <= 2023].copy()

# ── 4. Rename columns to clean names ─────────────────────────────────────────
df = df.rename(columns={
    "DisNo.": "disaster_id",
    "Country": "country",
    "ISO": "iso3",
    "Subregion": "subregion",
    "Start Year": "start_year",
    "Start Month": "start_month",
    "End Year": "end_year",
    "End Month": "end_month",
    "Total Affected": "total_affected"
})

# ── 5. Create a drought flag per country per year ─────────────────────────────
# A country has a drought year if a drought event starts in that year
drought_years = df.groupby(["country", "iso3", "subregion", "start_year"]).agg(
    drought_events=("disaster_id", "count"),
    total_affected=("total_affected", "sum")
).reset_index()

drought_years = drought_years.rename(columns={"start_year": "year"})
drought_years["drought_occurred"] = 1

# ── 6. Save ───────────────────────────────────────────────────────────────────
output_path = r"C:\Users\user\Desktop\Projects\P1_Lag_analysis\Food_Security_Data\emdat_clean.csv"
drought_years.to_csv(output_path, index=False)

print("\nCleaned shape:", drought_years.shape)
print("\nSample output:")
print(drought_years.head(10).to_string())
print("\nCountries with drought events:", drought_years["country"].nunique())
print("Year range:", drought_years["year"].min(), "to", drought_years["year"].max())
print("\nSubregions found:", drought_years["subregion"].unique())
print("\nDone. Saved to emdat_clean.csv")