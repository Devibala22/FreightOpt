"""
Logistics Infrastructure Deficit Scoring & Simulation Engine
Computes multi-pillar deficit scores (0-100), state benchmarks, high-vulnerability alerts,
and interactive deficit reduction simulation metrics.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple

def compute_state_benchmarks(df: pd.DataFrame) -> Dict[str, float]:
    """
    Computes baseline state-wide averages for key infrastructure indicators.
    """
    if df.empty:
        return {
            "avg_road_density": 2.0,
            "avg_congestion": 20.0,
            "avg_freight": 20.0,
            "avg_warehouses": 15.0,
            "avg_rail_score": 5.0,
            "avg_port_score": 5.0
        }

    return {
        "avg_road_density": float(df["road_density"].mean()),
        "avg_congestion": float(df["congestion_index"].mean()),
        "avg_freight": float(df["freight_volume_million_tonnes"].mean()),
        "avg_warehouses": float(df["warehouses"].mean()),
        "avg_rail_score": float(df["railway_connectivity_score"].mean()),
        "avg_port_score": float(df["port_connectivity_score"].mean())
    }

def calculate_multi_pillar_deficit(row: pd.Series, benchmarks: Dict[str, float]) -> Dict[str, float]:
    """
    Calculates sub-component pillar scores for a district:
    1. Road Density Gap Score (0 - 100)
    2. Congestion Bottleneck Score (0 - 100)
    3. Storage Capacity Gap Score (0 - 100)
    4. Connectivity Deficit Score (0 - 100)
    5. Composite Infrastructure Deficit Index (0 - 100)
    """
    # 1. Road Density Gap
    road_density = row.get("road_density", 2.0)
    bench_road = max(0.1, benchmarks["avg_road_density"])
    road_gap_score = max(0.0, min(100.0, ((bench_road - road_density) / bench_road) * 100.0 + 40.0))

    # 2. Congestion Bottleneck Severity
    congestion = row.get("congestion_index", 15.0)
    congestion_score = max(0.0, min(100.0, (congestion / 100.0) * 100.0))

    # 3. Storage Gap (Warehouses per M Tonnes of Freight)
    freight = max(0.1, row.get("freight_volume_million_tonnes", 10.0))
    wh = row.get("warehouses", 5)
    wh_ratio = wh / freight
    storage_gap_score = max(0.0, min(100.0, (1.0 - min(1.0, wh_ratio / 1.5)) * 100.0))

    # 4. Connectivity Gap (Rail + Port Scores: Max 20)
    rail = row.get("railway_connectivity_score", 5.0)
    port = row.get("port_connectivity_score", 5.0)
    conn_total = rail + port
    conn_gap_score = max(0.0, min(100.0, (1.0 - min(1.0, conn_total / 18.0)) * 100.0))

    # Composite Score (Weighted Average)
    composite_score = (
        (road_gap_score * 0.25) +
        (congestion_score * 0.35) +
        (storage_gap_score * 0.20) +
        (conn_gap_score * 0.20)
    )

    return {
        "road_gap_score": round(road_gap_score, 1),
        "congestion_score": round(congestion_score, 1),
        "storage_gap_score": round(storage_gap_score, 1),
        "conn_gap_score": round(conn_gap_score, 1),
        "composite_deficit_score": round(composite_score, 1)
    }

def get_deficit_tier(score: float) -> Tuple[str, str, str]:
    """
    Returns (Tier Name, Badge CSS Class, Hex Color).
    """
    if score >= 75.0:
        return ("Critical Deficit", "badge-red", "#EF4444")
    elif score >= 55.0:
        return ("High Deficit", "badge-amber", "#F59E0B")
    elif score >= 35.0:
        return ("Moderate Deficit", "badge-blue", "#3B82F6")
    else:
        return ("Low Deficit", "badge-green", "#10B981")

def simulate_deficit_reduction(
    current_density: float,
    current_wh: int,
    current_congestion: float,
    added_road_km: float,
    added_warehouses: int,
    area_sq_km: float = 4000.0
) -> Dict[str, Any]:
    """
    Simulates the impact of proposed infrastructure additions on district deficit scores.
    """
    # Calculate new road density
    new_density = current_density + (added_road_km / (area_sq_km / 100.0))
    new_wh = current_wh + added_warehouses
    
    # Estimated congestion reduction (adding road & warehouse capacity reduces congestion)
    congestion_reduction = (added_road_km * 0.12) + (added_warehouses * 0.8)
    new_congestion = max(5.0, current_congestion - congestion_reduction)

    # Simulated Deficit Reduction
    density_gain_impact = (new_density - current_density) * 12.0
    wh_gain_impact = added_warehouses * 2.5
    congestion_drop_impact = (current_congestion - new_congestion) * 1.5

    total_score_reduction = min(45.0, density_gain_impact + wh_gain_impact + congestion_drop_impact)

    return {
        "new_road_density": round(new_density, 2),
        "new_warehouses": new_wh,
        "new_congestion_index": round(new_congestion, 1),
        "score_reduction": round(total_score_reduction, 1)
    }
