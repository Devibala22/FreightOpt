"""
FreightOpt Main Streamlit Application Entry Point
Controls application routing across all 10 project modules.
"""

import streamlit as st

# Configure Page
st.set_page_config(
    page_title="FreightOpt – Smart Freight Planning & Budget Optimization",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

from src.config import apply_custom_css
from src.components.sidebar import render_sidebar
from modules.module_1_project_setup import run_module_1
from modules.module_2_auth import run_module_2
from modules.module_3_dashboard import run_module_3
from modules.module_4_project_input import run_module_4
from modules.module_5_gis_map import run_module_5
from modules.module_6_deficit import run_module_6
from modules.module_7_prediction import run_module_7
from modules.module_8_budget import run_module_8
from modules.module_9_reports import run_module_9
from modules.module_10_api import run_module_10

def main():
    # 1. Apply global styling
    apply_custom_css()

    # 2. Render sidebar navigation & retrieve active role & module
    role, selected_module = render_sidebar()

    # 3. Router for all 10 Modules
    if selected_module == "Module 1: Project Setup":
        run_module_1(role=role)
    elif selected_module == "Module 2: Authentication UI":
        run_module_2(role=role)
    elif selected_module == "Module 3: Dashboard":
        run_module_3(role=role)
    elif selected_module == "Module 4: Project Input":
        run_module_4(role=role)
    elif selected_module == "Module 5: Tamil Nadu GIS Map":
        run_module_5(role=role)
    elif selected_module == "Module 6: Infrastructure Deficit Page":
        run_module_6(role=role)
    elif selected_module == "Module 7: Freight Prediction Page":
        run_module_7(role=role)
    elif selected_module == "Module 8: Budget Optimization":
        run_module_8(role=role)
    elif selected_module == "Module 9: Reports":
        run_module_9(role=role)
    elif selected_module == "Module 10: API Integration":
        run_module_10(role=role)
    else:
        run_module_3(role=role)

if __name__ == "__main__":
    main()
