"""
Folium GIS Map Component for Tamil Nadu Spatial Logistics Visualization
Provides multi-layer interactive map with Freight Heatmaps, Congestion Alerts,
and District Infrastructure Deficit Circle Markers.
"""

import folium
from folium.plugins import HeatMap
import pandas as pd
from typing import Optional
from src.logic.gis_engine import (
    get_district_coordinates,
    get_color_for_metric,
    build_district_popup_html
)

# Centroid of Tamil Nadu
TN_CENTER_LAT = 11.1271
TN_CENTER_LON = 78.6569
DEFAULT_ZOOM = 7

def create_tn_gis_map(
    df: pd.DataFrame,
    active_layer: str = "Freight Deficit Heatmap",
    color_by: str = "deficit"
) -> folium.Map:
    """
    Renders an interactive Folium map displaying Tamil Nadu district logistics metrics.
    """
    # Create Folium Base Map with Dark Tile
    m = folium.Map(
        location=[TN_CENTER_LAT, TN_CENTER_LON],
        zoom_start=DEFAULT_ZOOM,
        tiles="CartoDB dark_matter",
        width="100%",
        height="600px"
    )

    if df.empty:
        return m

    # 1. FREIGHT DENSITY HEATMAP LAYER
    if active_layer in ["Freight Density Heatmap", "All Layers"]:
        heat_data = []
        for _, row in df.iterrows():
            lat, lon = get_district_coordinates(row["district_name"])
            freight = row.get("freight_volume_million_tonnes", 10.0)
            heat_data.append([lat, lon, freight])
        
        HeatMap(
            heat_data,
            name="Freight Volume Density",
            radius=25,
            blur=15,
            max_zoom=10,
            gradient={0.2: 'blue', 0.5: 'lime', 0.8: 'yellow', 1.0: 'red'}
        ).add_to(m)

    # 2. CONGESTION CHOKEPOINT ALERTS LAYER
    if active_layer in ["Congestion Chokepoints", "All Layers"]:
        choke_df = df[df["congestion_index"] >= 20.0]
        for _, row in choke_df.iterrows():
            lat, lon = get_district_coordinates(row["district_name"])
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(build_district_popup_html(row.to_dict()), max_width=300),
                tooltip=f"🛑 CONGESTION ALERT: {row['district_name']} (Index: {row['congestion_index']:.1f})",
                icon=folium.Icon(color="red", icon="exclamation-triangle", prefix="fa")
            ).add_to(m)

    # 3. DISTRICT CIRCLE MARKERS LAYER (Default)
    for _, row in df.iterrows():
        name = row["district_name"]
        lat, lon = get_district_coordinates(name)
        
        # Scaling marker radius by Freight Volume
        freight_vol = row.get("freight_volume_million_tonnes", 10.0)
        radius = max(6.0, min(30.0, freight_vol * 0.45))
        
        val_for_color = row.get("infrastructure_deficit_score", 50.0) if color_by == "deficit" else row.get("congestion_index", 15.0)
        color = get_color_for_metric(val_for_color, metric_type=color_by)

        popup_html = build_district_popup_html(row.to_dict())

        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.75,
            weight=2,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"📍 {name} | Freight: {freight_vol:.1f} M Tonnes | Deficit: {row.get('infrastructure_deficit_score', 0):.1f}"
        ).add_to(m)

    return m
