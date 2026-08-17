"""
Data Repository Access Layer
Encapsulates SQL queries and data transformations for the multi-year Tamil Nadu dataset (2020-2026).
"""

import pandas as pd
from typing import Dict, Any, List, Optional
from src.database.db_connection import get_db_connection
from src.database.seed_data import initialize_database

def get_all_districts_df(year: Optional[int] = None) -> pd.DataFrame:
    """
    Fetches Tamil Nadu district records from SQLite database.
    If year is provided, filters by that year (e.g. 2026). If None, fetches latest year (2026).
    If year is 'All', returns all 266 historical multi-year records (2020-2026).
    """
    initialize_database()
    with get_db_connection() as conn:
        if year == "All":
            df = pd.read_sql_query("SELECT * FROM districts_multiyear ORDER BY year DESC, freight_volume_million_tonnes DESC;", conn)
        elif year is not None:
            df = pd.read_sql_query("SELECT * FROM districts_multiyear WHERE year = ? ORDER BY freight_volume_million_tonnes DESC;", conn, params=(int(year),))
        else:
            # Default to latest year 2026
            df = pd.read_sql_query("SELECT * FROM districts_multiyear WHERE year = (SELECT MAX(year) FROM districts_multiyear) ORDER BY freight_volume_million_tonnes DESC;", conn)
    
    # Map legacy column aliases for seamless compatibility
    if not df.empty:
        df["freight_volume_mton"] = df["freight_volume_million_tonnes"]
        df["gdp_cr"] = df["gddp_cr"]
        df["population_lakhs"] = df["population"] / 100_000.0
        df["rail_score"] = df["railway_connectivity_score"]
        df["port_airport_dist_km"] = df["port_connectivity_score"]  # Connectivity score / indicator
        df["warehouse_sqft"] = df["warehouses"] * 50_000  # Approximated storage sq ft per warehouse unit
        df["current_budget_cr"] = df["recommended_budget_cr"]

    return df

def get_available_years() -> List[int]:
    """Returns sorted list of available dataset years [2020, 2021, 2022, 2023, 2024, 2025, 2026]."""
    initialize_database()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT year FROM districts_multiyear ORDER BY year ASC;")
        return [row[0] for row in cursor.fetchall()]

def get_district_timeseries(district_name: str) -> pd.DataFrame:
    """
    Fetches multi-year historical trend (2020-2026) for a specific district.
    """
    initialize_database()
    with get_db_connection() as conn:
        df = pd.read_sql_query(
            "SELECT * FROM districts_multiyear WHERE LOWER(district_name) = LOWER(?) ORDER BY year ASC;",
            conn, params=(district_name.strip(),)
        )
    return df

def get_state_kpis(year: int = 2026) -> Dict[str, Any]:
    """
    Computes state-wide high-level KPI metrics for Tamil Nadu for a specific year.
    """
    df = get_all_districts_df(year=year)
    return {
        "total_districts": int(len(df)),
        "total_freight_mton": float(df["freight_volume_million_tonnes"].sum()) if not df.empty else 0.0,
        "total_gdp_cr": float(df["gddp_cr"].sum()) if not df.empty else 0.0,
        "avg_road_density": float(df["road_density"].mean()) if not df.empty else 0.0,
        "avg_congestion": float(df["congestion_index"].mean()) if not df.empty else 0.0,
        "total_budget_cr": float(df["recommended_budget_cr"].sum()) if not df.empty else 0.0,
        "top_freight_district": str(df.iloc[0]["district_name"]) if len(df) > 0 else "N/A"
    }

def get_regional_summary(year: int = 2026) -> pd.DataFrame:
    """
    Groups and aggregates freight metrics by region for a given year.
    """
    df = get_all_districts_df(year=year)
    summary = df.groupby("region").agg(
        district_count=("district_id", "count"),
        total_freight_mton=("freight_volume_million_tonnes", "sum"),
        total_gdp_cr=("gddp_cr", "sum"),
        avg_congestion=("congestion_index", "mean"),
        total_budget_cr=("recommended_budget_cr", "sum")
    ).reset_index()
    return summary

def get_database_health() -> Dict[str, Any]:
    """
    Inspects SQLite DB status, tables, record counts, and file integrity.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            cursor.execute("SELECT COUNT(*) FROM districts_multiyear;")
            district_count = cursor.fetchone()[0]
            
            return {
                "status": "Healthy",
                "tables": tables,
                "district_count": district_count,
                "is_seeded": district_count >= 266
            }
    except Exception as e:
        return {
            "status": f"Error: {str(e)}",
            "tables": [],
            "district_count": 0,
            "is_seeded": False
        }
