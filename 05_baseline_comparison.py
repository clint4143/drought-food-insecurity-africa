import pandas as pd
import numpy as np

# ── 1. Load ───────────────────────────────────────────────────────────────────
df = pd.read_csv(r"C:\Users\user\Desktop\Projects\P1_Lag_analysis\Food_Security_Data\lag_analysis.csv")

# ── 2. Mean PoU change in DROUGHT years vs NON-DROUGHT years ─────────────────
print("="*60)
print("CORE FINDING: PoU change after drought vs no drought")
print("="*60)

for lag in [1, 2, 3]:
    col = f"pou_change_{lag}yr"
    drought = df[df["drought_occurred"]==1][col].mean()
    no_drought = df[df["drought_occurred"]==0][col].mean()
    diff = drought - no_drought
    print(f"\nLag {lag} year:")
    print(f"  Drought years avg PoU change:     {drought:+.3f} pp")
    print(f"  Non-drought years avg PoU change: {no_drought:+.3f} pp")
    print(f"  Difference (drought penalty):     {diff:+.3f} pp")

# ── 3. By sub-region ──────────────────────────────────────────────────────────
print("\n" + "="*60)
print("DROUGHT PENALTY BY SUB-REGION (Lag 2 year)")
print("="*60)

results = []
for region in df["subregion"].dropna().unique():
    rdf = df[df["subregion"]==region]
    drought_mean = rdf[rdf["drought_occurred"]==1]["pou_change_2yr"].mean()
    nodrt_mean = rdf[rdf["drought_occurred"]==0]["pou_change_2yr"].mean()
    penalty = drought_mean - nodrt_mean
    n_events = rdf[rdf["drought_occurred"]==1]["pou_change_2yr"].notna().sum()
    results.append({
        "subregion": region,
        "drought_pou_change": round(drought_mean, 3),
        "baseline_pou_change": round(nodrt_mean, 3),
        "drought_penalty_pp": round(penalty, 3),
        "n_drought_events": n_events
    })

results_df = pd.DataFrame(results).sort_values("drought_penalty_pp", ascending=False)
print(results_df.to_string(index=False))

# ── 4. Save for Tableau ───────────────────────────────────────────────────────
tableau_path = r"C:\Users\user\Desktop\Projects\P1_Lag_analysis\Food_Security_Data\tableau_ready.csv"
df[df["year"] <= 2023].to_csv(tableau_path, index=False)

summary_path = r"C:\Users\user\Desktop\Projects\P1_Lag_analysis\Food_Security_Data\subregion_drought_penalty.csv"
results_df.to_csv(summary_path, index=False)

print("\nDone. Saved tableau_ready.csv and subregion_drought_penalty.csv")