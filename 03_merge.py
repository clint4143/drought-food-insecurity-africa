import pandas as pd
import numpy as np

# ── 1. Load both clean datasets ───────────────────────────────────────────────
faostat = pd.read_csv(r"C:\Users\user\Desktop\Projects\P1_Lag_analysis\Food_Security_Data\faostat_clean.csv")
emdat = pd.read_csv(r"C:\Users\user\Desktop\Projects\P1_Lag_analysis\Food_Security_Data\emdat_clean.csv")

# Strip whitespace and fix encoding artifacts in country names
faostat["Area"] = faostat["Area"].str.strip()

print("FAOSTAT shape:", faostat.shape)
print("EM-DAT shape:", emdat.shape)

# ── 2. Complete African country name to ISO3 + AU subregion mapping ───────────
country_map = {
    # North Africa
    "Algeria":{"iso3":"DZA","subregion":"North Africa"},
    "Egypt":{"iso3":"EGY","subregion":"North Africa"},
    "Libya":{"iso3":"LBY","subregion":"North Africa"},
    "Morocco":{"iso3":"MAR","subregion":"North Africa"},
    "Sudan":{"iso3":"SDN","subregion":"North Africa"},
    "Tunisia":{"iso3":"TUN","subregion":"North Africa"},
    "Western Sahara":{"iso3":"ESH","subregion":"North Africa"},
    # East Africa
    "Burundi":{"iso3":"BDI","subregion":"East Africa"},
    "Comoros":{"iso3":"COM","subregion":"East Africa"},
    "Djibouti":{"iso3":"DJI","subregion":"East Africa"},
    "Eritrea":{"iso3":"ERI","subregion":"East Africa"},
    "Ethiopia":{"iso3":"ETH","subregion":"East Africa"},
    "Kenya":{"iso3":"KEN","subregion":"East Africa"},
    "Madagascar":{"iso3":"MDG","subregion":"East Africa"},
    "Malawi":{"iso3":"MWI","subregion":"East Africa"},
    "Mauritius":{"iso3":"MUS","subregion":"East Africa"},
    "Mozambique":{"iso3":"MOZ","subregion":"East Africa"},
    "Rwanda":{"iso3":"RWA","subregion":"East Africa"},
    "Seychelles":{"iso3":"SYC","subregion":"East Africa"},
    "Somalia":{"iso3":"SOM","subregion":"East Africa"},
    "South Sudan":{"iso3":"SSD","subregion":"East Africa"},
    "Uganda":{"iso3":"UGA","subregion":"East Africa"},
    "United Republic of Tanzania":{"iso3":"TZA","subregion":"East Africa"},
    "Zambia":{"iso3":"ZMB","subregion":"East Africa"},
    "Zimbabwe":{"iso3":"ZWE","subregion":"East Africa"},
    # West Africa
    "Benin":{"iso3":"BEN","subregion":"West Africa"},
    "Burkina Faso":{"iso3":"BFA","subregion":"West Africa"},
    "Cabo Verde":{"iso3":"CPV","subregion":"West Africa"},
    "Cote d'Ivoire":{"iso3":"CIV","subregion":"West Africa"},
    "CÃ´te d'Ivoire":{"iso3":"CIV","subregion":"West Africa"},
    "C\u00f4te d'Ivoire":{"iso3":"CIV","subregion":"West Africa"},
    "Gambia":{"iso3":"GMB","subregion":"West Africa"},
    "Ghana":{"iso3":"GHA","subregion":"West Africa"},
    "Guinea":{"iso3":"GIN","subregion":"West Africa"},
    "Guinea-Bissau":{"iso3":"GNB","subregion":"West Africa"},
    "Liberia":{"iso3":"LBR","subregion":"West Africa"},
    "Mali":{"iso3":"MLI","subregion":"West Africa"},
    "Mauritania":{"iso3":"MRT","subregion":"West Africa"},
    "Niger":{"iso3":"NER","subregion":"West Africa"},
    "Nigeria":{"iso3":"NGA","subregion":"West Africa"},
    "Senegal":{"iso3":"SEN","subregion":"West Africa"},
    "Sierra Leone":{"iso3":"SLE","subregion":"West Africa"},
    "Togo":{"iso3":"TGO","subregion":"West Africa"},
    # Central Africa
    "Angola":{"iso3":"AGO","subregion":"Central Africa"},
    "Cameroon":{"iso3":"CMR","subregion":"Central Africa"},
    "Central African Republic":{"iso3":"CAF","subregion":"Central Africa"},
    "Chad":{"iso3":"TCD","subregion":"Central Africa"},
    "Congo":{"iso3":"COG","subregion":"Central Africa"},
    "Democratic Republic of the Congo":{"iso3":"COD","subregion":"Central Africa"},
    "Equatorial Guinea":{"iso3":"GNQ","subregion":"Central Africa"},
    "Gabon":{"iso3":"GAB","subregion":"Central Africa"},
    "Sao Tome and Principe":{"iso3":"STP","subregion":"Central Africa"},
    # Southern Africa
    "Botswana":{"iso3":"BWA","subregion":"Southern Africa"},
    "Eswatini":{"iso3":"SWZ","subregion":"Southern Africa"},
    "Lesotho":{"iso3":"LSO","subregion":"Southern Africa"},
    "Namibia":{"iso3":"NAM","subregion":"Southern Africa"},
    "South Africa":{"iso3":"ZAF","subregion":"Southern Africa"},
}

# ── 3. Apply mapping to FAOSTAT ───────────────────────────────────────────────
faostat["iso3"] = faostat["Area"].map(
    lambda x: country_map.get(x, {}).get("iso3", np.nan)
)
faostat["subregion"] = faostat["Area"].map(
    lambda x: country_map.get(x, {}).get("subregion", np.nan)
)

print("\nFAOSTAT countries without subregion match:")
unmatched = faostat[faostat["subregion"].isna()]["Area"].unique()
print(unmatched)

# ── 4. Merge FAOSTAT + EM-DAT on iso3 + year ─────────────────────────────────
merged = faostat.merge(
    emdat[["iso3","year","drought_events","total_affected","drought_occurred"]],
    on=["iso3","year"],
    how="left"
)

merged["drought_occurred"] = merged["drought_occurred"].fillna(0).astype(int)
merged["drought_events"] = merged["drought_events"].fillna(0).astype(int)
merged["total_affected"] = merged["total_affected"].fillna(0)

# ── 5. Keep only rows with pou_pct and subregion ──────────────────────────────
merged = merged.dropna(subset=["pou_pct", "subregion"])

# ── 6. Save ───────────────────────────────────────────────────────────────────
output_path = r"C:\Users\user\Desktop\Projects\P1_Lag_analysis\Food_Security_Data\merged_clean.csv"
merged.to_csv(output_path, index=False)

print("\nMerged shape:", merged.shape)
print("\nSub-region distribution:")
print(merged.drop_duplicates(subset=["Area"])["subregion"].value_counts())
print("\nDrought years vs non-drought years:")
print(merged["drought_occurred"].value_counts())
print("\nCountries in final dataset:", merged["Area"].nunique())
print("\nSample output:")
print(merged[["Area","year","subregion","pou_pct","drought_occurred",
              "total_affected"]].head(15).to_string())
print("\nDone. Saved to merged_clean.csv")