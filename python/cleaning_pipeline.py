import pandas as pd

df=pd.read_csv("data/raw/placements_messy.csv")

print("=== Before Cleaning ===")
print(f"shape:{df.shape}")
print(f"Missing values:\n{df.isnull().sum()}")
print(f"Duplicates:{df.duplicated().sum()}")

df["job_post_date"]=pd.to_datetime(df["job_post_date"],format='mixed',dayfirst=True)
df["fill_date"]=pd.to_datetime(df["fill_date"],format='mixed',dayfirst=True)

df["days_check"]=(df["fill_date"]-df["job_post_date"]).dt.days
match=(df['days_check']==df['days_to_fill']).all()
print(f"\nVerify match:{match}")

df = df.drop(columns=['days_check'])

#Mapping all variations to one clean name
country_mapping={
    "Pakistan": "Pakistan", "pak": "Pakistan", "PK": "Pakistan",
    "India": "India", "india": "India", "IND": "India",
    "Philippines": "Philippines", "philippines": "Philippines", "PH": "Philippines",
    "Kenya": "Kenya", "kenya": "Kenya", "KEN": "Kenya",
    "Nigeria": "Nigeria", "nigeria": "Nigeria", "NG": "Nigeria"
}

before_unique=df['candidate_country'].nunique()
df["candidate_country"]=df["candidate_country"].map(country_mapping)
after_unique=df["candidate_country"].nunique()

print(f"\nCountry formats before: {before_unique}")
print(f"Country formats after: {after_unique}")
print(df['candidate_country'].value_counts())

title_mapping={
     "Senior IT Support": "Senior IT Support",
    "Sr. IT Support": "Senior IT Support",
    "Senior IT": "Senior IT Support",
    "Sr IT Support": "Senior IT Support",
    "Junior Developer": "Junior Developer",
    "Jr Developer": "Junior Developer",
    "Junior Dev": "Junior Developer",
    "Jr. Developer": "Junior Developer",
    "Data Analyst": "Data Analyst",
    "Data Anlyst": "Data Analyst",
    "Data Analysis": "Data Analyst",
    "DataAnalyst": "Data Analyst",
    "HR Manager": "HR Manager",
    "H.R. Manager": "HR Manager",
    "Human Resources Manager": "HR Manager",
    "HR Mgr": "HR Manager"
}

before_titles=df['job_title'].nunique()
df['job_title']=df["job_title"].map(title_mapping)
after_titles=df['job_title'].nunique()

print(f"\nJob title formats before: {before_titles}")
print(f"Job title formats after: {after_titles}")
print(df['job_title'].value_counts())

before_rows = len(df)
df = df.drop_duplicates()
after_rows = len(df)

print(f"\nRows before dedup: {before_rows}")
print(f"Rows after dedup: {after_rows}")
print(f"Duplicates removed: {before_rows - after_rows}")

before_missing=df['placement_fee'].isnull().sum()
df['placement_fee']=df.groupby('job_title')['placement_fee'].transform(
    lambda x:x.fillna(x.median())
)
after_missing = df['placement_fee'].isnull().sum()

print(f"\nMissing fees before: {before_missing}")
print(f"Missing fees after: {after_missing}")
print(f"\nMedian fee by job title:")
print(df.groupby('job_title')['placement_fee'].median().round(2))



print("\n=== AFTER CLEANING ===")
print(f"Shape: {df.shape}")
print(f"Missing values:\n{df.isnull().sum()}")
print(f"Duplicates: {df.duplicated().sum()}")

# Creating new columns
df['daily_rate']=(df["placement_fee"]/df["days_to_fill"]).round(2)
print("\nDaily rate column added:")
print(df[['placement_fee',
          'days_to_fill',
          'daily_rate']].head())

avg_days=df["days_to_fill"].mean()
df['is_fast_fill']=df["days_to_fill"] < avg_days
print(f"\nAverage days to fill: {avg_days:.1f}")
print(f"Fast fills: {df['is_fast_fill'].sum()}")
print(f"Slow fills: {(~df['is_fast_fill']).sum()}")

def categorize_fee(fee):
    if fee < 2000:
        return 'Low'
    elif fee <5000:
        return 'Medium'
    else:
        return 'High'
    
df['fee_category']=df["placement_fee"].apply(categorize_fee)
print("\nFee categories:")
print(df['fee_category'].value_counts())


# Save clean file
df.to_csv("data/clean/placements_clean.csv", index=False)


# Load clients and recruiters clean files
clients = pd.read_csv("data/clean/clients_clean.csv")
recruiters = pd.read_csv(
    "data/clean/recruiters_clean.csv"
)

print("\nBefore merge:")
print(f"Placements: {len(df)} rows, {len(df.columns)} cols")
print(f"Clients: {len(clients)} rows")
print(f"Recruiters: {len(recruiters)} rows")

# Step 1: merge placements with clients
df_merged = pd.merge(
    df,
    clients[['client_id', 'client_name', 'industry']],
    on='client_id',
    how='left'
)

# Step 2: merge result with recruiters
df_merged = pd.merge(
    df_merged,
    recruiters[['recruiter_id',
                 'recruiter_name',
                 'seniority']],
    on='recruiter_id',
    how='left'
)

print("\nAfter merge:")
print(f"Merged: {len(df_merged)} rows, "
      f"{len(df_merged.columns)} cols")
print(f"\nNew columns added: "
      f"{set(df_merged.columns) - set(df.columns)}")
print(f"\nSample of merged data:")
print(df_merged[['placement_fee',
                  'client_name',
                  'recruiter_name',
                  'candidate_country']].head())

# Verify no placements lost in merge
assert len(df_merged) == len(df), \
    "Merge lost rows — check for duplicate keys"
print("\n✅ Row count verified — no placements lost")

# ── SKILL 8: EXPORT ──────────────────────────────────

# Save clean placements (your main cleaned file)
df.to_csv("data/clean/placements_clean.csv",
          index=False)
print("\nSaved: data/clean/placements_clean.csv")
print(f"Rows: {len(df)}, Columns: {len(df.columns)}")

# Save merged file (all three tables combined)
df_merged.to_csv(
    "data/clean/placements_merged.csv",
    index=False
)
print("\nSaved: data/clean/placements_merged.csv")
print(f"Rows: {len(df_merged)}, "
      f"Columns: {len(df_merged.columns)}")

# Final summary
print("\n" + "="*40)
print("PIPELINE COMPLETE")
print("="*40)
print(f"Input rows (messy):  5023")
print(f"Output rows (clean): {len(df)}")
print(f"Rows removed:        {5023 - len(df)}")
print(f"Columns in clean:    {len(df.columns)}")
print(f"Columns in merged:   {len(df_merged.columns)}")
print(f"New columns added:   "
      f"daily_rate, is_fast_fill, fee_category")