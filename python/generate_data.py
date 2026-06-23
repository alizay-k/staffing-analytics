import pandas as pd
import random 
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

job_titles=[
    "Senior IT Support","Sr.IT Support" ,"Senior IT","Sr IT Support",
    "Junior Developer","Jr Developer","Junior Dev","Jr.Developer",
    "Data Analyst","Data Anlyst","Data Analysis","DataAnalyst",
    "HR manager","H.R. Manager","Human Resources Manager", "HR Mgr"
]

candidate_countries=[
    "Pakistan", "pak", "PK",
    "India", "india", "IND",
    "Philippines", "philippines", "PH",
    "Kenya", "kenya", "KEN",
    "Nigeria", "nigeria", "NG"
]
client_countries = ["United Kingdom", "United States", "UAE",
                    "Canada", "Australia"]

fill_days_by_country = {
    "Pakistan": (15, 25), "pak": (15, 25), "PK": (15, 25),
    "India": (22, 34), "india": (22, 34), "IND": (22, 34),
    "Philippines": (24, 36), "philippines": (24, 36), "PH": (24, 36),
    "Kenya": (26, 38), "kenya": (26, 38), "KEN": (26, 38),
    "Nigeria": (28, 42), "nigeria": (28, 42), "NG": (28, 42),
}

# ---- GENERATE ROWS ----
rows = []

for i in range(0,5001):
    country=random.choice(candidate_countries)
    min_days,max_days=fill_days_by_country[country]
    days=random.randint(min_days,max_days)
    jobs=random.choice(job_titles)

    if "Senior" in jobs or "SR" in jobs or "Manager" in jobs:
        fee=round(random.uniform(3000,8000),2)
    else:
        fee=round(random.uniform(1000,4000),2)

    if random.random() < 0.08:
        fee=None

    
    start_date=datetime(2023,1,1)
    post_offset=random.randint(0,545)
    job_post_date=start_date+timedelta(days=post_offset)

    fill_date=job_post_date+timedelta(days=days)

    if random.random() < 0.6:
        post_str = job_post_date.strftime("%Y-%m-%d")
        fill_str = fill_date.strftime("%Y-%m-%d")
    else:
        post_str = job_post_date.strftime("%d/%m/%Y")
        fill_str = fill_date.strftime("%d/%m/%Y")

    rows.append({
        "placement_id": i,
        "job_title": jobs,
        "job_post_date": post_str,
        "fill_date": fill_str,
        "days_to_fill": days,
        "placement_fee": fee,
        "client_id": random.randint(1, 100),
        "recruiter_id": random.randint(1, 30),
        "candidate_country": country,
        "client_country": random.choice(client_countries)
    })

df = pd.DataFrame(rows)

# Add 23 exact duplicate rows
duplicates = df.sample(23, random_state=42)
df = pd.concat([df, duplicates], ignore_index=True)

# Save messy version
df.to_csv("placements_messy.csv", index=False)

# Generate clients.csv
clients = []
client_industries = [
    "Technology", "Healthcare", "Finance",
    "Retail", "Manufacturing"
]
client_countries = [
    "United Kingdom", "United States",
    "UAE", "Canada", "Australia"
]

for i in range(1, 101):
    clients.append({
        "client_id": i,
        "client_name": f"Client_{i:03d}",
        "industry": random.choice(client_industries),
        "client_country": random.choice(client_countries),
        "contract_start": (datetime(2022, 1, 1) +
                          timedelta(days=random.randint(0, 365))
                          ).strftime("%Y-%m-%d"),
        "monthly_retainer": round(random.uniform(2000, 15000), 2)
    })

clients_df = pd.DataFrame(clients)
clients_df.to_csv("clients.csv", index=False)
print(f"Clients generated: {len(clients_df)}")

# Generate recruiters.csv
recruiters = []
recruiter_countries = ["Pakistan", "India", "Philippines", "Kenya", "Nigeria"]
seniority_levels = ["Junior", "Mid", "Senior"]

for i in range(1, 31):
    recruiters.append({
        "recruiter_id": i,
        "recruiter_name": f"Recruiter_{i:02d}",
        "seniority": random.choice(seniority_levels),
        "base_country": random.choice(recruiter_countries),
        "hire_date": (datetime(2020, 1, 1) +
                     timedelta(days=random.randint(0, 1095))
                     ).strftime("%Y-%m-%d"),
        "target_placements_monthly": random.randint(8, 20)
    })

recruiters_df = pd.DataFrame(recruiters)
recruiters_df.to_csv("recruiters.csv", index=False)
print(f"Recruiters generated: {len(recruiters_df)}")