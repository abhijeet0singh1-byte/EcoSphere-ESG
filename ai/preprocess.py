import pandas as pd

DATA_DIR = "ecosphere_seed_data"

departments = pd.read_csv(f"{DATA_DIR}/departments.csv")
employees = pd.read_csv(f"{DATA_DIR}/employees.csv")
carbon_transactions = pd.read_csv(f"{DATA_DIR}/carbon_transactions.csv")
employee_participation = pd.read_csv(f"{DATA_DIR}/employee_participation.csv")
challenge_participation = pd.read_csv(f"{DATA_DIR}/challenge_participation.csv")
department_scores = pd.read_csv(f"{DATA_DIR}/department_scores.csv")

# ---------- 1. Carbon: total emissions per department ----------
carbon_by_dept = (
    carbon_transactions.groupby("department_id")["co2e_emitted_kg"]
    .sum()
    .reset_index()
    .rename(columns={"co2e_emitted_kg": "total_co2e_kg"})
)

# ---------- 2. CSR: map employee_participation -> department via employees ----------
csr_with_dept = employee_participation.merge(
    employees[["employee_id", "department_id"]], on="employee_id", how="left"
)
csr_by_dept = (
    csr_with_dept[csr_with_dept["approval_status"] == "Approved"]
    .groupby("department_id")
    .agg(
        approved_csr_count=("participation_id", "count"),
        total_csr_points=("points_earned", "sum"),
    )
    .reset_index()
)

# ---------- 3. Challenges: map challenge_participation -> department via employees ----------
challenges_with_dept = challenge_participation.merge(
    employees[["employee_id", "department_id"]], on="employee_id", how="left"
)
challenges_by_dept = (
    challenges_with_dept[challenges_with_dept["approval_status"] == "Approved"]
    .groupby("department_id")
    .agg(
        completed_challenges=("participation_id", "count"),
        total_xp_earned=("xp_awarded", "sum"),
    )
    .reset_index()
)

# ---------- 4. Merge everything into one department-level summary ----------
summary = departments[["department_id", "name"]].copy()
summary = summary.merge(carbon_by_dept, on="department_id", how="left")
summary = summary.merge(csr_by_dept, on="department_id", how="left")
summary = summary.merge(challenges_by_dept, on="department_id", how="left")
summary = summary.merge(
    department_scores[["department_id", "environmental_score", "social_score", "governance_score", "total_score"]],
    on="department_id", how="left"
)

# Fill missing values (departments with zero activity) with 0
fill_cols = ["total_co2e_kg", "approved_csr_count", "total_csr_points",
             "completed_challenges", "total_xp_earned"]
summary[fill_cols] = summary[fill_cols].fillna(0)

print(summary)

summary.to_csv("department_summary.csv", index=False)
print("\nSaved department_summary.csv")
