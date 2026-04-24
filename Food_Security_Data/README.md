## Live Dashboard
[View on Tableau Public](https://public.tableau.com/views/africa_food_security_dashboard/AfricaFoodSecurityDashboard?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

## GitHub Repository
https://github.com/clint4143/drought-food-insecurity-africa

# Drought and Food Insecurity in Africa: A Sub-Regional Lag Analysis (2000-2023)

## Project Overview
This project analyzes the relationship between drought events and food insecurity
across five African sub-regions between 2000 and 2023. The core question is:
how does food insecurity change in the years following a drought shock, and does
this pattern differ by sub-region?

## Key Findings
- West Africa shows the clearest drought penalty: +0.58 percentage points of
  Prevalence of Undernourishment (PoU) at the 2-year lag across 35 drought events
- East Africa's anomalous result (-0.80pp) likely reflects post-drought
  humanitarian response masking acute PoU increases -- itself a finding relevant
  to early warning system design
- FAO's 3-year rolling PoU average structurally limits detection of acute shocks,
  pointing to the need for higher-frequency indicators like FIES in future work

## Data Sources
| Dataset | Source | Link |
|---|---|---|
| Prevalence of Undernourishment (PoU) | FAOSTAT Suite of Food Security Indicators | https://www.fao.org/faostat/en/#data/FS |
| Drought Events | EM-DAT International Disaster Database (CRED) | https://www.emdat.be |

## Methodology
1. Filtered FAOSTAT food security indicators to three PoU measures across 52
   African countries, 2002-2023
2. Extracted 169 drought events from EM-DAT, filtered to Africa, 2000-2023
3. Merged datasets on ISO3 country code and year with AU sub-region mapping
4. Computed lagged PoU changes at 1, 2, and 3-year intervals after drought onset
5. Calculated drought penalty as the difference between mean PoU change in
   drought years vs non-drought years, controlling for background trend

## Limitations
- PoU is a 3-year rolling average -- acute shocks are smoothed and may be
  underdetected
- EM-DAT captures officially reported drought events only -- unreported or
  localized droughts are excluded
- North Africa result (n=1) is not statistically meaningful and should not be
  interpreted as a finding
- No causal inference is made -- this is a descriptive lag analysis

## Project Structure
P1_Lag_analysis/
├── Food_Security_Data/
│   ├── Food_Security_Data_E_Africa.csv   # Raw FAOSTAT data
│   ├── emdat_drought_africa_raw.csv      # Raw EM-DAT data
│   ├── faostat_clean.csv                 # Cleaned FAOSTAT
│   ├── emdat_clean.csv                   # Cleaned EM-DAT
│   ├── merged_clean.csv                  # Merged dataset
│   ├── lag_analysis.csv                  # Lag analysis output
│   ├── tableau_ready.csv                 # Final Tableau input
│   └── subregion_drought_penalty.csv     # Summary for bar chart
├── 01_clean_faostat.py
├── 02_clean_emdat.py
├── 03_merge.py
├── 04_lag_analysis.py
├── 05_baseline_comparison.py
└── README.md

## Tools Used
- Python 3.13 (pandas, numpy)
- Tableau Public
- Data sources: FAOSTAT, EM-DAT/CRED

## Live Dashboard
[View on Tableau Public](https://public.tableau.com/views/africa_food_security_dashboard/AfricaFoodSecurityDashboard?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

## Policy Relevance
The lag structure of this analysis is directly relevant to early warning system
calibration used by WFP, FEWS NET, and IGAD. Understanding how long it takes
for a drought shock to manifest as measurable food insecurity increases -- and
whether that lag differs by sub-region -- informs pre-positioning of humanitarian
resources and triggers for emergency response activation.

## Author
GitHub: https://github.com/clint4143/drought-food-insecurity-africa
