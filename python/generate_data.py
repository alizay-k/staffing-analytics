import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

# ---- BUILDING BLOCKS ----

job_titles = [
    "Senior IT Support", "Sr. IT Support",
    "Senior IT", "Sr IT Support",
    "Junior Developer", "Jr Developer",
    "Junior Dev", "Jr. Developer",
    "Data Analyst", "Data Anlyst",
    "Data Analysis", "DataAnalyst",
    "HR Manager", "H.R. Manager",
    "Human Resources Manager", "HR Mgr"
]

candidate_countries = [
    "Pakistan", "pak", "PK",
    "India", "india", "IND",
    "Philippines", "philippines", "PH",
    "Kenya", "kenya", "KEN",
    "Nigeria", "nigeria", "NG"
]

client_countries_list = [
    "United Kingdom", "United States",
    "UAE", "Canada", "Australia"
]

fill_days_by_country = {
    "Pakistan": (15, 25), "pak": (15, 25), "PK": (15, 25),
    "India": (22, 34), "india": (22, 34), "IND": (22, 34),
    "Philippines": (24, 36), "philippines": (24, 36),
    "PH": (24, 36),
    "Kenya": (26, 38), "kenya": (26, 38), "KEN": (26, 38),
    "Nigeria": (28, 42), "nigeria": (28, 42), "NG": (28, 42),
}

# Realistic company names for clients
company_names = [
    "TalentBridge Solutions", "PeakHire Group",
    "GlobalStaff Partners", "NexGen Recruitment",
    "EliteForce Staffing", "ProLink HR",
    "SwiftTalent Agency", "CoreHire Solutions",
    "PrimePath Staffing", "ApexRecruit Ltd",
    "BrightForce Group", "ClearPath Hiring",
    "TrueNorth Staffing", "RapidHire Partners",
    "BlueStar Recruitment"
]

# Realistic recruiter names
first_names = [
    "Sarah", "James", "Aisha", "Omar", "Chen",
    "Fatima", "David", "Priya", "Emma",
    "Carlos", "Zara", "Ahmed", "Lisa", "Raj"
]
last_names = [
    "Khan", "Smith", "Johnson", "Patel", "Williams",
    "Ahmed", "Brown", "Singh", "Taylor", "Ali",
    "Davis", "Hassan", "Wilson", "Malik", "Jones"
]

# ---- GENERATE PLACEMENTS ----
rows = []

for i in range(1, 5001):
    country = random.choice(candidate_countries)
    min_days, max_days = fill_days_by_country[country]
    days = random.randint(min_days, max_days)
    job = random.choice(job_titles)

    # Bug fix: "Sr" not "SR" — case sensitive
    if "Senior" in job or "Sr" in job or "Manager" in job:
        fee = round(random.uniform(3000, 8000), 2)
    else:
        fee = round(random.uniform(1000, 4000), 2)

    # 8% missing fees
    if random.random() < 0.08:
        fee = None

    # Generate dates
    start_date = datetime(2023, 1, 1)
    post_offset = random.randint(0, 545)
    job_post_date = start_date + timedelta(days=post_offset)
    fill_date = job_post_date + timedelta(days=days)

    # Mixed date formats — 60% one way, 40% other
    if random.random() < 0.6:
        post_str = job_post_date.strftime("%Y-%m-%d")
        fill_str = fill_date.strftime("%Y-%m-%d")
    else:
        post_str = job_post_date.strftime("%d/%m/%Y")
        fill_str = fill_date.strftime("%d/%m/%Y")

    rows.append({
        "placement_id": i,
        "job_title": job,
        "job_post_date": post_str,
        "fill_date": fill_str,
        "days_to_fill": days,
        "placement_fee": fee,
        "client_id": random.randint(1, 100),
        "recruiter_id": random.randint(1, 30),
        "candidate_country": country,
        "client_country": random.choice(client_countries_list)
    })

df = pd.DataFrame(rows)

# Add 23 duplicate rows
duplicates = df.sample(23, random_state=42)
df = pd.concat([df, duplicates], ignore_index=True)

# Save to correct folder
df.to_csv("data/raw/placements_messy.csv", index=False)

print(f"Total rows: {len(df)}")
print(f"Missing fees: {df['placement_fee'].isnull().sum()}")
print(f"Unique job title formats: {df['job_title'].nunique()}")
print(f"Unique country formats: "
      f"{df['candidate_country'].nunique()}")
print(f"\nSample of messy data:")
print(df[['job_title', 'candidate_country',
          'job_post_date', 'placement_fee']].head(8))

# ---- GENERATE CLIENTS ----
clients = []
client_industries = [
    "Technology", "Healthcare", "Finance",
    "Retail", "Manufacturing"
]
client_countries_gen = [
    "United Kingdom", "United States",
    "UAE", "Canada", "Australia"
]

for i in range(1, 101):
    clients.append({
        "client_id": i,
        # Realistic name instead of Client_001
        "client_name": (f"{random.choice(company_names)}"
                        f" {i}"),
        "industry": random.choice(client_industries),
        "client_country": random.choice(client_countries_gen),
        "contract_start": (
            datetime(2022, 1, 1) +
            timedelta(days=random.randint(0, 365))
        ).strftime("%Y-%m-%d"),
        "monthly_retainer": round(
            random.uniform(2000, 15000), 2
        )
    })

clients_df = pd.DataFrame(clients)
clients_df.to_csv("data/raw/clients.csv", index=False)
print(f"\nClients generated: {len(clients_df)}")
print(clients_df[['client_id',
                   'client_name',
                   'industry']].head())

# ---- GENERATE RECRUITERS ----
recruiters = []
recruiter_countries = [
    "Pakistan", "India", "Philippines",
    "Kenya", "Nigeria"
]
seniority_levels = ["Junior", "Mid", "Senior"]

for i in range(1, 31):
    recruiters.append({
        "recruiter_id": i,
        # Realistic name instead of Recruiter_01
        "recruiter_name": (
            f"{random.choice(first_names)} "
            f"{random.choice(last_names)}"
        ),
        "seniority": random.choice(seniority_levels),
        "base_country": random.choice(recruiter_countries),
        "hire_date": (
            datetime(2020, 1, 1) +
            timedelta(days=random.randint(0, 1095))
        ).strftime("%Y-%m-%d"),
        "target_placements_monthly": random.randint(8, 20)
    })

recruiters_df = pd.DataFrame(recruiters)
recruiters_df.to_csv(
    "data/raw/recruiters.csv", index=False
)
print(f"\nRecruiters generated: {len(recruiters_df)}")
print(recruiters_df[['recruiter_id',
                      'recruiter_name',
                      'seniority',
                      'base_country']].head())