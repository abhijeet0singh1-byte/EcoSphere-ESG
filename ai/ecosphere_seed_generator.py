"""
EcoSphere - Synthetic Seed Data Generator
------------------------------------------
Generates realistic seed CSVs for every core entity in the EcoSphere ESG
platform: Departments, Categories, Emission Factors (real EPA-based values),
Employees, Environmental Goals, ESG Policies, Badges, Rewards, Carbon
Transactions, CSR Activities + Participation, Challenges + Participation,
Policy Acknowledgements, Audits, Compliance Issues, Department Scores.

Run:  python ecosphere_seed_generator.py
Output: ./ecosphere_seed_data/*.csv
"""

import random
from datetime import datetime, timedelta
import pandas as pd
from faker import Faker

fake = Faker()
Faker.seed(7)
random.seed(7)

OUT_DIR = "ecosphere_seed_data"
import os
os.makedirs(OUT_DIR, exist_ok=True)

NOW = datetime(2026, 7, 12)

# ---------- 1. Departments ----------
DEPT_NAMES = ["Engineering", "Human Resources", "Finance", "Operations",
              "Facilities", "Sales", "Marketing", "Procurement"]
departments = []
for i, name in enumerate(DEPT_NAMES, start=1):
    departments.append({
        "department_id": i,
        "name": name,
        "code": name[:3].upper(),
        "head_employee_id": None,  # filled after employees generated
        "parent_department_id": None if i <= 3 else random.randint(1, 3),
        "employee_count": random.randint(8, 40),
        "status": "Active",
    })
df_departments = pd.DataFrame(departments)

# ---------- 2. Categories (shared: CSR Activity / Challenge) ----------
csr_categories = ["Tree Plantation", "Blood Donation", "Community Cleanup", "Food Drive", "Education Outreach"]
challenge_categories = ["Energy Saving", "Waste Reduction", "Commute Green", "Water Conservation"]
categories = []
cid = 1
for name in csr_categories:
    categories.append({"category_id": cid, "name": name, "type": "CSR Activity", "status": "Active"})
    cid += 1
for name in challenge_categories:
    categories.append({"category_id": cid, "name": name, "type": "Challenge", "status": "Active"})
    cid += 1
df_categories = pd.DataFrame(categories)

# ---------- 3. Emission Factors (real-world reference values, EPA/DEFRA style) ----------
# Source: EPA GHG Emission Factors Hub (https://www.epa.gov/climateleadership/ghg-emission-factors-hub)
emission_factors = [
    {"factor_id": 1, "activity_type": "Diesel Fuel Combustion", "unit": "liter", "co2e_factor_kg_per_unit": 2.68, "source": "EPA GHG Emission Factors Hub"},
    {"factor_id": 2, "activity_type": "Petrol/Gasoline Combustion", "unit": "liter", "co2e_factor_kg_per_unit": 2.31, "source": "EPA GHG Emission Factors Hub"},
    {"factor_id": 3, "activity_type": "Purchased Electricity (Grid Avg)", "unit": "kWh", "co2e_factor_kg_per_unit": 0.42, "source": "EPA eGRID"},
    {"factor_id": 4, "activity_type": "Natural Gas Combustion", "unit": "therm", "co2e_factor_kg_per_unit": 5.31, "source": "EPA GHG Emission Factors Hub"},
    {"factor_id": 5, "activity_type": "Air Travel - Short Haul", "unit": "passenger_km", "co2e_factor_kg_per_unit": 0.15, "source": "DEFRA Conversion Factors"},
    {"factor_id": 6, "activity_type": "Air Travel - Long Haul", "unit": "passenger_km", "co2e_factor_kg_per_unit": 0.11, "source": "DEFRA Conversion Factors"},
    {"factor_id": 7, "activity_type": "Road Freight - Truck", "unit": "tonne_km", "co2e_factor_kg_per_unit": 0.10, "source": "EPA Scope 3 Guidance"},
    {"factor_id": 8, "activity_type": "Paper Consumption", "unit": "kg", "co2e_factor_kg_per_unit": 0.94, "source": "EPA WARM Model"},
    {"factor_id": 9, "activity_type": "Waste to Landfill", "unit": "kg", "co2e_factor_kg_per_unit": 0.58, "source": "EPA WARM Model"},
    {"factor_id": 10, "activity_type": "LPG Combustion", "unit": "liter", "co2e_factor_kg_per_unit": 1.51, "source": "EPA GHG Emission Factors Hub"},
]
df_emission_factors = pd.DataFrame(emission_factors)

