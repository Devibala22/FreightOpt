"""
Module 3: Executive Overview Dashboard
Independently runnable module for high-level logistics infrastructure analytics,
multi-year KPI monitoring (2020-2026), regional breakdown, dynamic Plotly visual charts,
and district dataset exploration.
"""

import sys
import os
import streamlit as st
import pandas as pd

# Ensure parent root is in Python path for standalone execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.config import apply_custom_css
from src.components.header import render_header
from src.database.repository import get_all_districts_df, get_available_years
from src.logic.metrics import compute_dashboard_metrics, get_regional_breakdown
from src.components.charts import (
    render_top_districts_bar_chart,
    render_regional_freight_donut,
    render_congestion_density_scatter,
    render_warehouse_capacity_chart,
    render_multiyear_trend_chart
)

def run_module_3(role: str = "Administrator"):
    """
    Executes Module 3 Dashboard UI & Visual Analytics workflows.
    """
    apply_custom_css()
    render_header(module_title="Module 3: Dashboard", role=role)

    # 1. Role-Specific Executive Insight Banner
    if role == "Administrator":
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.7); border-left: 4px solid #34D399; padding: 12px 18px; border-radius: 8px; margin-bottom: 20px; font-size: 0.9rem;">
            👑 <strong>Administrator View</strong>: Monitoring state-wide freight trends, industrial growth, and infrastructure deficit scores across all 38 Tamil Nadu districts.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.7); border-left: 4px solid #3B82F6; padding: 12px 18px; border-radius: 8px; margin-bottom: 20px; font-size: 0.9rem;">
            📐 <strong>Decision Maker (Government Planner) View</strong>: Analyzing regional freight bottlenecks, road density deficits, and warehouse storage gaps to prioritize capital investments.
        </div>
        """, unsafe_allow_html=True)

    # Sidebar Year Slider Filter
    years = get_available_years()
    selected_year = st.sidebar.select_slider(
        "📅 Select Dataset Year (2020 - 2026):",
        options=years,
        value=max(years) if years else 2026
    )

    # Fetch Data
    raw_df = get_all_districts_df(year=selected_year)
    all_years_df = get_all_districts_df(year="All")

    # 2. Interactive Filter Controls
    f_col1, f_col2, f_col3 = st.columns([2, 3, 2])
    with f_col1:
        selected_region = st.selectbox(
            "Filter by Geographic Region:",
            options=["All Regions (State-wide)"] + sorted(list(raw_df["region"].unique()))
        )
    with f_col2:
        search_query = st.text_input("Search District:", placeholder="e.g. Chennai, Coimbatore, Madurai, Salem...")
    with f_col3:
        sort_by = st.selectbox(
            "Sort Ranking By:",
            options=["Freight Volume", "GDDP (₹ Cr)", "Industrial Output", "Road Density", "Congestion Index", "Deficit Score"]
        )

    # Apply Filter Logic
    df = raw_df.copy()
    if selected_region != "All Regions (State-wide)":
        df = df[df["region"] == selected_region]
    if search_query:
        df = df[df["district_name"].str.contains(search_query, case=False, na=False)]

    # Map Sort Keys
    sort_column_map = {
        "Freight Volume": "freight_volume_million_tonnes",
        "GDDP (₹ Cr)": "gddp_cr",
        "Industrial Output": "industrial_output_cr",
        "Road Density": "road_density",
        "Congestion Index": "congestion_index",
        "Deficit Score": "infrastructure_deficit_score"
    }
    df = df.sort_values(by=sort_column_map[sort_by], ascending=False)

    # Compute KPI Summaries
    kpis = compute_dashboard_metrics(df)
    regional_df = get_regional_breakdown(df)

    # 3. High-Level KPI Metric Cards
    st.markdown(f"### 📊 Executive Key Performance Indicators ({selected_year})")
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

    with kpi_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Districts Displayed</div>
            <div class="metric-value">{kpis['total_districts']} / 38</div>
            <div class="metric-badge badge-blue">Year {selected_year}</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Annual Freight</div>
            <div class="metric-value">{kpis['total_freight_mton']:.1f} M Tonnes</div>
            <div class="metric-badge badge-green">State Cargo</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total GDDP</div>
            <div class="metric-value">₹ {kpis['total_gdp_cr']:,.0f} Cr</div>
            <div class="metric-badge badge-blue">Economic Base</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Congestion Index</div>
            <div class="metric-value">{kpis['avg_congestion']:.1f}</div>
            <div class="metric-badge badge-amber">Traffic Pressure</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">High Congestion Hubs</div>
            <div class="metric-value">{kpis['high_congestion_count']} Districts</div>
            <div class="metric-badge badge-red">Index ≥ 20.0</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # 4. Redesigned Plotly Visual Analytics Grid
    st.markdown("### 📈 Visual Analytics & Infrastructure Overview")

    # ROW 1 CHARTS
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        top_bar_fig = render_top_districts_bar_chart(df, n=10)
        st.plotly_chart(top_bar_fig, use_container_width=True)

    with chart_col2:
        donut_fig = render_regional_freight_donut(regional_df)
        st.plotly_chart(donut_fig, use_container_width=True)

    # ROW 2 CHARTS
    chart_col3, chart_col4 = st.columns(2)
    with chart_col3:
        scatter_fig = render_congestion_density_scatter(df)
        st.plotly_chart(scatter_fig, use_container_width=True)

    with chart_col4:
        wh_fig = render_warehouse_capacity_chart(regional_df)
        st.plotly_chart(wh_fig, use_container_width=True)

    # ROW 3 MULTI-YEAR TREND CHART
    st.markdown("### 📈 Multi-Year Freight Trajectory (2020 – 2026)")
    trend_fig = render_multiyear_trend_chart(all_years_df)
    st.plotly_chart(trend_fig, use_container_width=True)

    st.divider()

    # 5. Tamil Nadu Official Dataset Explorer Table
    st.markdown(f"### 📋 Tamil Nadu Official Multi-Year Dataset ({selected_year})")
    st.write(f"Displaying **{len(df)}** district records for Year **{selected_year}**.")

    st.dataframe(
        df[[
            "district_id", "district_name", "year", "region", "population", "gddp_cr",
            "industrial_output_cr", "number_of_industries", "road_length_km", "road_density",
            "freight_volume_million_tonnes", "warehouses", "logistics_parks",
            "railway_connectivity_score", "port_connectivity_score", "congestion_index",
            "infrastructure_deficit_score", "recommended_budget_cr"
        ]],
        column_config={
            "district_id": st.column_config.TextColumn("ID"),
            "district_name": st.column_config.TextColumn("District Name"),
            "year": st.column_config.NumberColumn("Year", format="%d"),
            "region": st.column_config.TextColumn("Region"),
            "population": st.column_config.NumberColumn("Population", format="%,d"),
            "gddp_cr": st.column_config.NumberColumn("GDDP (₹ Cr)", format="₹ %,d"),
            "industrial_output_cr": st.column_config.NumberColumn("Industrial Output", format="₹ %,d"),
            "number_of_industries": st.column_config.NumberColumn("Industries", format="%d"),
            "road_length_km": st.column_config.NumberColumn("Road Length (km)", format="%.1f"),
            "road_density": st.column_config.NumberColumn("Road Density", format="%.2f"),
            "freight_volume_million_tonnes": st.column_config.NumberColumn("Freight (M Tonnes)", format="%.2f"),
            "warehouses": st.column_config.NumberColumn("Warehouses", format="%d"),
            "logistics_parks": st.column_config.NumberColumn("Logistics Parks", format="%d"),
            "railway_connectivity_score": st.column_config.NumberColumn("Rail Score", format="%.1f"),
            "port_connectivity_score": st.column_config.NumberColumn("Port Score", format="%.1f"),
            "congestion_index": st.column_config.NumberColumn("Congestion Index", format="%.1f"),
            "infrastructure_deficit_score": st.column_config.NumberColumn("Deficit Score", format="%.1f"),
            "recommended_budget_cr": st.column_config.NumberColumn("Rec. Budget (₹ Cr)", format="₹ %,d")
        },
        use_container_width=True,
        hide_index=True
    )

    # CSV Export Button
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=f"📥 Export Official TN Dataset for Year {selected_year} (CSV)",
        data=csv_data,
        file_name=f"tn_freight_dataset_{selected_year}.csv",
        mime="text/csv"
    )
if __name__ == "__main__":
    st.set_page_config(
        page_title="FreightOpt - Module 3 Dashboard",
        page_icon="📊",
        layout="wide"
    )
    run_module_3()
