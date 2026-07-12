import pandas as pd

DATA_DIR = "ecosphere_seed_data"

carbon_transactions = pd.read_csv(f"{DATA_DIR}/carbon_transactions.csv")
carbon_transactions["date"] = pd.to_datetime(carbon_transactions["date"])
carbon_transactions["month"] = carbon_transactions["date"].dt.to_period("M").astype(str)

monthly_carbon = (
    carbon_transactions.groupby(["department_id", "month"])["co2e_emitted_kg"]
    .sum()
    .reset_index()
    .sort_values(["department_id", "month"])
)

print(monthly_carbon)
monthly_carbon.to_csv("carbon_monthly.csv", index=False)
print("\nSaved carbon_monthly.csv")
