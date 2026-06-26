import pandas as pd
import json
import io
import sys
import os
from datetime import datetime

# ── LOAD DATA ─────────────────────────────────────────
def load_data():
    """Load all three clean tables"""
    placements = pd.read_csv(
        "data/clean/placements_clean.csv"
    )
    clients = pd.read_csv(
        "data/clean/clients_clean.csv"
    )
    recruiters = pd.read_csv(
        "data/clean/recruiters_clean.csv"
    )
    return placements, clients, recruiters

def load_roi_summary():
    """Load pre-calculated ROI from JSON
    Why: avoids recalculating every time report runs
    roi_analysis.py saves this — we just read it
    """
    with open("data/clean/roi_summary.json", "r") as f:
        return json.load(f)

# ── REPORT FUNCTIONS ──────────────────────────────────

def check_data_quality(dataframe, name):
    """Check quality for any table"""
    missing = dataframe.isnull().sum().sum()
    dupes = dataframe.duplicated().sum()
    status_missing = "✅" if missing == 0 else "⚠️"
    status_dupes = "✅" if dupes == 0 else "⚠️"
    print(f"  {name}:")
    print(f"    Rows: {len(dataframe):,} | "
          f"Missing: {status_missing} {missing} | "
          f"Dupes: {status_dupes} {dupes}")

def country_performance(dataframe):
    """Summarize by country — sorted fastest first"""
    return (dataframe
            .groupby('candidate_country')
            .agg(
                placements=('placement_id', 'count'),
                avg_days=('days_to_fill', 'mean'),
                total_fees=('placement_fee', 'sum'),
                avg_fee=('placement_fee', 'mean')
            )
            .round(2)
            .sort_values('avg_days'))

def recruiter_ranking(merged_df):
    """Top 10 recruiters by total revenue"""
    return (merged_df
            .groupby('recruiter_name')
            ['placement_fee']
            .agg(['sum', 'count', 'mean'])
            .round(2)
            .sort_values('sum', ascending=False)
            .head(10)
            .rename(columns={
                'sum': 'total_fees',
                'count': 'placements',
                'mean': 'avg_fee'
            }))

def monthly_trend(dataframe):
    """Placement volume and revenue by month"""
    dataframe = dataframe.copy()
    dataframe['job_post_date'] = pd.to_datetime(
        dataframe['job_post_date']
    )
    dataframe['month'] = (dataframe['job_post_date']
                          .dt.to_period('M'))
    return (dataframe
            .groupby('month')
            .agg(
                placements=('placement_id', 'count'),
                total_fees=('placement_fee', 'sum'),
                avg_days=('days_to_fill', 'mean')
            )
            .round(2))

def fee_category_breakdown(dataframe):
    """Break down by fee category"""
    def categorize(fee):
        if fee < 2000:
            return 'Low (<$2k)'
        elif fee < 5000:
            return 'Medium ($2k-$5k)'
        else:
            return 'High (>$5k)'

    dataframe = dataframe.copy()
    dataframe['fee_category'] = (
        dataframe['placement_fee'].apply(categorize)
    )
    return (dataframe
            .groupby('fee_category')
            .agg(
                placements=('placement_id', 'count'),
                total_fees=('placement_fee', 'sum'),
                avg_fee=('placement_fee', 'mean')
            )
            .round(2))

