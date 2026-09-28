"""
Module 10: API Integration & External System Connectors
Independently runnable module for testing REST API endpoints, generating security bearer tokens,
and connecting with ULIP National Logistics Portal & State GIS feeds.
"""

import sys
import os
import json
import streamlit as st
import pandas as pd

# Ensure parent root is in Python path for standalone execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.config import apply_custom_css
from src.components.header import render_header
from src.api.main import (
    get_health, get_districts, get_district_by_name,
    get_projects, create_project, predict_freight, optimize_budget,
    ProjectProposalRequest, PredictionRequest
)
from src.logic.api_client import generate_api_bearer_token, simulate_ulip_national_portal_feed

def run_module_10(role: str = "Administrator"):
    """
    Executes Module 10 API Integration UI & Workflows.
    """
    apply_custom_css()
    render_header(module_title="Module 10: API Integration", role=role)

    st.markdown("### 🔌 REST API Integration & External System Hub")
    st.info("Interface with FreightOpt REST API endpoints, generate security tokens, and inspect integrations with National Logistics Portals (ULIP) & State GIS systems.")

    # Main Tabs
    tab_explorer, tab_tokens, tab_feeds = st.tabs([
        "🧪 Interactive REST API Endpoint Explorer",
        "🔑 Security Bearer Token Manager",
        "🌐 External System Integration Feeds (ULIP / GIS)"
    ])

    # -------------------------------------------------------------
    # TAB 1: INTERACTIVE REST API ENDPOINT EXPLORER
    # -------------------------------------------------------------
    with tab_explorer:
        st.subheader("Interactive REST API Endpoint Tester")

        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.7); border-left: 4px solid #3B82F6; padding: 12px 18px; border-radius: 8px; margin-bottom: 20px; font-size: 0.88rem;">
            🌐 <strong>REST API Base URL:</strong> <code>http://localhost:8000/api/v1</code> | 📚 <strong>OpenAPI Docs:</strong> <a href="http://localhost:8000/docs" target="_blank" style="color: #60A5FA;">http://localhost:8000/docs</a>
        </div>
        """, unsafe_allow_html=True)

        e_col1, e_col2 = st.columns([1, 1])

        with e_col1:
            st.markdown("#### ⚙️ Request Configuration")
            endpoint = st.selectbox(
                "Select API Endpoint:",
                options=[
                    "GET /api/v1/health",
                    "GET /api/v1/districts",
                    "GET /api/v1/districts/{name}",
                    "GET /api/v1/projects",
                    "POST /api/v1/projects",
                    "POST /api/v1/predict",
                    "GET /api/v1/optimize"
                ],
                index=0,
                key="api_end"
            )

            # Parameters per Endpoint
            params = {}
            if endpoint == "GET /api/v1/districts":
                param_year = st.selectbox("Year Parameter:", options=[2020, 2021, 2022, 2023, 2024, 2025, 2026], index=6)
                params["year"] = param_year
            elif endpoint == "GET /api/v1/districts/{name}":
                param_name = st.text_input("District Name:", value="Coimbatore")
                params["district_name"] = param_name
            elif endpoint == "GET /api/v1/projects":
                param_status = st.selectbox("Status Filter:", options=["All Statuses", "Approved", "Under Review", "Proposed"])
                params["status"] = param_status if param_status != "All Statuses" else None
            elif endpoint == "POST /api/v1/projects":
                st.caption("JSON Payload for Project Creation:")
                p_dist = st.text_input("District Name:", value="Salem")
                p_title = st.text_input("Project Name:", value="Salem Agro Logistics Hub")
                p_cost = st.number_input("Cost (₹ Cr):", value=180.0)
                p_roi = st.number_input("ROI Multiplier:", value=2.2)
                p_year = st.selectbox("Target Year:", options=[2025, 2026, 2027], index=1)
                params["payload"] = ProjectProposalRequest(
                    district_name=p_dist,
                    project_name=p_title,
                    project_type="Cold Storage Hub",
                    cost_estimate_cr=p_cost,
                    expected_roi_multiplier=p_roi,
                    implementation_year=p_year,
                    priority_level="High",
                    submitted_by="api_user@tn.gov.in"
                )
            elif endpoint == "POST /api/v1/predict":
                st.caption("JSON Payload for Freight Prediction:")
                pr_dist = st.text_input("District Target:", value="Chennai")
                pr_yr = st.selectbox("Target Forecast Year:", options=[2027, 2028, 2029, 2030], index=1)
                pr_ind = st.slider("Industrial Growth (%):", min_value=1.0, max_value=15.0, value=8.5)
                params["payload"] = PredictionRequest(
                    district_name=pr_dist,
                    target_year=pr_yr,
                    gddp_growth_pct=6.5,
                    industrial_growth_pct=pr_ind,
                    added_road_density=0.5,
                    added_warehouses=2
                )
            elif endpoint == "GET /api/v1/optimize":
                param_b = st.number_input("Total Budget Limit (₹ Cr):", value=1200.0, step=100.0)
                params["total_budget_cr"] = param_b

            run_api = st.button("🚀 Execute REST API Request", type="primary", use_container_width=True)

        with e_col2:
            st.markdown("#### 📄 API JSON Response")
            if run_api:
                try:
                    response_data = None
                    status_code = 200

                    if endpoint == "GET /api/v1/health":
                        response_data = get_health()
                    elif endpoint == "GET /api/v1/districts":
                        response_data = get_districts(year=params.get("year", 2026))
                    elif endpoint == "GET /api/v1/districts/{name}":
                        response_data = get_district_by_name(district_name=params.get("district_name", "Coimbatore"))
                    elif endpoint == "GET /api/v1/projects":
                        response_data = get_projects(status=params.get("status"))
                    elif endpoint == "POST /api/v1/projects":
                        response_data = create_project(payload=params["payload"])
                        status_code = 201
                    elif endpoint == "POST /api/v1/predict":
                        response_data = predict_freight(payload=params["payload"])
                    elif endpoint == "GET /api/v1/optimize":
                        response_data = optimize_budget(total_budget_cr=params.get("total_budget_cr", 1200.0))

                    st.markdown(f"**HTTP Status:** <span style='color:#34D399; font-weight:bold;'>{status_code} OK / Success</span>", unsafe_allow_html=True)
                    st.json(response_data)
                except Exception as ex:
                    st.error(f"API Error: {str(ex)}")
            else:
                st.info("Click 'Execute REST API Request' to send a request and view the JSON response payload.")

    # -------------------------------------------------------------
    # TAB 2: SECURITY BEARER TOKEN MANAGER
    # -------------------------------------------------------------
    with tab_tokens:
        st.subheader("API Authentication & Security Token Management")
        st.caption("Generate secure API Bearer Tokens for external government departments and regional transport portals.")

        with st.form("token_gen_form"):
            t_dept = st.selectbox("Department / External System:", options=[
                "Ministry of Road Transport & Highways (MoRTH)",
                "Tamil Nadu Industrial Development Corporation (TIDCO)",
                "ULIP National Logistics Portal Connector",
                "Greater Chennai Port Trust API Client",
                "State Disaster Management Authority"
            ])
            t_submit = st.form_submit_button("🔑 Generate Secure API Bearer Token", type="primary", use_container_width=True)

            if t_submit:
                tok_info = generate_api_bearer_token(department=t_dept)
                st.success(f"Generated API Bearer Token for **{t_dept}**:")
                st.code(tok_info["api_key"], language="bash")
                st.toast("Bearer token created.", icon="🔑")

        st.divider()

        st.markdown("#### 📋 Active Registered API Keys")
        active_keys = pd.DataFrame([
            {"Department": "TIDCO Logistics Division", "API Key": "tn_logistics_live_8f3a1c9e_4b2d109a", "Role": "Read/Write", "Created": "2026-08-01", "Status": "Active"},
            {"Department": "MoRTH National Highways", "API Key": "tn_logistics_live_7c4d2e1f_8a9b0c1d", "Role": "Read Only", "Created": "2026-08-05", "Status": "Active"},
            {"Department": "ULIP National Portal", "API Key": "tn_logistics_live_1a2b3c4d_5e6f7a8b", "Role": "Sync Feed", "Created": "2026-08-10", "Status": "Active"}
        ])
        st.dataframe(active_keys, use_container_width=True, hide_index=True)

    # -------------------------------------------------------------
    # TAB 3: EXTERNAL SYSTEM FEEDS (ULIP & GIS)
    # -------------------------------------------------------------
    with tab_feeds:
        st.subheader("External System Data Sync Feeds")
        
        ulip_feed = simulate_ulip_national_portal_feed()

        u_col1, u_col2 = st.columns([1, 1])
        with u_col1:
            st.markdown(f"""
            <div style="background: #1E293B; border-left: 4px solid #34D399; padding: 18px; border-radius: 8px;">
                <h4 style="margin-top:0; color:#34D399;">🌐 ULIP National Logistics Portal Feed</h4>
                <div>Status: <strong>{ulip_feed['sync_status']}</strong></div>
                <div>Synced Records: <strong>{ulip_feed['last_synced_records']} Districts</strong></div>
                <hr style="border-top: 1px solid #334155; margin: 10px 0;"/>
                <div style="font-size: 0.85rem;">
                    <strong>Monitored Port Terminals:</strong><br/>
                    • Chennai Port Trust<br/>
                    • Kamarajar Port Ennore<br/>
                    • VO Chidambaranar Port Tuticorin
                </div>
            </div>
            """, unsafe_allow_html=True)

        with u_col2:
            st.markdown("""
            <div style="background: #1E293B; border-left: 4px solid #3B82F6; padding: 18px; border-radius: 8px;">
                <h4 style="margin-top:0; color:#60A5FA;">🗺️ Tamil Nadu State GIS Infrastructure Sync</h4>
                <div>Spatial Sync Status: <strong>Connected / Operational</strong></div>
                <div>Mapped Features: <strong>38 District Boundaries & Highways</strong></div>
                <hr style="border-top: 1px solid #334155; margin: 10px 0;"/>
                <div style="font-size: 0.85rem;">
                    <strong>Synced Spatial Layers:</strong><br/>
                    • State Highway Network (km/100 km²)<br/>
                    • Railway Goods Terminal Freight Yards<br/>
                    • Industrial Parks & MMLP Locations
                </div>
            </div>
            """, unsafe_allow_html=True)
if __name__ == "__main__":
    st.set_page_config(
        page_title="FreightOpt - Module 10 API Integration",
        page_icon="🔌",
        layout="wide"
    )
    run_module_10()
