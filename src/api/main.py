"""
FastAPI REST Server Application for FreightOpt
Exposes RESTful JSON endpoints for Tamil Nadu logistics data, project proposals,
ML freight demand predictions, and Scipy linear programming budget optimization.
"""

from fastapi import FastAPI, HTTPException, Query, Body, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import os
import sys

# Ensure parent root is in Python path for repository access
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.database.repository import get_all_districts_df, get_district_timeseries, get_database_health
from src.database.projects_repository import get_all_projects_df, add_infrastructure_project
from src.logic.ml_prediction_engine import predict_district_freight_scenario
from src.logic.budget_optimizer import optimize_budget_allocation

app = FastAPI(
    title="FreightOpt REST API - Tamil Nadu Logistics Intelligence",
    description="Official API for Tamil Nadu Freight Demand Forecasting, Deficit Analytics, and Capital Budget Optimization.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for external portal integration (e.g. ULIP, State GIS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Request & Response Schemas ---
class ProjectProposalRequest(BaseModel):
    district_name: str = Field(..., example="Coimbatore")
    project_name: str = Field(..., example="Coimbatore Logistics Highway Bypass")
    project_type: str = Field(..., example="Freight Bypass Road")
    cost_estimate_cr: float = Field(..., example=320.0)
    expected_roi_multiplier: float = Field(..., example=2.4)
    implementation_year: int = Field(..., example=2025)
    priority_level: str = Field(..., example="High")
    description: Optional[str] = Field(None, example="6-lane heavy cargo corridor bypass.")
    submitted_by: str = Field(..., example="planner@tnlogistics.gov.in")

class PredictionRequest(BaseModel):
    district_name: str = Field(..., example="Chennai")
    target_year: int = Field(2028, example=2028)
    gddp_growth_pct: float = Field(6.5, example=6.5)
    industrial_growth_pct: float = Field(8.5, example=8.5)
    added_road_density: float = Field(0.5, example=0.5)
    added_warehouses: int = Field(2, example=2)

# --- REST Endpoints ---

@app.get("/api/v1/health", summary="Get System & Database Health Status")
def get_health():
    """Returns database connection health, total district records, and server status."""
    db_health = get_database_health()
    return {
        "status": "online",
        "system": "FreightOpt REST API v1.0",
        "database": db_health,
        "region_coverage": "38 Tamil Nadu Districts"
    }

@app.get("/api/v1/districts", summary="Get All 38 District Logistics Metrics")
def get_districts(year: Optional[int] = Query(2026, description="Dataset year (2020 - 2026)")):
    """Returns JSON array of district freight volume, GDDP, road density, and deficit scores."""
    df = get_all_districts_df(year=year)
    if df.empty:
        raise HTTPException(status_code=404, detail=f"No dataset found for year {year}")
    return df.to_dict(orient="records")

@app.get("/api/v1/districts/{district_name}", summary="Get Specific District Multi-Year Timeseries")
def get_district_by_name(district_name: str):
    """Returns historical multi-year records (2020-2026) for a specific district."""
    df = get_district_timeseries(district_name)
    if df.empty:
        raise HTTPException(status_code=404, detail=f"District '{district_name}' not found")
    return df.to_dict(orient="records")

@app.get("/api/v1/projects", summary="Get Infrastructure Projects Registry")
def get_projects(status: Optional[str] = Query(None, description="Filter status (Approved, Under Review, Proposed)")):
    """Returns list of submitted and approved infrastructure project proposals."""
    df = get_all_projects_df(status_filter=status)
    return df.to_dict(orient="records")

@app.post("/api/v1/projects", summary="Submit New Project Proposal via API", status_code=201)
def create_project(payload: ProjectProposalRequest):
    """Ingests a new project proposal into SQLite database."""
    try:
        project_dict = payload.dict()
        project_id = add_infrastructure_project(project_dict)
        return {
            "message": "Project proposal submitted successfully",
            "project_id": f"PRJ-TN-{project_id:04d}",
            "district_name": payload.district_name,
            "status": "Proposed"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/predict", summary="Run ML Freight Demand Forecast Scenario")
def predict_freight(payload: PredictionRequest):
    """Runs trained Scikit-Learn Machine Learning model (R2 = 98.7%) to forecast future freight demand."""
    df = get_all_districts_df(year=2026)
    match = df[df["district_name"].str.lower() == payload.district_name.lower()]
    if match.empty:
        raise HTTPException(status_code=404, detail=f"District '{payload.district_name}' not found.")
    
    district_row = match.iloc[0]
    res = predict_district_freight_scenario(
        district_row=district_row,
        target_year=payload.target_year,
        gddp_growth_pct=payload.gddp_growth_pct,
        industrial_growth_pct=payload.industrial_growth_pct,
        added_road_density=payload.added_road_density,
        added_warehouses=payload.added_warehouses
    )
    return res

@app.get("/api/v1/optimize", summary="Execute Scipy Linear Programming Budget Optimization")
def optimize_budget(
    total_budget_cr: float = Query(1500.0, description="Available State Budget in Rs. Crore"),
    objective: str = Query("Balanced Multi-Objective", description="Optimization Target Objective")
):
    """Solves Linear Programming Knapsack Capital Allocation for given state budget limit."""
    res = optimize_budget_allocation(total_budget_cr=total_budget_cr, objective=objective)
    # Convert DataFrames to JSON dicts
    if "selected_projects_df" in res:
        res["selected_projects"] = res.pop("selected_projects_df").to_dict(orient="records")
    if "unselected_projects_df" in res:
        res["unselected_projects"] = res.pop("unselected_projects_df").to_dict(orient="records")
    return res
