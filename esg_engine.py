"""
EcoSphere - AI & Analytics Engine (Step 3)
--------------------------------------------
Builds on department_summary.csv and carbon_monthly.csv (from Step 2) to produce:
  1. A recomputed ESG score per department (derived from real activity, not
     random placeholder numbers)
  2. A carbon emissions trend prediction per department (next month + direction)
  3. Rule-based sustainability recommendations per department

Run:  python esg_engine.py
Output: esg_scores.csv, carbon_trends.csv, recommendations.csv
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# ---------- Config: adjust these weights if your org wants different priorities ----------
WEIGHTS = {"environmental": 0.40, "social": 0.30, "governance": 0.30}

summary = pd.read_csv("department_summary.csv")
monthly_carbon = pd.read_csv("carbon_monthly.csv")


# ==========================================================
# 1. ESG SCORE ENGINE (computed from real data)
# ==========================================================
def min_max_scale(series, invert=False):
    """Scale a column to 0-100. invert=True means lower raw value -> higher score
    (used for emissions, where less is better)."""
    if series.max() == series.min():
        return pd.Series([100.0] * len(series), index=series.index)
    scaled = (series - series.min()) / (series.max() - series.min()) * 100
    return 100 - scaled if invert else scaled


summary["computed_environmental_score"] = min_max_scale(summary["total_co2e_kg"], invert=True).round(1)

# Social: blend CSR points and XP earned into one activity measure, then scale
summary["social_activity_raw"] = summary["total_csr_points"] + summary["total_xp_earned"]
summary["computed_social_score"] = min_max_scale(summary["social_activity_raw"]).round(1)

# Governance: no dedicated transactional dataset prepped yet -> reuse existing score.
# (Enhancement: derive this from compliance_issues.csv - open/overdue issue count.)
summary["computed_governance_score"] = summary["governance_score"]

summary["computed_total_score"] = (
    summary["computed_environmental_score"] * WEIGHTS["environmental"]
    + summary["computed_social_score"] * WEIGHTS["social"]
    + summary["computed_governance_score"] * WEIGHTS["governance"]
).round(1)

esg_scores = summary[[
    "department_id", "name",
    "computed_environmental_score", "computed_social_score",
    "computed_governance_score", "computed_total_score",
    "total_score",  # original placeholder score, kept for comparison
]].rename(columns={"total_score": "original_placeholder_score"})

esg_scores.to_csv("esg_scores.csv", index=False)
print("=== ESG Scores (computed vs. original) ===")
print(esg_scores.to_string(index=False))


# ==========================================================
# 2. CARBON TREND MODEL
# ==========================================================
trend_rows = []
for dept_id, group in monthly_carbon.groupby("department_id"):
    group = group.sort_values("month").reset_index(drop=True)
    dept_name = summary.loc[summary["department_id"] == dept_id, "name"].values[0]

    if len(group) < 2:
        trend_rows.append({
            "department_id": dept_id, "name": dept_name,
            "predicted_next_month_co2e": None, "trend": "Insufficient data",
        })
        continue

    # Turn months into a simple numeric time index (0, 1, 2, ...) for regression
    X = np.arange(len(group)).reshape(-1, 1)
    y = group["co2e_emitted_kg"].values

    model = LinearRegression()
    model.fit(X, y)

    next_index = np.array([[len(group)]])
    predicted_next = model.predict(next_index)[0]
    predicted_next = max(0, predicted_next)  # emissions can't be negative
    slope = model.coef_[0]

    if slope > 5:
        trend_label = "Increasing"
    elif slope < -5:
        trend_label = "Decreasing"
    else:
        trend_label = "Stable"

    trend_rows.append({
        "department_id": dept_id,
        "name": dept_name,
        "predicted_next_month_co2e": round(float(predicted_next), 2),
        "trend": trend_label,
    })

carbon_trends = pd.DataFrame(trend_rows)
carbon_trends.to_csv("carbon_trends.csv", index=False)
print("\n=== Carbon Trend Predictions ===")
print(carbon_trends.to_string(index=False))


# ==========================================================
# 3. RECOMMENDATION ENGINE (rule-based)
# ==========================================================
def recommend(row):
    scores = {
        "environmental": row["computed_environmental_score"],
        "social": row["computed_social_score"],
        "governance": row["computed_governance_score"],
    }
    weakest = min(scores, key=scores.get)

    messages = {
        "environmental": "Carbon output is high relative to other departments — consider switching a portion of fuel/electricity use to lower-emission sources or reviewing high-emission activities flagged in Carbon Transactions.",
        "social": "Employee participation in CSR activities and challenges is low — consider running a targeted challenge or CSR event to boost engagement and XP.",
        "governance": "Governance score is the weakest area — review open compliance issues and ensure policy acknowledgements are up to date.",
    }
    return weakest.capitalize(), messages[weakest]


recommendations = []
for _, row in esg_scores.iterrows():
    weakest_area, message = recommend(row)
    recommendations.append({
        "department_id": row["department_id"],
        "name": row["name"],
        "weakest_area": weakest_area,
        "recommendation": message,
    })

df_recommendations = pd.DataFrame(recommendations)
df_recommendations.to_csv("recommendations.csv", index=False)
print("\n=== Recommendations ===")
print(df_recommendations.to_string(index=False))

print("\nSaved: esg_scores.csv, carbon_trends.csv, recommendations.csv")
