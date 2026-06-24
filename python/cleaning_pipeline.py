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

before_missing=df['placement_fee'].isnull().sum()
df['placement_fee']=df.groupby('job_title')['placement_fee'].transform(
    lambda x:x.fillna(x.median())
)
after_missing = df['placement_fee'].isnull().sum()

print(f"\nMissing fees before: {before_missing}")
print(f"Missing fees after: {after_missing}")
print(f"\nMedian fee by job title:")
print(df.groupby('job_title')['placement_fee'].median().round(2))

before_rows = len(df)
df = df.drop_duplicates()
after_rows = len(df)

print(f"\nRows before dedup: {before_rows}")
print(f"Rows after dedup: {after_rows}")
print(f"Duplicates removed: {before_rows - after_rows}")

print("\n=== AFTER CLEANING ===")
print(f"Shape: {df.shape}")
print(f"Missing values:\n{df.isnull().sum()}")
print(f"Duplicates: {df.duplicated().sum()}")

# Save clean file
df.to_csv("data/clean/placements_clean.csv", index=False)

print("=== ROI Analysis===")
overall_avg=df["days_to_fill"].mean()

pak_avg=df[df["candidate_country"]=="Pakistan"]["days_to_fill"].mean()

days_saved=overall_avg-pak_avg
avg_fee=df["placement_fee"].mean()
cost_per_day=avg_fee/overall_avg

total_placements=len(df)
pak_placements=len(df[df["candidate_country"]=="Pakistan"])
pak_pct=pak_placements/total_placements

# Current state
print(f"Total placements: {total_placements}")
print(f"Pakistan current share: {pak_pct:.1%}")
print(f"Pakistan current placements: {pak_placements}")

# The opportunity is placements NOT currently in Pakistan
non_pak_placements = total_placements - pak_placements
shift_volume = int(non_pak_placements * 0.08)

# Saving from shifting those placements
annual_saving = shift_volume * days_saved * cost_per_day

print(f"\nNon-Pakistan placements: {non_pak_placements}")
print(f"8% of non-Pakistan shifted: {shift_volume}")
print(f"Days saved per placement: {days_saved:.1f}")
print(f"Cost per day: ${cost_per_day:.2f}")
print(f"Revised annual saving: ${annual_saving:,.0f}")

# Sensitivity check — what if we're wrong about cost per day?
print("=== Sensitivity Analysis ===")
for pct in [0.05, 0.08, 0.10, 0.15]:
    volume = int(non_pak_placements * pct)
    saving = volume * days_saved * cost_per_day
    print(f"If we shift {pct:.0%}: {volume} placements → ${saving:,.0f} saving")


# # Creating new columns
# df['Daily_rate']=(df["placement_fee"]/df["days_to_fill"]).round(2)
# print("\nDaily rate column added:")
# print(df[['placement_fee',
#           'days_to_fill',
#           'daily_rate']].head())

# avg_days=df["days_to_fill"].mean()
# df['is_fast_fill']=df["days_to_fill"]<avg_days
# print(f"\nAverage days to fill: {avg_days:.1f}")
# print(f"Fast fills: {df['is_fast_fill'].sum()}")
# print(f"Slow fills: {(~df['is_fast_fill']).sum()}")

# def categorize_fee(fee):
#     if fee < 2000:
#         return 'Low'
#     elif fee <5000:
#         return 'Medium'
#     else:
#         return 'High'
    
# df['fee_category']=df["placement_fee"].apply(categorize_fee)
# print("\nFee categories:")
# print(df['fee_category'].value_counts())

# #