# ---------- 4. Employees ----------
NUM_EMPLOYEES = 50
GENDERS = ["Male", "Female", "Non-binary", "Prefer not to say"]
ROLES = ["Employee", "Department Head", "ESG Admin", "Auditor"]
employees = []
for i in range(1, NUM_EMPLOYEES + 1):
    dept_id = random.randint(1, len(DEPT_NAMES))
    role = "ESG Admin" if i == 1 else ("Department Head" if i <= 6 else ("Auditor" if i <= 10 else "Employee"))
    employees.append({
        "employee_id": i,
        "name": fake.name(),
        "email": fake.unique.email(),
        "department_id": dept_id,
        "gender": random.choice(GENDERS),
        "role": role,
        "status": random.choices(["Active", "Inactive"], weights=[19, 1])[0],
        "xp_total": random.randint(0, 3000),
        "points_balance": random.randint(0, 1500),
    })
df_employees = pd.DataFrame(employees)

heads = df_employees[df_employees["role"] == "Department Head"]["employee_id"].tolist()
for idx, row in df_departments.iterrows():
    if heads:
        df_departments.at[idx, "head_employee_id"] = random.choice(heads)

# ---------- 5. Environmental Goals ----------
env_goals = []
metrics = ["Reduce Carbon Emissions", "Reduce Paper Usage", "Increase Renewable Energy Use", "Reduce Water Consumption"]
for i in range(1, 13):
    dept_id = random.randint(1, len(DEPT_NAMES))
    target = round(random.uniform(500, 5000), 1)
    current = round(target * random.uniform(0.3, 1.1), 1)
    env_goals.append({
        "goal_id": i,
        "department_id": dept_id,
        "metric": random.choice(metrics),
        "target_value": target,
        "current_value": current,
        "unit": "kg_co2e",
        "deadline": fake.date_between(start_date="+1M", end_date="+1y"),
        "status": "Achieved" if current >= target else "In Progress",
    })
df_env_goals = pd.DataFrame(env_goals)

# ---------- 6. ESG Policies ----------
policy_titles = ["Code of Conduct", "Anti-Bribery Policy", "Data Privacy Policy", "Environmental Compliance Policy",
                 "Workplace Safety Policy", "Diversity & Inclusion Policy", "Whistleblower Policy"]
esg_policies = []
for i, title in enumerate(policy_titles, start=1):
    esg_policies.append({
        "policy_id": i,
        "title": title,
        "description": fake.sentence(nb_words=12),
        "category": random.choice(["Governance", "Environmental", "Social"]),
        "effective_date": fake.date_between(start_date="-2y", end_date="-1M"),
        "status": "Active",
    })
df_policies = pd.DataFrame(esg_policies)

# ---------- 7. Badges ----------
badges = [
    {"badge_id": 1, "name": "Green Starter", "description": "Complete your first challenge", "unlock_rule": "completed_challenges >= 1", "icon": "seedling"},
    {"badge_id": 2, "name": "Eco Warrior", "description": "Earn 1000 XP", "unlock_rule": "xp_total >= 1000", "icon": "shield-leaf"},
    {"badge_id": 3, "name": "CSR Champion", "description": "Complete 5 CSR activities", "unlock_rule": "completed_csr_activities >= 5", "icon": "heart-hands"},
    {"badge_id": 4, "name": "Carbon Cutter", "description": "Earn 2500 XP", "unlock_rule": "xp_total >= 2500", "icon": "co2-cut"},
    {"badge_id": 5, "name": "Sustainability Legend", "description": "Complete 20 challenges", "unlock_rule": "completed_challenges >= 20", "icon": "trophy-green"},
]
df_badges = pd.DataFrame(badges)

