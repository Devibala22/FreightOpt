"""
Module 4: Project Input & Infrastructure Proposal Management
Independently runnable module for proposing new freight infrastructure projects,
managing approval workflows, and updating district logistics master data.
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
from src.database.repository import get_all_districts_df
from src.database.projects_repository import (
    add_infrastructure_project, get_all_projects_df,
    update_project_status, update_district_logistics_metrics
)
from src.logic.projects_engine import compute_project_summary_kpis, calculate_roi_score
from src.logic.auth import get_current_user

# Pre-defined Infrastructure Project Categories
PROJECT_TYPES = [
    "Multi-Modal Logistics Park (MMLP)",
    "Freight Bypass Road",
    "Cold Storage Hub",
    "Industrial Rail Spur",
    "Port Access Highway Corridor",
    "Warehousing & Cargo Cluster",
    "Logistics Terminal Expansion"
]

def run_module_4(role: str = "Administrator"):
    """
    Executes Module 4 Project Input UI & Management workflows.
    """
    apply_custom_css()
    current_user = get_current_user()
    active_role = current_user["role"] if current_user else role
    user_email = current_user["email"] if current_user else "planner@tnlogistics.gov.in"

    render_header(module_title="Module 4: Project Input", role=active_role)

    st.markdown("### 🏗️ Infrastructure Project Input & Data Management")
    st.info("Submit new freight infrastructure proposals, review project status, or update baseline district logistics metrics.")

    # Fetch 38 TN Districts list
    districts_df = get_all_districts_df(year=2026)
    tn_district_names = sorted(list(districts_df["district_name"].unique()))

    # Main Module Tabs
    tab_propose, tab_registry, tab_editor = st.tabs([
        "🏗️ Propose New Infrastructure Project",
        "📋 Project Proposals Registry",
        "✏️ District Master Data Editor"
    ])

    # -------------------------------------------------------------
    # TAB 1: SUBMIT NEW INFRASTRUCTURE PROJECT PROPOSAL
    # -------------------------------------------------------------
    with tab_propose:
        st.subheader("Submit Freight Infrastructure Investment Proposal")
        st.caption("Fill out the fields below to submit a capital expenditure proposal for Tamil Nadu logistics optimization.")

        with st.form("new_project_form"):
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                target_district = st.selectbox("Target District (Tamil Nadu):", options=tn_district_names)
                project_name = st.text_input("Project Name / Title:", placeholder="e.g. Salem Freight Bypass Link Corridor")
                project_type = st.selectbox("Infrastructure Category:", options=PROJECT_TYPES)
                cost_estimate = st.number_input("Estimated Capital Investment (₹ Cr):", min_value=1.0, max_value=5000.0, value=250.0, step=10.0)

            with p_col2:
                expected_roi = st.slider("Expected ROI Multiplier (Efficiency Gain):", min_value=1.0, max_value=5.0, value=2.2, step=0.1)
                impl_year = st.selectbox("Target Implementation Year:", options=[2024, 2025, 2026, 2027, 2028, 2029, 2030], index=2)
                priority_level = st.selectbox("Requested Priority Tier:", options=["High", "Medium", "Normal"])
                description = st.text_area("Detailed Rationale & Scope:", placeholder="Provide project alignment with industrial hubs, congestion relief, and freight connectivity...")

            submit_proposal = st.form_submit_button("🚀 Submit Project Proposal for Review", type="primary", use_container_width=True)

            if submit_proposal:
                if not project_name:
                    st.error("Please enter a valid Project Name.")
                else:
                    new_project_data = {
                        "district_name": target_district,
                        "project_name": project_name,
                        "project_type": project_type,
                        "cost_estimate_cr": cost_estimate,
                        "expected_roi_multiplier": expected_roi,
                        "implementation_year": impl_year,
                        "priority_level": priority_level,
                        "description": description,
                        "submitted_by": user_email,
                        "status": "Proposed"
                    }
                    proj_id = add_infrastructure_project(new_project_data)
                    st.success(f"🎉 **Proposal Submitted Successfully!** Assigned Project ID: `PRJ-TN-{proj_id:04d}` for **{target_district}**.")
                    st.toast("Project proposal recorded into database.", icon="✅")

    # -------------------------------------------------------------
    # TAB 2: PROPOSED PROJECTS REGISTRY & APPROVAL WORKFLOW
    # -------------------------------------------------------------
    with tab_registry:
        st.subheader("Project Proposals Portfolio & Approval Status")
        
        # Filter Bar
        f_col1, f_col2 = st.columns([2, 3])
        with f_col1:
            status_filter = st.selectbox("Filter Proposals by Status:", options=["All Statuses", "Proposed", "Under Review", "Approved", "Rejected"])
        with f_col2:
            search_proj = st.text_input("Search Proposal Name or District:", placeholder="Filter by project name...")

        projects_df = get_all_projects_df(status_filter=status_filter)
        if search_proj:
            projects_df = projects_df[
                projects_df["project_name"].str.contains(search_proj, case=False, na=False) |
                projects_df["district_name"].str.contains(search_proj, case=False, na=False)
            ]

        # Portfolio KPI Metrics
        pkpis = compute_project_summary_kpis(projects_df)
        k_col1, k_col2, k_col3, k_col4 = st.columns(4)
        with k_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Proposals</div>
                <div class="metric-value">{pkpis['total_projects']}</div>
                <div class="metric-badge badge-blue">Portfolio</div>
            </div>
            """, unsafe_allow_html=True)

        with k_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Investment</div>
                <div class="metric-value">₹ {pkpis['total_investment_cr']:,.1f} Cr</div>
                <div class="metric-badge badge-green">Capital Outlay</div>
            </div>
            """, unsafe_allow_html=True)

        with k_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Avg Expected ROI</div>
                <div class="metric-value">{pkpis['avg_roi_multiplier']:.2f} x</div>
                <div class="metric-badge badge-amber">Efficiency Multiplier</div>
            </div>
            """, unsafe_allow_html=True)

        with k_col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Approved Projects</div>
                <div class="metric-value" style="color: #34D399;">{pkpis['approved_count']}</div>
                <div class="metric-badge badge-green">Ready to Execute</div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Display Data Table
        st.dataframe(
            projects_df[[
                "project_id", "district_name", "project_name", "project_type",
                "cost_estimate_cr", "expected_roi_multiplier", "implementation_year",
                "priority_level", "submitted_by", "status"
            ]],
            column_config={
                "project_id": st.column_config.NumberColumn("ID", format="PRJ-%04d"),
                "district_name": st.column_config.TextColumn("District"),
                "project_name": st.column_config.TextColumn("Project Title"),
                "project_type": st.column_config.TextColumn("Category"),
                "cost_estimate_cr": st.column_config.NumberColumn("Cost (₹ Cr)", format="₹ %,d"),
                "expected_roi_multiplier": st.column_config.NumberColumn("ROI", format="%.1fx"),
                "implementation_year": st.column_config.NumberColumn("Target Year", format="%d"),
                "priority_level": st.column_config.TextColumn("Priority"),
                "submitted_by": st.column_config.TextColumn("Submitted By"),
                "status": st.column_config.TextColumn("Status")
            },
            use_container_width=True,
            hide_index=True
        )

        # Administrator Approval Action Controls
        if active_role == "Administrator":
            st.markdown("#### ⚡ Administrator Approval Controls")
            if not projects_df.empty:
                app_col1, app_col2, app_col3 = st.columns([2, 2, 1])
                with app_col1:
                    target_pid = st.selectbox("Select Project ID to Update:", options=projects_df["project_id"].tolist())
                with app_col2:
                    target_status = st.selectbox("Update Status To:", options=["Approved", "Under Review", "Proposed", "Rejected"])
                with app_col3:
                    st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
                    if st.button("Update Status", type="primary"):
                        if update_project_status(target_pid, target_status):
                            st.success(f"Updated Project `PRJ-{target_pid:04d}` status to **{target_status}**.")
                            st.rerun()

        # CSV Export
        csv_proj = projects_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Export Infrastructure Proposals Registry (CSV)",
            data=csv_proj,
            file_name="tn_infrastructure_proposals.csv",
            mime="text/csv"
        )

    # -------------------------------------------------------------
    # TAB 3: DISTRICT MASTER DATA EDITOR
    # -------------------------------------------------------------
    with tab_editor:
        st.subheader("Edit District Logistics Baseline Parameters")
        st.caption("Update baseline parameters for any district directly in the SQLite database.")

        edit_col1, edit_col2 = st.columns(2)
        with edit_col1:
            edit_district = st.selectbox("Select District to Edit:", options=tn_district_names, key="edit_dist")
            edit_year = st.selectbox("Select Year:", options=[2020, 2021, 2022, 2023, 2024, 2025, 2026], index=6, key="edit_yr")

        # Fetch current record for selected district & year
        cur_df = districts_df[(districts_df["district_name"] == edit_district) & (districts_df["year"] == edit_year)]
        if not cur_df.empty:
            rec = cur_df.iloc[0]
            with st.form("district_edit_form"):
                e_col1, e_col2 = st.columns(2)
                with e_col1:
                    new_density = st.number_input("Road Network Density:", value=float(rec["road_density"]), step=0.1)
                    new_wh = st.number_input("Warehouses Count:", value=int(rec["warehouses"]), step=1)
                    new_lp = st.number_input("Logistics Parks Count:", value=int(rec["logistics_parks"]), step=1)

                with e_col2:
                    new_congestion = st.number_input("Congestion Index:", value=float(rec["congestion_index"]), step=0.5)
                    new_deficit = st.number_input("Infrastructure Deficit Score:", value=float(rec["infrastructure_deficit_score"]), step=0.5)

                save_metrics = st.form_submit_button("💾 Save Updated District Metrics", type="primary", use_container_width=True)

                if save_metrics:
                    updated_metrics = {
                        "road_density": new_density,
                        "warehouses": new_wh,
                        "logistics_parks": new_lp,
                        "congestion_index": new_congestion,
                        "infrastructure_deficit_score": new_deficit
                    }
                    if update_district_logistics_metrics(edit_district, edit_year, updated_metrics):
                        st.success(f"Updated logistics metrics for **{edit_district} ({edit_year})** in SQLite database!")
                        st.rerun()
                    else:
                        st.error("Failed to update district metrics.")
if __name__ == "__main__":
    st.set_page_config(
        page_title="FreightOpt - Module 4 Project Input",
        page_icon="🏗️",
        layout="wide"
    )
    run_module_4()
