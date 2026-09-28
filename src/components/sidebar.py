"""
Sidebar Navigation Component
Supports Role-Based Access (Administrator vs Decision Maker)
and multi-module navigation across all 10 project modules.
"""

import streamlit as st
from src.logic.auth import init_auth_session, is_authenticated, get_current_user

# Clean Module Pipeline Titles (Without "Module X:" prefix)
MODULES_LIST = [
    "Project Setup",
    "Authentication UI",
    "Dashboard",
    "Project Input",
    "Tamil Nadu GIS Map",
    "Infrastructure Deficit Page",
    "Freight Prediction Page",
    "Budget Optimization",
    "Reports",
    "API Integration"
]

def render_sidebar():
    """
    Renders sidebar controls: Active Session/Role selector, Module navigation, and System info.
    Returns a tuple: (selected_role, selected_module)
    """
    init_auth_session()
    current_user = get_current_user()

    with st.sidebar:
        # App Branding Header
        col_icon, col_title = st.columns([1, 3])
        with col_icon:
            st.markdown("<div style='font-size: 2.4rem; line-height: 1;'>🚛</div>", unsafe_allow_html=True)
        with col_title:
            st.markdown("<h2 style='margin:0; padding:0; color:#FFFFFF !important; font-size: 1.5rem;'>FreightOpt TN</h2>", unsafe_allow_html=True)
            st.markdown("<p style='margin:0; color:#94A3B8 !important; font-size: 0.8rem; font-weight: 500;'>Smart Infrastructure & Analytics</p>", unsafe_allow_html=True)
        
        st.markdown("<div style='margin-top: 15px; margin-bottom: 15px; border-bottom: 1px solid #334155;'></div>", unsafe_allow_html=True)

        # 1. Target User Role & Session Widget
        st.markdown("<h4 style='color:#60A5FA !important; margin-bottom: 8px;'>👤 User Identity</h4>", unsafe_allow_html=True)
        
        if is_authenticated() and current_user:
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.9); padding: 12px; border-radius: 8px; border: 1px solid #3B82F6; margin-bottom: 10px;">
                <div style="font-size: 0.75rem; color: #34D399; font-weight: 700;">🟢 LOGGED IN</div>
                <div style="font-size: 0.95rem; font-weight: 700; color: #FFFFFF; margin-top: 2px;">{current_user['full_name']}</div>
                <div style="font-size: 0.8rem; color: #94A3B8;">{current_user['role']}</div>
            </div>
            """, unsafe_allow_html=True)
            role = current_user['role']
        else:
            role_options = ["Administrator", "Decision Maker (Government Planner)"]
            default_idx = role_options.index(st.session_state.get("active_role", "Administrator")) if st.session_state.get("active_role") in role_options else 0
            
            role = st.selectbox(
                "Select Operating Role:",
                options=role_options,
                index=default_idx,
                label_visibility="collapsed",
                help="Switching role adjusts access rights and feature availability."
            )
            st.session_state["active_role"] = role

        st.markdown("<div style='margin-top: 15px; margin-bottom: 15px; border-bottom: 1px solid #334155;'></div>", unsafe_allow_html=True)

        # 2. Module Navigation
        st.markdown("<h4 style='color:#60A5FA !important; margin-bottom: 8px;'>🗺️ Module Pipeline</h4>", unsafe_allow_html=True)
        selected_module = st.radio(
            "Select Module:",
            options=MODULES_LIST,
            index=1,  # Default to Authentication UI if active
            label_visibility="collapsed"
        )

        st.markdown("<div style='margin-top: 15px; margin-bottom: 15px; border-bottom: 1px solid #334155;'></div>", unsafe_allow_html=True)

        # 3. System Status Widget
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.8); padding: 14px; border-radius: 10px; border: 1px solid #334155;">
            <div style="color: #60A5FA; font-weight: 700; font-size: 0.85rem; margin-bottom: 6px;">⚡ SYSTEM STATUS</div>
            <div style="color: #E2E8F0; font-size: 0.8rem; line-height: 1.6;">
                🟢 <strong>Auth System:</strong> Active<br>
                📍 <strong>Coverage:</strong> 38 TN Districts<br>
                👤 <strong>Role:</strong> {role.split(' ')[0]}
            </div>
        </div>
        """, unsafe_allow_html=True)

        return role, selected_module