# ---------- 8. Rewards ----------
rewards = [
    {"reward_id": 1, "name": "Reusable Water Bottle", "description": "Branded steel bottle", "points_required": 200, "stock": 50, "status": "Active"},
    {"reward_id": 2, "name": "Extra Day Off", "description": "One paid day off", "points_required": 1500, "stock": 20, "status": "Active"},
    {"reward_id": 3, "name": "Plant a Tree (in your name)", "description": "A tree planted via partner NGO", "points_required": 300, "stock": 100, "status": "Active"},
    {"reward_id": 4, "name": "E-Bike Voucher", "description": "Discount voucher for e-bike purchase", "points_required": 2000, "stock": 10, "status": "Active"},
    {"reward_id": 5, "name": "Company Merchandise Kit", "description": "T-shirt, mug, tote bag", "points_required": 500, "stock": 30, "status": "Active"},
]
df_rewards = pd.DataFrame(rewards)

# ---------- 9. Carbon Transactions ----------
SOURCE_TYPES = ["Purchase", "Manufacturing", "Expense", "Fleet"]
carbon_transactions = []
for i in range(1, 101):
    factor = df_emission_factors.sample(1).iloc[0]
    qty = round(random.uniform(10, 500), 2)
    carbon_transactions.append({
        "transaction_id": i,
        "department_id": random.randint(1, len(DEPT_NAMES)),
        "source_type": random.choice(SOURCE_TYPES),
        "emission_factor_id": factor["factor_id"],
        "quantity": qty,
        "unit": factor["unit"],
        "co2e_emitted_kg": round(qty * factor["co2e_factor_kg_per_unit"], 2),
        "date": fake.date_between(start_date="-6M", end_date="today"),
        "auto_calculated": random.choice([True, False]),
    })
df_carbon_transactions = pd.DataFrame(carbon_transactions)

# ---------- 10. CSR Activities + Participation ----------
csr_cat_ids = df_categories[df_categories["type"] == "CSR Activity"]["category_id"].tolist()
csr_activities = []
for i in range(1, 16):
    csr_activities.append({
        "activity_id": i,
        "title": fake.catch_phrase(),
        "category_id": random.choice(csr_cat_ids),
        "description": fake.sentence(nb_words=10),
        "date": fake.date_between(start_date="-3M", end_date="+1M"),
        "status": random.choice(["Planned", "Completed", "Cancelled"]),
    })
df_csr_activities = pd.DataFrame(csr_activities)

emp_participation = []
for i in range(1, 61):
    emp = df_employees.sample(1).iloc[0]
    activity = df_csr_activities.sample(1).iloc[0]
    approval = random.choices(["Pending", "Approved", "Rejected"], weights=[2, 7, 1])[0]
    emp_participation.append({
        "participation_id": i,
        "employee_id": emp["employee_id"],
        "activity_id": activity["activity_id"],
        "proof_attached": approval != "Pending" or random.random() < 0.5,
        "approval_status": approval,
        "points_earned": random.randint(20, 150) if approval == "Approved" else 0,
        "completion_date": fake.date_between(start_date="-3M", end_date="today") if approval == "Approved" else None,
    })
df_emp_participation = pd.DataFrame(emp_participation)

# ---------- 11. Challenges + Participation ----------
challenge_cat_ids = df_categories[df_categories["type"] == "Challenge"]["category_id"].tolist()
CHALLENGE_STATUSES = ["Draft", "Active", "Under Review", "Completed", "Archived"]
challenges = []
for i in range(1, 21):
    status = random.choice(CHALLENGE_STATUSES)
    deadline = fake.date_between(start_date="-1M", end_date="+2M")
    challenges.append({
        "challenge_id": i,
        "title": fake.bs().title(),
        "category_id": random.choice(challenge_cat_ids),
        "description": fake.sentence(nb_words=10),
        "xp": random.choice([50, 100, 150, 250, 500]),
        "difficulty": random.choice(["Easy", "Medium", "Hard"]),
        "evidence_required": random.choice([True, False]),
        "deadline": deadline,
        "status": status,
    })
df_challenges = pd.DataFrame(challenges)

