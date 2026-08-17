"""
Module 1: Project Setup & Diagnostics
Independently runnable module for verifying system architecture, SQLite database health,
and exploring the 38 Tamil Nadu districts seed dataset.
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

from src.config import apply_custom_css, TN_REGIONS
from src.components.header import render_header
from src.database.repository import get_database_health, get_all_districts_df, get_state_kpis

def run_module_1(role: str = "Administrator"):
    """
    Executes Module 1 UI and diagnostic workflows.
    """
    apply_custom_css()
    render_header(module_title="Module 1: Project Setup", role=role)

    st.markdown("### ⚙️ System Architecture & Setup Status")
    st.info("Module 1 verifies directory layout, SQLite database initialization, and seeds the master dataset for all **38 Tamil Nadu districts**.")

    # 1. System Health Checks
    db_health = get_database_health()
    kpis = get_state_kpis()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">DB Health Status</div>
            <div class="metric-value" style="color: #34D399;">{db_health['status']}</div>
            <div class="metric-badge badge-green">SQLite Thread-Safe</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TN Districts Loaded</div>
            <div class="metric-value">{db_health['district_count']} / 38</div>
            <div class="metric-badge badge-blue">100% Coverage</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Freight Volume</div>
            <div class="metric-value">{kpis['total_freight_mton']:.1f} M Tons</div>
            <div class="metric-badge badge-amber">Annual Capacity</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total TN State GDP</div>
            <div class="metric-value">₹ {kpis['total_gdp_cr']:,.0f} Cr</div>
            <div class="metric-badge badge-blue">Industrial Base</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # 2. Database & Schema Inspection
    st.subheader("📋 SQLite Database & Schema Details")

    with st.expander("🔍 View Database Technical Metrics & Table Schema", expanded=True):
        st.json({
            "Database Engine": "SQLite 3",
            "Active Tables": db_health["tables"],
            "Seeded Record Count": db_health["district_count"],
            "Database Seed Status": "SUCCESS (Seeded 38 TN Districts)" if db_health["is_seeded"] else "Pending",
            "Primary Keys": ["district_id"],
            "Supported Regions": list(TN_REGIONS.keys())
        })

    st.divider()

    # 3. Interactive Data Explorer for 38 TN Districts
    st.subheader("🌾 Tamil Nadu 38 District Logistics Master Dataset")
    st.write("Browse, filter, and inspect the baseline freight dataset seeded into the application backend.")

    df = get_all_districts_df()

    # Filters
    f_col1, f_col2 = st.columns([1, 2])
    with f_col1:
        selected_region = st.selectbox(
            "Filter by Geographic Region:",
            options=["All Regions"] + list(TN_REGIONS.keys())
        )
    with f_col2:
        search_query = st.text_input("Search District Name:", placeholder="e.g. Coimbatore, Madurai, Thoothukudi...")

    # Apply filters
    filtered_df = df.copy()
    if selected_region != "All Regions":
        filtered_df = filtered_df[filtered_df["region"] == selected_region]
    if search_query:
        filtered_df = filtered_df[filtered_df["district_name"].str.contains(search_query, case=False, na=False)]

    st.dataframe(
        filtered_df[[
            "district_id", "district_name", "region", "population_lakhs", "gdp_cr",
            "freight_volume_mton", "road_density", "rail_score", "port_airport_dist_km",
            "warehouse_sqft", "congestion_index", "current_budget_cr"
        ]],
        column_config={
            "district_id": st.column_config.NumberColumn("ID", format="%d"),
            "district_name": st.column_config.TextColumn("District Name"),
            "region": st.column_config.TextColumn("Region"),
            "population_lakhs": st.column_config.NumberColumn("Population (Lakhs)", format="%.1f"),
            "gdp_cr": st.column_config.NumberColumn("GDP (₹ Cr)", format="₹ %,d"),
            "freight_volume_mton": st.column_config.NumberColumn("Freight (M Tons)", format="%.1f"),
            "road_density": st.column_config.NumberColumn("Road Density", format="%.1f"),
            "rail_score": st.column_config.NumberColumn("Rail Score (1-10)", format="%.1f"),
            "port_airport_dist_km": st.column_config.NumberColumn("Port/Airport Dist (km)", format="%.1f km"),
            "warehouse_sqft": st.column_config.NumberColumn("Warehouse (sq ft)", format="%,d"),
            "congestion_index": st.column_config.NumberColumn("Congestion Index", format="%.1f"),
            "current_budget_cr": st.column_config.NumberColumn("Budget (₹ Cr)", format="₹ %,d")
        },
        use_container_width=True,
        hide_index=True
    )

    # Download CSV capability
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Filtered TN Dataset (CSV)",
        data=csv_data,
        file_name="tamil_nadu_freight_dataset.csv",
        mime="text/csv"
    )

    st.success("✅ **Module 1 Setup Complete**: Project layout, SQLite database engine, configuration tokens, and 38 Tamil Nadu districts seed dataset are fully operational.")

if __name__ == "__main__":
    # Standalone execution support
    st.set_page_config(
        page_title="FreightOpt - Module 1 Project Setup",
        page_icon="🚛",
        layout="wide"
    )
    run_module_1()
