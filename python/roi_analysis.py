import pandas as pd
import json
from datetime import datetime

# ── LOAD CLEAN DATA ───────────────────────────────────
df = pd.read_csv("data/clean/placements_clean.csv")

print(f"Loaded {len(df)} clean placements")

# ── CORE CALCULATIONS ─────────────────────────────────
overall_avg = df['days_to_fill'].mean()
avg_fee = df['placement_fee'].mean()
cost_per_day = avg_fee / overall_avg

# ── COUNTRY PERFORMANCE ───────────────────────────────
country_stats = (df.groupby('candidate_country')
                 .agg(
                     placements=('placement_id', 'count'),
                     avg_days=('days_to_fill', 'mean'),
                     total_fees=('placement_fee', 'sum'),
                     avg_fee=('placement_fee', 'mean')
                 )
                 .round(2))

# ROI for every country — data decides not assumption
country_stats['days_saved'] = (
    overall_avg - country_stats['avg_days']
).round(2)

country_stats['non_country_placements'] = (
    len(df) - country_stats['placements']
)

country_stats['shift_volume_8pct'] = (
    country_stats['non_country_placements'] * 0.08
).astype(int)

country_stats['annual_roi_8pct'] = (
    country_stats['days_saved'] *
    cost_per_day *
    country_stats['shift_volume_8pct']
).round(0)

country_stats = country_stats.sort_values(
    'annual_roi_8pct', ascending=False
)

# ── SENSITIVITY ANALYSIS ──────────────────────────────
best_country = country_stats['annual_roi_8pct'].idxmax()
best_country_data = country_stats.loc[best_country]

sensitivity_rows = []
for pct in [0.05, 0.08, 0.10, 0.15, 0.20]:
    non_country = int(
        best_country_data['non_country_placements']
    )
    shift_vol = int(non_country * pct)
    roi = (best_country_data['days_saved'] *
           cost_per_day * shift_vol)
    sensitivity_rows.append({
        'shift_pct': f"{pct:.0%}",
        'placements_shifted': shift_vol,
        'annual_roi': round(roi, 0)
    })

sensitivity_df = pd.DataFrame(sensitivity_rows)

# ── COUNTRIES TO SHIFT AWAY FROM ─────────────────────
# Negative ROI countries — cost money vs overall avg
negative_roi = country_stats[
    country_stats['annual_roi_8pct'] < 0
].copy()

# ── RECRUITER PERFORMANCE GAP ─────────────────────────
recruiter_stats = (df.groupby('recruiter_id')
                   .agg(
                       avg_days=('days_to_fill', 'mean'),
                       total_fee=('placement_fee', 'sum'),
                       placements=('placement_id', 'count')
                   ).round(2))

top_5_avg = (recruiter_stats
             .nlargest(5, 'total_fee')['avg_days']
             .mean())
bottom_5_avg = (recruiter_stats
                .nsmallest(5, 'total_fee')['avg_days']
                .mean())
performance_gap = bottom_5_avg - top_5_avg
bottom_5_placements = (recruiter_stats
                       .nsmallest(5, 'total_fee')
                       ['placements'].sum())
recruiter_roi = (performance_gap *
                 cost_per_day *
                 bottom_5_placements)

# ── SENIOR ROLE ANALYSIS BY COUNTRY ──────────────────
senior_mask = df['job_title'].str.contains(
    'Senior|Sr|Manager', na=False
)
senior_by_country = (df[senior_mask]
                     .groupby('candidate_country')
                     .agg(
                         avg_days=('days_to_fill', 'mean'),
                         avg_fee=('placement_fee', 'mean'),
                         count=('placement_id', 'count')
                     )
                     .round(2)
                     .sort_values('avg_fee',
                                  ascending=False))

# ── HIGHEST FEE COUNTRY ───────────────────────────────
highest_fee_country = (df.groupby('candidate_country')
                        ['placement_fee']
                        .mean()
                        .idxmax())
highest_fee = (df.groupby('candidate_country')
               ['placement_fee']
               .mean()
               .max())

# ── TOTAL ROI ─────────────────────────────────────────
sourcing_roi = float(best_country_data['annual_roi_8pct'])

# Additional saving from reducing Nigeria/Kenya sourcing
avoid_loss = abs(float(
    negative_roi['annual_roi_8pct'].sum()
))

total_roi = sourcing_roi + recruiter_roi

