import pandas as pd
import numpy as np

# ── 1. Load ───────────────────────────────────────────────────────────────────
raw_path = r"C:\Users\user\Desktop\Projects\P1_Lag_analysis\Food_Security_Data\Food_Security_Data_E_Africa.csv"

df = pd.read_csv(raw_path, encoding="latin-1")

# ── 2. Filter items we need ───────────────────────────────────────────────────
items_needed = [
    "Prevalence of undernourishment (percent) (3-year average)",
    "Prevalence of severe food insecurity in the total population (percent) (3-year average)",
    "Prevalence of moderate or severe food insecurity in the total population (percent) (3-year average)"
]

df = df[df["Item"].isin(items_needed)].copy()

# Keep only Value element rows, drop confidence intervals
df = df[df["Element"] == "Value"].copy()

print("Filtered shape:", df.shape)

# ── 3. Keep only 3-year average year columns ──────────────────────────────────
# These columns look like Y20002002, Y20012003 etc. (8 digits, no F or N suffix)
import re

id_cols = ["Area Code", "Area", "Item", "Unit"]

year_cols = [
    col for col in df.columns
    if re.match(r'^Y\d{8}$', col)
]

print("Number of 3-year average year columns found:", len(year_cols))
print("Sample year columns:", year_cols[:5])

df = df[id_cols + year_cols].copy()

# ── 4. Melt to long format ────────────────────────────────────────────────────
df_long = df.melt(
    id_vars=id_cols,
    value_vars=year_cols,
    var_name="year_raw",
    value_name="value"
)

# Extract the end year from column name e.g. Y20002002 -> 2002
df_long["year"] = df_long["year_raw"].str[5:9].astype(int)
df_long = df_long.drop(columns=["year_raw"])

# ── 5. Handle "<2.5" and other non-numeric values ─────────────────────────────
df_long["value"] = df_long["value"].replace("<2.5", "2.5")
df_long["value"] = pd.to_numeric(df_long["value"], errors="coerce")

# Drop rows with no value
df_long = df_long.dropna(subset=["value"])

# ── 6. Pivot so each indicator is its own column ──────────────────────────────
df_pivot = df_long.pivot_table(
    index=["Area Code", "Area", "year"],
    columns="Item",
    values="value"
).reset_index()

# Flatten column names
df_pivot.columns.name = None
df_pivot = df_pivot.rename(columns={
    "Prevalence of undernourishment (percent) (3-year average)": "pou_pct",
    "Prevalence of severe food insecurity in the total population (percent) (3-year average)": "severe_insecurity_pct",
    "Prevalence of moderate or severe food insecurity in the total population (percent) (3-year average)": "mod_severe_insecurity_pct"
})

# ── 7. Save clean output ──────────────────────────────────────────────────────
output_path = r"C:\Users\user\Desktop\Projects\P1_Lag_analysis\Food_Security_Data\faostat_clean.csv"
df_pivot.to_csv(output_path, index=False)

print("\nFinal shape:", df_pivot.shape)
print("\nSample output:")
print(df_pivot.head(10).to_string())
print("\nCountries in dataset:", df_pivot["Area"].nunique())
print("Year range:", df_pivot["year"].min(), "to", df_pivot["year"].max())
print("\nDone. Saved to faostat_clean.csv")