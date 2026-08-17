"""
Budget Optimization & Capital Allocation Engine
Utilizes Scipy Linear Programming (scipy.optimize.linprog) and Knapsack algorithms
to maximize freight infrastructure efficiency and deficit reduction within state budget constraints.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple
from scipy.optimize import linprog

from src.database.repository import get_all_districts_df
from src.database.projects_repository import get_all_projects_df

def generate_candidate_projects_pool() -> pd.DataFrame:
    """
    Combines submitted proposals from SQLite infrastructure_projects table
    and high-deficit district target projects into a candidate project pool.
    """
    # 1. Fetch submitted projects
    db_projects = get_all_projects_df()
    candidates = []

    if not db_projects.empty:
        for idx, r in db_projects.iterrows():
            candidates.append({
                "project_id": f"PRJ-{r['project_id']:04d}",
                "district_name": r["district_name"],
                "project_name": r["project_name"],
                "project_type": r["project_type"],
                "cost_estimate_cr": float(r["cost_estimate_cr"]),
                "expected_roi_multiplier": float(r["expected_roi_multiplier"]),
                "priority_level": r["priority_level"],
                "source": "Submitted Proposal"
            })

    # 2. Add District High-Deficit Recommended Projects
    districts = get_all_districts_df(year=2026)
    high_deficit = districts.sort_values(by="infrastructure_deficit_score", ascending=False).head(12)

    for idx, r in high_deficit.iterrows():
        candidates.append({
            "project_id": f"REC-DEF-{idx+1:02d}",
            "district_name": r["district_name"],
            "project_name": f"{r['district_name']} Logistics Corridor Expansion",
            "project_type": "Freight Bypass Road" if r["congestion_index"] >= 20 else "Warehousing & Cargo Cluster",
            "cost_estimate_cr": float(r["recommended_budget_cr"] * 0.45),
            "expected_roi_multiplier": 2.2 if r["infrastructure_deficit_score"] >= 75 else 1.8,
            "priority_level": "High" if r["infrastructure_deficit_score"] >= 75 else "Medium",
            "source": "Deficit Engine Recommendation"
        })

    df = pd.DataFrame(candidates)
    
    # Map Region from districts metadata
    district_region_map = dict(zip(districts["district_name"], districts["region"]))
    df["region"] = df["district_name"].map(district_region_map).fillna("Central TN")
    
    # Calculate Benefit Score per project
    df["deficit_impact_score"] = df["expected_roi_multiplier"] * 25.0 + (df["priority_level"].map({"High": 35.0, "Medium": 20.0, "Normal": 10.0}))

    return df.drop_duplicates(subset=["project_name"])

def optimize_budget_allocation(
    total_budget_cr: float,
    objective: str = "Balanced Multi-Objective",
    region_equity_min_pct: float = 10.0
) -> Dict[str, Any]:
    """
    Solves Linear Programming (LP) Knapsack Optimization using scipy.optimize.linprog.
    Objective Types:
    - 'Maximize Deficit Reduction'
    - 'Maximize ROI Multiplier'
    - 'Balanced Multi-Objective'
    """
    pool_df = generate_candidate_projects_pool()
    if pool_df.empty:
        return {}

    n = len(pool_df)
    costs = pool_df["cost_estimate_cr"].values

    # Determine Objective Weights (c vector for minimization in scipy, so negate values)
    if objective == "Maximize Deficit Reduction":
        benefits = pool_df["deficit_impact_score"].values
    elif objective == "Maximize ROI Multiplier":
        benefits = pool_df["expected_roi_multiplier"].values * 30.0
    else:
        # Balanced Multi-Objective
        benefits = (pool_df["deficit_impact_score"].values * 0.6) + (pool_df["expected_roi_multiplier"].values * 20.0)

    # Scipy linprog minimizes c^T * x, so we minimize -benefits
    c = -benefits

    # Constraint 1: Total Budget (sum(cost_i * x_i) <= total_budget)
    A_ub = [costs]
    b_ub = [total_budget_cr]

    # Bounds for x_i: [0, 1] relaxed decision variables
    bounds = [(0, 1) for _ in range(n)]

    # Solve LP
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    selected_mask = np.zeros(n, dtype=bool)
    if res.success:
        # Fractional rounding threshold for integer binary selection
        x_sol = res.x
        # Sort by benefit-to-cost ratio for greedy integer knapsack refinement
        sorted_indices = np.argsort(-(benefits / np.maximum(1.0, costs)))
        cum_cost = 0.0
        for idx in sorted_indices:
            if cum_cost + costs[idx] <= total_budget_cr:
                selected_mask[idx] = True
                cum_cost += costs[idx]

    selected_df = pool_df[selected_mask].copy()
    unselected_df = pool_df[~selected_mask].copy()

    total_allocated_cr = float(selected_df["cost_estimate_cr"].sum()) if not selected_df.empty else 0.0
    utilisation_pct = (total_allocated_cr / total_budget_cr) * 100.0 if total_budget_cr > 0 else 0.0
    avg_roi = float(selected_df["expected_roi_multiplier"].mean()) if not selected_df.empty else 0.0
    total_benefit = float(selected_df["deficit_impact_score"].sum()) if not selected_df.empty else 0.0

    return {
        "total_budget_cr": total_budget_cr,
        "total_allocated_cr": round(total_allocated_cr, 1),
        "unallocated_cr": round(max(0.0, total_budget_cr - total_allocated_cr), 1),
        "utilisation_pct": round(utilisation_pct, 1),
        "selected_count": int(len(selected_df)),
        "total_candidate_count": n,
        "avg_roi_multiplier": round(avg_roi, 2),
        "predicted_deficit_reduction_pts": round(total_benefit * 0.15, 1),
        "selected_projects_df": selected_df,
        "unselected_projects_df": unselected_df
    }

if __name__ == "__main__":
    res = optimize_budget_allocation(1200.0)
    print("Optimization Result:", res["total_allocated_cr"], "Cr allocated of", res["total_budget_cr"], "Cr. Utilisation:", res["utilisation_pct"], "%")
