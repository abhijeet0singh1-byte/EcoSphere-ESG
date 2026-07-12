"""
EcoSphere - AI & Analytics REST API (Step 4)
-----------------------------------------------
Exposes the outputs of esg_engine.py (Step 3) as REST endpoints so the
frontend/dashboard team can fetch scores, trends, and recommendations
per department.

Run:
    uvicorn analytics_api:app --reload --port 8000

Then open http://127.0.0.1:8000/docs for interactive API docs (Swagger UI).
"""

from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI(title="EcoSphere Analytics API", version="1.0")

# Load once at startup - re-run esg_engine.py separately whenever underlying
# data changes, then restart this server to pick up fresh CSVs.
esg_scores = pd.read_csv("esg_scores.csv")
carbon_trends = pd.read_csv("carbon_trends.csv")
recommendations = pd.read_csv("recommendations.csv")


def get_dept_row(df: pd.DataFrame, department_id: int):
    row = df[df["department_id"] == department_id]
    if row.empty:
        raise HTTPException(status_code=404, detail=f"Department {department_id} not found")
    return row.iloc[0].to_dict()


@app.get("/")
def root():
    return {"message": "EcoSphere Analytics API is running. See /docs for endpoints."}


@app.get("/api/departments")
def list_departments():
    """Returns all department IDs and names - useful for populating dropdowns."""
    return esg_scores[["department_id", "name"]].to_dict(orient="records")


@app.get("/api/department/{department_id}/esg-score")
def get_esg_score(department_id: int):
    """Returns computed Environmental/Social/Governance/Total ESG scores for one department."""
    return get_dept_row(esg_scores, department_id)


@app.get("/api/department/{department_id}/carbon-trend")
def get_carbon_trend(department_id: int):
    """Returns the predicted next-month CO2e and trend direction for one department."""
    return get_dept_row(carbon_trends, department_id)


@app.get("/api/department/{department_id}/recommendations")
def get_recommendations(department_id: int):
    """Returns the weakest ESG area and a suggested action for one department."""
    return get_dept_row(recommendations, department_id)


@app.get("/api/department/{department_id}/full-report")
def get_full_report(department_id: int):
    """Convenience endpoint: combines score + trend + recommendation in one call
    (handy for a single dashboard card that shows everything about a department)."""
    return {
        "esg_score": get_dept_row(esg_scores, department_id),
        "carbon_trend": get_dept_row(carbon_trends, department_id),
        "recommendation": get_dept_row(recommendations, department_id),
    }
