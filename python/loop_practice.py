import pandas as pd

df=pd.read_csv("data/clean/placements_clean.csv")

for column in df.columns:
    missing=df[column].isnull().sum()
    pct=missing/len(df)*100
    if pct >0:
        print(f"{column}:{missing} missing:{pct:.1f}%")
    else:
        print(f"{column} clean.")

numerical_column=["placement_id","days_to_fill","daily_rate"]
for col in numerical_column:
    print(f"\n{col}:")
    print(f"  Mean:   {df[col].mean():.2f}")
    print(f"  Median: {df[col].median():.2f}")
    print(f"  Min:    {df[col].min():.2f}")
    print(f"  Max:    {df[col].max():.2f}")

countries=df['candidate_country'].unique()

for country in countries:
    country_df=df[df['candidate_country']==country]
    avg_days=country_df['days_to_fill'].mean()
    total_fee=country_df['placement_fee'].sum()
    count=len(country_df)

    print(f"{country}:")
    print(f"  Placements: {count}")
    print(f"  Avg days:   {avg_days:.1f}")
    print(f"  Total fees: ${total_fee:,.0f}")