challenge_participation = []
for i in range(1, 71):
    challenge = df_challenges.sample(1).iloc[0]
    emp = df_employees.sample(1).iloc[0]
    approval = random.choices(["Pending", "Approved", "Rejected"], weights=[2, 7, 1])[0]
    progress = 100 if approval == "Approved" else random.randint(0, 90)
    challenge_participation.append({
        "participation_id": i,
        "challenge_id": challenge["challenge_id"],
        "employee_id": emp["employee_id"],
        "progress_percent": progress,
        "proof_attached": challenge["evidence_required"] and approval != "Pending",
        "approval_status": approval,
        "xp_awarded": challenge["xp"] if approval == "Approved" else 0,
    })
df_challenge_participation = pd.DataFrame(challenge_participation)

# ---------- 12. Policy Acknowledgements ----------
policy_acks = []
ack_id = 1
for _, emp in df_employees.iterrows():
    for _, policy in df_policies.sample(random.randint(1, len(df_policies))).iterrows():
        policy_acks.append({
            "ack_id": ack_id,
            "employee_id": emp["employee_id"],
            "policy_id": policy["policy_id"],
            "acknowledged_date": fake.date_between(start_date="-1y", end_date="today"),
        })
        ack_id += 1
df_policy_acks = pd.DataFrame(policy_acks)

# ---------- 13. Audits + Compliance Issues ----------
audits = []
compliance_issues = []
issue_id = 1
for i in range(1, 9):
    dept_id = random.randint(1, len(DEPT_NAMES))
    audit_date = fake.date_between(start_date="-6M", end_date="-1M")
    status = "Completed" if i <= 5 else random.choice(["Scheduled", "In Progress", "Completed"])
    audits.append({
        "audit_id": i,
        "department_id": dept_id,
        "auditor_employee_id": random.choice(df_employees[df_employees["role"] == "Auditor"]["employee_id"].tolist() or [1]),
        "date": audit_date,
        "status": status,
    })
    if status == "Completed" and random.random() < 0.8:
        for _ in range(random.randint(1, 3)):
            due_date = audit_date + timedelta(days=random.randint(10, 60))
            compliance_issues.append({
                "issue_id": issue_id,
                "audit_id": i,
                "severity": random.choice(["Low", "Medium", "High", "Critical"]),
                "description": fake.sentence(nb_words=10),
                "owner_employee_id": df_employees.sample(1).iloc[0]["employee_id"],
                "due_date": due_date,
                "status": "Overdue" if due_date < NOW.date() and random.random() < 0.4 else random.choice(["Open", "Resolved"]),
            })
            issue_id += 1
df_audits = pd.DataFrame(audits)
df_compliance_issues = pd.DataFrame(compliance_issues)

# ---------- 14. Department Scores ----------
dept_scores = []
for _, dept in df_departments.iterrows():
    env_score = round(random.uniform(50, 100), 1)
    social_score = round(random.uniform(50, 100), 1)
    gov_score = round(random.uniform(50, 100), 1)
    total = round(env_score * 0.4 + social_score * 0.3 + gov_score * 0.3, 1)
    dept_scores.append({
        "department_id": dept["department_id"],
        "environmental_score": env_score,
        "social_score": social_score,
        "governance_score": gov_score,
        "total_score": total,
        "period": "2026-Q2",
    })
df_dept_scores = pd.DataFrame(dept_scores)

# ---------- Write all CSVs ----------
tables = {
    "departments": df_departments,
    "categories": df_categories,
    "emission_factors": df_emission_factors,
    "employees": df_employees,
    "environmental_goals": df_env_goals,
    "esg_policies": df_policies,
    "badges": df_badges,
    "rewards": df_rewards,
    "carbon_transactions": df_carbon_transactions,
    "csr_activities": df_csr_activities,
    "employee_participation": df_emp_participation,
    "challenges": df_challenges,
    "challenge_participation": df_challenge_participation,
    "policy_acknowledgements": df_policy_acks,
    "audits": df_audits,
    "compliance_issues": df_compliance_issues,
    "department_scores": df_dept_scores,
}

for name, df in tables.items():
    df.to_csv(f"{OUT_DIR}/{name}.csv", index=False)
    print(f"Wrote {OUT_DIR}/{name}.csv  ({len(df)} rows)")

print("\nDone. All EcoSphere seed CSVs generated in:", OUT_DIR)