def save_report(report_content):
    """Save report to timestamped file
    Why: preserves every report so you can compare
    week over week without rerunning anything
    """
    os.makedirs("reports", exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"reports/weekly_report_{date_str}.txt"
    with open(filename, "w",encoding="utf-8") as f:
        f.write(report_content)
    print(f"\n✅ Report saved: {filename}")
    return filename

# ── MAIN REPORT ───────────────────────────────────────

def generate_report():
    """Generate full weekly staffing analytics report"""

    report_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M"
    )
    print("\n" + "="*55)
    print("    STAFFING ANALYTICS — WEEKLY REPORT")
    print(f"    Generated: {report_date}")
    print("="*55)

    # Load everything
    placements, clients, recruiters = load_data()
    roi = load_roi_summary()

    # Merge for recruiter names
    merged = pd.merge(
        placements,
        recruiters[['recruiter_id', 'recruiter_name',
                     'seniority']],
        on='recruiter_id',
        how='left'
    )

    # ── SECTION 1: Data Quality ───────────────────────
    print("\n── 1. DATA QUALITY CHECK ────────────────────────")
    check_data_quality(placements, "placements_clean")
    check_data_quality(clients, "clients_clean")
    check_data_quality(recruiters, "recruiters_clean")

    # ── SECTION 2: Volume Summary ─────────────────────
    print("\n── 2. VOLUME SUMMARY ────────────────────────────")
    print(f"  Total placements:     {len(placements):,}")
    print(f"  Total revenue:        "
          f"${placements['placement_fee'].sum():,.0f}")
    print(f"  Average fee:          "
          f"${placements['placement_fee'].mean():,.2f}")
    print(f"  Average days to fill: "
          f"{placements['days_to_fill'].mean():.1f}")
    print(f"  Cost per day unfilled:${roi['cost_per_day']}")

    # ── SECTION 3: Country Performance ────────────────
    print("\n── 3. COUNTRY PERFORMANCE ───────────────────────")
    print("  Sorted fastest to slowest:")
    cp = country_performance(placements)
    print(cp.to_string())
    print(f"\n  ⚡ Fastest: {cp.index[0]} "
          f"({cp['avg_days'].iloc[0]:.1f} days)")
    print(f"  🐢 Slowest: {cp.index[-1]} "
          f"({cp['avg_days'].iloc[-1]:.1f} days)")

    # ── SECTION 4: ROI Summary ────────────────────────
    print("\n── 4. ROI SUMMARY ───────────────────────────────")
    print(f"  ROI calculated:        {roi['generated_date']}")
    print(f"  Best sourcing country: {roi['best_country']}")
    print(f"  Days saved:            {roi['days_saved']}")
    print(f"  Sourcing ROI (8%):     "
          f"${roi['sourcing_roi_8pct']:,.0f}")
    print(f"  Recruiter gap ROI:     "
          f"${roi['recruiter_roi']:,.0f}")
    print(f"  TOTAL ROI:             "
          f"${roi['total_roi']:,.0f}")
    if 'negative_roi_countries' in roi:
        print(f"\n  ⚠️  Negative ROI countries "
              f"(reduce sourcing from these):")
        for country in roi['negative_roi_countries']:
            print(f"     → {country}")

    # ── SECTION 5: Top 10 Recruiters ──────────────────
    print("\n── 5. TOP 10 RECRUITERS BY REVENUE ─────────────")
    print(recruiter_ranking(merged).to_string())

    # ── SECTION 6: Fee Category Breakdown ─────────────
    print("\n── 6. FEE CATEGORY BREAKDOWN ────────────────────")
    print(fee_category_breakdown(placements).to_string())

    # ── SECTION 7: Monthly Trend ──────────────────────
    print("\n── 7. MONTHLY TREND (Last 6 Months) ────────────")
    trend = monthly_trend(placements)
    print(trend.tail(6).to_string())

    # ── SECTION 8: Key Recommendations ───────────────
    print("\n── 8. KEY RECOMMENDATIONS ───────────────────────")
    print(f"  1. SHIFT SOURCING TO {roi['best_country']}:")
    print(f"     → {roi['best_country']} fills roles "
          f"{roi['days_saved']} days faster")
    print(f"     → Shifting 8% saves "
          f"${roi['sourcing_roi_8pct']:,.0f} annually")
    print(f"     → Trade-off: 2 weeks recruiter retraining")
    if 'negative_roi_countries' in roi:
        print(f"\n  2. REDUCE SOURCING FROM:")
        for c in roi['negative_roi_countries']:
            print(f"     → {c} (slower than average = "
                  f"costs money per placement)")
    print(f"\n  3. RECRUITER PERFORMANCE:")
    print(f"     → Gap is only 0.3 days across recruiters")
    print(f"     → Team is performing consistently")
    print(f"     → Focus energy on sourcing shift "
          f"not recruiter training")

    print("\n" + "="*55)
    print("  END OF REPORT")
    print("="*55 + "\n")

# ── RUN AND SAVE ──────────────────────────────────────
if __name__ == "__main__":
    # Capture output
    captured = io.StringIO()
    sys.stdout = captured

    generate_report()

    # Restore printing
    sys.stdout = sys.__stdout__

    # Get captured text
    report_text = captured.getvalue()

    # Print to screen
    print(report_text)

    # Save to file
    save_report(report_text)