import pandas as pd
import numpy as np

df = pd.read_csv("data/clean/placements_clean.csv")

# ── FUNCTION 1 ────────────────────────────────────────
# Country performance summary
# Input: dataframe
# Output: grouped summary sorted by avg days

def country_performance(dataframe):
    """
    Summarize placement performance by country.
    Returns dataframe sorted fastest to slowest.
    Used in: weekly_report.py, roi_analysis.py
    """
    summary = (dataframe
               .groupby('candidate_country')
               .agg(
                   placements=('placement_id', 'count'),
                   avg_days=('days_to_fill', 'mean'),
                   total_fees=('placement_fee', 'sum'),
                   avg_fee=('placement_fee', 'mean')
               )
               .round(2)
               .sort_values('avg_days'))
    return summary

print("=== Function 1: Country Performance ===")
print(country_performance(df))

# ── FUNCTION 2 ────────────────────────────────────────
# ROI calculator
# Input: dataframe, country name, shift percentage
# Output: prints ROI breakdown
# Why inputs not hardcoded: makes function reusable
# for any country and any shift % — not just Pakistan 8%

def calculate_roi(dataframe, target_country, shift_pct):
    """
    Calculate ROI from shifting sourcing to target_country.
    target_country: string — must match column values
    shift_pct: float — e.g. 0.08 for 8%
    """
    overall_avg = dataframe['days_to_fill'].mean()
    country_avg = (dataframe[
        dataframe['candidate_country'] == target_country
    ]['days_to_fill'].mean())

    days_saved = overall_avg - country_avg
    avg_fee = dataframe['placement_fee'].mean()
    cost_per_day = avg_fee / overall_avg

    total = len(dataframe)
    country_count = len(dataframe[
        dataframe['candidate_country'] == target_country
    ])
    non_country = total - country_count
    shift_volume = int(non_country * shift_pct)
    annual_saving = (shift_volume *
                     days_saved *
                     cost_per_day)

    print(f"\n=== ROI: {target_country} "
          f"at {shift_pct:.0%} shift ===")
    print(f"Overall avg days:   {overall_avg:.1f}")
    print(f"{target_country} avg: {country_avg:.1f}")
    print(f"Days saved:         {days_saved:.1f}")
    print(f"Cost per day:       ${cost_per_day:.2f}")
    print(f"Placements shifted: {shift_volume}")
    print(f"Annual saving:      ${annual_saving:,.0f}")

print("\n=== Function 2: ROI Calculator ===")
# Data decides — check all countries
calculate_roi(df, "Pakistan", 0.08)
calculate_roi(df, "India", 0.08)
calculate_roi(df, "Philippines", 0.08)

# ── FUNCTION 3 ────────────────────────────────────────
# Data quality checker
# Input: dataframe, name for logging
# Output: prints quality report
# Why: reusable across all three tables without
# copy-pasting the same checks three times

def check_data_quality(dataframe, name):
    """
    Check and report data quality for any dataframe.
    Checks: row count, missing values, duplicates.
    """
    print(f"\n=== Data Quality: {name} ===")
    print(f"Rows:    {len(dataframe):,}")
    print(f"Columns: {len(dataframe.columns)}")

    missing = dataframe.isnull().sum()
    missing = missing[missing > 0]
    if len(missing) == 0:
        print("Missing: ✅ none")
    else:
        print(f"Missing:\n{missing}")

    dupes = dataframe.duplicated().sum()
    if dupes == 0:
        print("Dupes:   ✅ none")
    else:
        print(f"Dupes:   ⚠️  {dupes} found")

print("\n=== Function 3: Data Quality Check ===")
check_data_quality(df, "placements_clean")

clients = pd.read_csv("data/clean/clients_clean.csv")
check_data_quality(clients, "clients_clean")

recruiters = pd.read_csv(
    "data/clean/recruiters_clean.csv"
)
check_data_quality(recruiters, "recruiters_clean")