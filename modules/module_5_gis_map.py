"""
Module 5: Tamil Nadu GIS Spatial Logistics Map
Independently runnable module for interactive spatial visualization of freight flows,
congestion chokepoint alerts, and infrastructure deficit scores across all 38 TN districts.
"""

import sys
import os
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium

# Ensure parent root is in Python path for standalone execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.config import apply_custom_css
from src.components.header import render_header
from src.database.repository import get_all_districts_df, get_available_years
from src.components.gis_map import create_tn_gis_map

def run_module_5(role: str = "Administrator"):
    """
    Executes Module 5 Tamil Nadu GIS Spatial Map UI & Workflows.
    """
    apply_custom_css()
    render_header(module_title="Module 5: Tamil Nadu GIS Map", role=role)

    st.markdown("### 🗺️ Tamil Nadu Interactive Spatial Freight & Infrastructure GIS")
    st.info("Explore geographical freight volume distributions, congestion chokepoint alerts, and district infrastructure deficit scores.")

    # Sidebar Filter Controls
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🗺️ GIS Map Controls")

    years = get_available_years()
    selected_year = st.sidebar.select_slider(
        "📅 Select Map Year (2020 - 2026):",
        options=years,
        value=max(years) if years else 2026,
        key="gis_year"
    )

    # Fetch Data for Selected Year
    raw_df = get_all_districts_df(year=selected_year)

    selected_region = st.sidebar.selectbox(
        "Filter Geographic Region:",
        options=["All Regions (State-wide)"] + sorted(list(raw_df["region"].unique())),
        key="gis_region"
    )

    active_layer = st.sidebar.radio(
        "Map Visual Layer:",
        options=["District Deficit Markers", "Freight Density Heatmap", "Congestion Chokepoints", "All Layers"],
        index=0,
        key="gis_layer"
    )

    color_by = st.sidebar.radio(
        "Color Circle Markers By:",
        options=["Infrastructure Deficit Score", "Congestion Index", "Freight Volume"],
        index=0,
        key="gis_color"
    )

    # Filter Data
    df = raw_df.copy()
    if selected_region != "All Regions (State-wide)":
        df = df[df["region"] == selected_region]

    # Map color_by string
    color_map = {
        "Infrastructure Deficit Score": "deficit",
        "Congestion Index": "congestion",
        "Freight Volume": "freight"
    }

    # Summary KPI Cards
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Mapped Districts</div>
            <div class="metric-value">{len(df)} / 38</div>
            <div class="metric-badge badge-blue">Year {selected_year}</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_col2:
        top_freight_row = df.sort_values(by="freight_volume_million_tonnes", ascending=False).iloc[0] if not df.empty else {}
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Top Freight Hub</div>
            <div class="metric-value" style="font-size: 1.2rem; color: #60A5FA;">{top_freight_row.get('district_name', 'N/A')}</div>
            <div class="metric-badge badge-green">{top_freight_row.get('freight_volume_million_tonnes', 0):.1f} M Tonnes</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_col3:
        max_cong_row = df.sort_values(by="congestion_index", ascending=False).iloc[0] if not df.empty else {}
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Max Congestion Hub</div>
            <div class="metric-value" style="font-size: 1.2rem; color: #EF4444;">{max_cong_row.get('district_name', 'N/A')}</div>
            <div class="metric-badge badge-red">Index: {max_cong_row.get('congestion_index', 0):.1f}</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_col4:
        avg_deficit = df["infrastructure_deficit_score"].mean() if not df.empty else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Regional Deficit</div>
            <div class="metric-value">{avg_deficit:.1f} / 100</div>
            <div class="metric-badge badge-amber">Deficit Index</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Map Display Layout
    map_col, legend_col = st.columns([3, 1])

    with map_col:
        st.markdown(f"#### 📍 Interactive Map Canvas ({selected_year}) — Click Markers for Details")
        folium_map = create_tn_gis_map(
            df=df,
            active_layer=active_layer,
            color_by=color_map[color_by]
        )
        st_data = st_folium(
            folium_map,
            width="100%",
            height=580,
            returned_objects=["last_clicked_marker"]
        )

    with legend_col:
        st.markdown("#### 🎨 Map Legend")
        
        st.markdown("**🔴 Deficit & Congestion Color Scale:**")
        st.markdown("🔴 **Red**: Critical Deficit (Score ≥ 75)")
        st.markdown("🟡 **Amber**: Moderate Deficit (Score 50 - 74)")
        st.markdown("🟢 **Green**: Optimal Infrastructure (Score < 50)")

        st.divider()

        st.markdown("**⭕ Circle Marker Radius:**")
        st.caption("Proportional to **Annual Freight Volume** (Million Tonnes). Larger circle = Higher cargo volume.")

        st.divider()

        st.markdown("**🛑 Alert Markers:**")
        st.caption("Highlights severe traffic bottleneck districts with **Congestion Index ≥ 20.0**.")

        if st_data and st_data.get("last_clicked_marker"):
            clicked = st_data["last_clicked_marker"]
            st.info(f"📍 Clicked GPS: `Lat: {clicked['lat']:.4f}, Lon: {clicked['lng']:.4f}`")

    st.divider()

    # District Spatial Data Table
    st.markdown(f"### 📋 Mapped District Spatial Metrics ({selected_year})")
    st.dataframe(
        df[[
            "district_name", "region", "freight_volume_million_tonnes",
            "road_density", "congestion_index", "infrastructure_deficit_score",
            "warehouses", "logistics_parks", "recommended_budget_cr"
        ]],
        column_config={
            "district_name": st.column_config.TextColumn("District Name"),
            "region": st.column_config.TextColumn("Region"),
            "freight_volume_million_tonnes": st.column_config.NumberColumn("Freight (M Tonnes)", format="%.2f"),
            "road_density": st.column_config.NumberColumn("Road Density", format="%.2f"),
            "congestion_index": st.column_config.NumberColumn("Congestion Index", format="%.1f"),
            "infrastructure_deficit_score": st.column_config.NumberColumn("Deficit Score", format="%.1f"),
            "warehouses": st.column_config.NumberColumn("Warehouses", format="%d"),
            "logistics_parks": st.column_config.NumberColumn("Logistics Parks", format="%d"),
            "recommended_budget_cr": st.column_config.NumberColumn("Rec. Budget (₹ Cr)", format="₹ %,d")
        },
        use_container_width=True,
        hide_index=True
    )

    # CSV Download Button
    csv_gis = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=f"📥 Export GIS Spatial Metrics for {selected_year} (CSV)",
        data=csv_gis,
        file_name=f"tn_gis_spatial_metrics_{selected_year}.csv",
        mime="text/csv"
    )

    st.success("✅ **Module 5 GIS Map Complete**: Interactive spatial visualization, heatmap layers, and district popups active.")

if __name__ == "__main__":
    st.set_page_config(
        page_title="FreightOpt - Module 5 GIS Map",
        page_icon="🗺️",
        layout="wide"
    )
    run_module_5()