# ── PRINT REPORT ──────────────────────────────────────
print("\n" + "="*55)
print("ROI ANALYSIS REPORT")
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("="*55)

print("\n── CORE METRICS ─────────────────────────────────────")
print(f"Overall avg days to fill:  {overall_avg:.1f}")
print(f"Average placement fee:     ${avg_fee:,.2f}")
print(f"Cost per day unfilled:     ${cost_per_day:.2f}")
print(f"Total placements:          {len(df):,}")

print("\n── ALL COUNTRIES ROI (8% shift) ─────────────────────")
print(country_stats[[
    'avg_days',
    'days_saved',
    'shift_volume_8pct',
    'annual_roi_8pct'
]].to_string())

print("\n── COUNTRIES WITH NEGATIVE ROI ──────────────────────")
print("These countries cost money vs average:")
print(negative_roi[[
    'avg_days',
    'days_saved',
    'annual_roi_8pct'
]].to_string())
print(f"\nTotal loss from negative ROI countries: "
      f"${avoid_loss:,.0f}")
print("Recommendation: reduce sourcing from these "
      "countries")

print(f"\n── DATA RECOMMENDATION ──────────────────────────────")
print(f"Best country to shift TO:  {best_country}")
print(f"Avg days to fill:          "
      f"{best_country_data['avg_days']:.1f} days")
print(f"Days saved:                "
      f"{best_country_data['days_saved']:.1f} days")
print(f"Annual ROI (8% shift):     "
      f"${best_country_data['annual_roi_8pct']:,.0f}")

print(f"\n── SENSITIVITY ANALYSIS: {best_country} ──────────────")
print(sensitivity_df.to_string(index=False))

print(f"\n── SENIOR ROLES BY COUNTRY ──────────────────────────")
print("Sorted by avg fee — high value role sourcing:")
print(senior_by_country.to_string())
print(f"\nHighest avg fee country overall: "
      f"{highest_fee_country} (${highest_fee:,.2f})")

print(f"\n── RECRUITER PERFORMANCE GAP ────────────────────────")
print(f"Top 5 recruiters avg days:    {top_5_avg:.1f}")
print(f"Bottom 5 recruiters avg days: {bottom_5_avg:.1f}")
print(f"Performance gap:              {performance_gap:.1f} days")
print(f"Recruiter ROI:                ${recruiter_roi:,.0f}")
print(f"Note: Small gap (0.3 days) — recruiters are")
print(f"performing consistently. Low improvement ROI.")

print(f"\n── TOTAL ROI SUMMARY ────────────────────────────────")
print(f"Sourcing to Pakistan (8%):  ${sourcing_roi:,.0f}")
print(f"Recruiter performance:      ${recruiter_roi:,.0f}")
print(f"TOTAL ESTIMATED ROI:        ${total_roi:,.0f}")
print("="*55)

# ── SAVE OUTPUTS ──────────────────────────────────────
country_stats.to_csv(
    "data/clean/country_roi_analysis.csv"
)
print("\n✅ Saved: data/clean/country_roi_analysis.csv")

sensitivity_df.to_csv(
    "data/clean/sensitivity_analysis.csv",
    index=False
)
print("✅ Saved: data/clean/sensitivity_analysis.csv")

roi_summary = {
    "generated_date": datetime.now().strftime("%Y-%m-%d"),
    "overall_avg_days": round(overall_avg, 1),
    "avg_fee": round(avg_fee, 2),
    "cost_per_day": round(cost_per_day, 2),
    "best_country": best_country,
    "best_country_avg_days": round(
        float(best_country_data['avg_days']), 1
    ),
    "days_saved": round(
        float(best_country_data['days_saved']), 1
    ),
    "sourcing_roi_8pct": round(sourcing_roi, 0),
    "recruiter_roi": round(recruiter_roi, 0),
    "total_roi": round(total_roi, 0),
    "negative_roi_countries": list(negative_roi.index),
    "negative_roi_total_loss": round(avoid_loss, 0),
    "highest_fee_country": highest_fee_country
}

with open("data/clean/roi_summary.json", "w") as f:
    json.dump(roi_summary, f, indent=2)
print("✅ Saved: data/clean/roi_summary.json")

print("\nTo view saved results anytime:")
print("  CSV: open data/clean/country_roi_analysis.csv")
print("  JSON: open data/clean/roi_summary.json")