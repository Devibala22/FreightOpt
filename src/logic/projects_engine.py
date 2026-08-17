"""
Projects Business & Analytics Logic Engine
Computes project portfolio KPIs, ROI efficiency metrics, and validation rules.
"""

import pandas as pd
from typing import Dict, Any

def compute_project_summary_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculates summary KPIs for the infrastructure project proposals portfolio.
    """
    if df.empty:
        return {
            "total_projects": 0,
            "total_investment_cr": 0.0,
            "avg_roi_multiplier": 0.0,
            "approved_count": 0,
            "under_review_count": 0,
            "proposed_count": 0
        }

    return {
        "total_projects": int(len(df)),
        "total_investment_cr": float(df["cost_estimate_cr"].sum()),
        "avg_roi_multiplier": float(df["expected_roi_multiplier"].mean()),
        "approved_count": int(len(df[df["status"] == "Approved"])),
        "under_review_count": int(len(df[df["status"] == "Under Review"])),
        "proposed_count": int(len(df[df["status"] == "Proposed"]))
    }

def calculate_roi_score(cost_cr: float, roi_multiplier: float, deficit_score: float = 85.0) -> float:
    """
    Calculates a composite project priority score based on Cost, ROI, and District Deficit.
    """
    if cost_cr <= 0:
        return 0.0
    
    # Higher ROI and Higher Deficit increase score; Cost balances the scale
    base_score = (roi_multiplier * 30.0) + (deficit_score * 0.5) - (cost_cr * 0.02)
    return max(10.0, min(100.0, round(base_score, 1)))
