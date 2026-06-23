import pandas as pd

clients = pd.read_csv("clients.csv")

print("=== CLIENTS BEFORE ===")
print(f"Shape: {clients.shape}")
print(f"Missing values:\n{clients.isnull().sum()}")
print(f"Duplicates: {clients.duplicated().sum()}")

# Check client_id is unique — it should be your primary key
print(f"Unique client_ids: {clients['client_id'].nunique()}")

# Fix any whitespace in text columns
clients['client_name'] = clients['client_name'].str.strip()
clients['industry'] = clients['industry'].str.strip()
clients['client_country'] = clients['client_country'].str.strip()

# Convert contract_start to datetime
clients['contract_start'] = pd.to_datetime(clients['contract_start'])

# Remove duplicates if any
clients = clients.drop_duplicates()

print("\n=== CLIENTS AFTER ===")
print(f"Shape: {clients.shape}")
print(f"Missing values:\n{clients.isnull().sum()}")

clients.to_csv("clients_clean.csv", index=False)
print("Saved to data/clean/clients_clean.csv")

recruiters = pd.read_csv("recruiters.csv")

print("=== RECRUITERS BEFORE ===")
print(f"Shape: {recruiters.shape}")
print(f"Missing values:\n{recruiters.isnull().sum()}")
print(f"Duplicates: {recruiters.duplicated().sum()}")

# Check recruiter_id is unique
print(f"Unique recruiter_ids: {recruiters['recruiter_id'].nunique()}")

# Fix whitespace
recruiters['recruiter_name'] = recruiters['recruiter_name'].str.strip()
recruiters['seniority'] = recruiters['seniority'].str.strip()
recruiters['base_country'] = recruiters['base_country'].str.strip()

# Convert hire_date to datetime
recruiters['hire_date'] = pd.to_datetime(recruiters['hire_date'])

# Remove duplicates
recruiters = recruiters.drop_duplicates()

print("\n=== RECRUITERS AFTER ===")
print(f"Shape: {recruiters.shape}")
print(f"Missing values:\n{recruiters.isnull().sum()}")

recruiters.to_csv("recruiters_clean.csv", index=False)
print("Saved to data/clean/recruiters_clean.csv")