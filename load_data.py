import pandas as pd

DATA_DIR = "ecosphere_seed_data"

departments = pd.read_csv(f"{DATA_DIR}/departments.csv")
carbon_transactions = pd.read_csv(f"{DATA_DIR}/carbon_transactions.csv")
csr_activities = pd.read_csv(f"{DATA_DIR}/csr_activities.csv")
employee_participation = pd.read_csv(f"{DATA_DIR}/employee_participation.csv")
challenges = pd.read_csv(f"{DATA_DIR}/challenges.csv")
challenge_participation = pd.read_csv(f"{DATA_DIR}/challenge_participation.csv")
department_scores = pd.read_csv(f"{DATA_DIR}/department_scores.csv")

datasets = {
    "departments": departments,
    "carbon_transactions": carbon_transactions,
    "csr_activities": csr_activities,
    "employee_participation": employee_participation,
    "challenges": challenges,
    "challenge_participation": challenge_participation,
    "department_scores": department_scores,
}

# Print shape and columns for each table
for name, df in datasets.items():
    print(f"\n{name}: {df.shape[0]} rows, {df.shape[1]} columns")
    print(df.columns.tolist())

# Check that department_id values match across tables (referential integrity check)
valid_ids = set(departments["department_id"])
print("\n--- Referential integrity check ---")
print("Invalid dept IDs in carbon_transactions:", set(carbon_transactions["department_id"]) - valid_ids)
print("Invalid dept IDs in department_scores:", set(department_scores["department_id"]) - valid_ids)
