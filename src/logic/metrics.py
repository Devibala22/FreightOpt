"""
Logistics Analytics & Business Metrics Engine
Computes analytical indicators, regional aggregations, and district rankings for official TN dataset.
"""

import pandas as pd
from typing import Dict, Any
from src.database.repository import get_all_districts_df

def compute_dashboard_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes summary KPIs from a filtered or full Tamil Nadu district DataFrame.
    """
    if df.empty:
        return {
            "total_districts": 0,
            "total_freight_mton": 0.0,
            "total_gdp_cr": 0.0,
            "avg_road_density": 0.0,
            "avg_congestion": 0.0,
            "top_freight_district": "N/A",
            "high_congestion_count": 0
        }

    freight_col = "freight_volume_million_tonnes" if "freight_volume_million_tonnes" in df.columns else "freight_volume_mton"
    gdp_col = "gddp_cr" if "gddp_cr" in df.columns else "gdp_cr"

    high_congestion = len(df[df["congestion_index"] >= 20.0])  # Adjust threshold for dataset scale
    top_district = df.sort_values(by=freight_col, ascending=False).iloc[0]["district_name"]

    return {
        "total_districts": int(len(df)),
        "total_freight_mton": float(df[freight_col].sum()),
        "total_gdp_cr": float(df[gdp_col].sum()),
        "avg_road_density": float(df["road_density"].mean()),
        "avg_congestion": float(df["congestion_index"].mean()),
        "top_freight_district": str(top_district),
        "high_congestion_count": int(high_congestion)
    }

def get_regional_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates freight volume, GDP, warehouses, and logistics parks by region.
    """
    if df.empty:
        return pd.DataFrame()

    freight_col = "freight_volume_million_tonnes" if "freight_volume_million_tonnes" in df.columns else "freight_volume_mton"
    gdp_col = "gddp_cr" if "gddp_cr" in df.columns else "gdp_cr"
    wh_col = "warehouses" if "warehouses" in df.columns else "warehouse_sqft"
    lp_col = "logistics_parks" if "logistics_parks" in df.columns else "district_id"
    budget_col = "recommended_budget_cr" if "recommended_budget_cr" in df.columns else "current_budget_cr"

    aggregated = df.groupby("region").agg(
        district_count=("district_name", "count"),
        total_freight_mton=(freight_col, "sum"),
        total_gdp_cr=(gdp_col, "sum"),
        avg_congestion=("congestion_index", "mean"),
        total_warehouses=(wh_col, "sum"),
        total_logistics_parks=(lp_col, "sum" if lp_col == "logistics_parks" else "count"),
        total_budget_cr=(budget_col, "sum")
    ).reset_index()

    return aggregated.sort_values(by="total_freight_mton", ascending=False)
