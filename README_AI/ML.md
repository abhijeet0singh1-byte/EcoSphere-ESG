EcoSphere Analytics API - how to use it

1. Install: pip install fastapi uvicorn pandas
2. Run: uvicorn analytics_api:app --reload --port 8000
3. Base URL: http://127.0.0.1:8000

Endpoints:
- GET /api/departments                          -> list of all departments
- GET /api/department/{id}/esg-score            -> ESG scores for one department
- GET /api/department/{id}/carbon-trend         -> predicted next month CO2e + trend
- GET /api/department/{id}/recommendations      -> weakest area + suggestion
- GET /api/department/{id}/full-report          -> all three combined (recommended for dashboard cards)

Full interactive docs: http://127.0.0.1:8000/docs

Example: GET /api/department/3/full-report
{
  "esg_score": {...},
  "carbon_trend": {...},
  "recommendation": {...}
}