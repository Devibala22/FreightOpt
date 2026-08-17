"""
Module 9: Reports & Executive Policy Briefing Suite
Independently runnable module for generating automated executive briefing documents (Markdown/Text)
and exporting multi-format CSV datasets across all FreightOpt modules.
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
from src.logic.reports_engine import (
    generate_executive_report_markdown,
    generate_executive_report_plaintext,
    get_exportable_datasets
)

AUDIENCE_OPTIONS = [
    "State Cabinet / Chief Minister's Office",
    "Ministry of Infrastructure & Transport",
    "Regional District Collectors",
    "Public & Media Briefing"
]

ALL_SECTIONS = [
    "Executive Summary",
    "Deficit Analysis",
    "AI Forecasts",
    "Budget Optimization",
    "Recommendations"
]

def run_module_9(role: str = "Administrator"):
    """
    Executes Module 9 Reports & Briefing Suite UI workflows.
    """
    apply_custom_css()
    render_header(module_title="Module 9: Reports", role=role)

    st.markdown("### 📜 Executive Briefing Reports & Data Export Suite")
    st.info("Compile formal government policy documents, customize briefing target audiences, and download multi-format CSV datasets.")

    # Main Tabs
    tab_report, tab_datasets = st.tabs([
        "📝 Executive Briefing Report Generator",
        "📊 Multi-Format Dataset Export Suite"
    ])

    # -------------------------------------------------------------
    # TAB 1: EXECUTIVE BRIEFING REPORT GENERATOR
    # -------------------------------------------------------------
    with tab_report:
        st.subheader("Automated Executive Policy Briefing Compiler")

        # Customization Panel
        with st.expander("⚙️ Report Customization & Section Controls", expanded=True):
            ctrl_col1, ctrl_col2 = st.columns([1, 1])
            with ctrl_col1:
                target_audience = st.selectbox(
                    "Target Audience / Stakeholder:",
                    options=AUDIENCE_OPTIONS,
                    index=0,
                    key="rep_aud"
                )
                budget_limit = st.number_input(
                    "State Budget Limit (₹ Cr):",
                    min_value=100.0,
                    max_value=5000.0,
                    value=1500.0,
                    step=100.0,
                    key="rep_bud"
                )

            with ctrl_col2:
                st.markdown("**Select Sections to Include:**")
                sec_cols = st.columns(3)
                selected_sections = []
                for idx, sec in enumerate(ALL_SECTIONS):
                    col_target = sec_cols[idx % 3]
                    if col_target.checkbox(sec, value=True, key=f"sec_{sec}"):
                        selected_sections.append(sec)

        # Generate Reports
        report_md = generate_executive_report_markdown(
            target_audience=target_audience,
            include_sections=selected_sections,
            budget_limit_cr=budget_limit
        )

        report_txt = generate_executive_report_plaintext(
            target_audience=target_audience,
            include_sections=selected_sections,
            budget_limit_cr=budget_limit
        )

        # Prominent Download Action Buttons
        st.markdown("#### 📥 Export Official Policy Documents")
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            st.download_button(
                label="📥 Download Executive Briefing Report (.md)",
                data=report_md.encode("utf-8"),
                file_name="tn_executive_logistics_report.md",
                mime="text/markdown",
                type="primary",
                use_container_width=True
            )
        with btn_col2:
            st.download_button(
                label="📄 Download Formal Official Memorandum (.txt)",
                data=report_txt.encode("utf-8"),
                file_name="tn_official_logistics_memorandum.txt",
                mime="text/plain",
                use_container_width=True
            )

        st.divider()

        # Live Document Preview Container
        st.markdown("#### 📄 Live Document Preview")
        with st.container(border=True, height=550):
            st.markdown(report_md)

    # -------------------------------------------------------------
    # TAB 2: MULTI-FORMAT DATASET EXPORT SUITE
    # -------------------------------------------------------------
    with tab_datasets:
        st.subheader("Tamil Nadu Master Datasets & Export Suite")
        st.caption("Download full CSV datasets generated across FreightOpt analysis modules.")

        datasets = get_exportable_datasets()

        d_col1, d_col2 = st.columns(2)

        with d_col1:
            # Dataset 1
            st.markdown("""
            <div style="background: #1E293B; border-left: 4px solid #3B82F6; padding: 14px; border-radius: 6px; margin-bottom: 15px;">
                <h5 style="margin:0; color:#60A5FA;">1. Official 38-District Baseline Dataset (2026)</h5>
                <div style="font-size:0.85rem; color:#94A3B8; margin-top:4px;">Contains population, GDDP, industrial output, road density, warehouses, connectivity, and deficit scores for all 38 TN districts.</div>
            </div>
            """, unsafe_allow_html=True)
            df1 = datasets["tn_districts_master_2026.csv"]
            st.download_button(
                label="📥 Download District Master Dataset (CSV)",
                data=df1.to_csv(index=False).encode("utf-8"),
                file_name="tn_districts_master_2026.csv",
                mime="text/csv",
                use_container_width=True
            )

            # Dataset 2
            st.markdown("""
            <div style="background: #1E293B; border-left: 4px solid #34D399; padding: 14px; border-radius: 6px; margin-bottom: 15px; margin-top: 15px;">
                <h5 style="margin:0; color:#34D399;">2. Infrastructure Proposals Registry</h5>
                <div style="font-size:0.85rem; color:#94A3B8; margin-top:4px;">Complete list of submitted project proposals, cost estimates, expected ROI multipliers, priority tiers, and approval statuses.</div>
            </div>
            """, unsafe_allow_html=True)
            df2 = datasets["infrastructure_proposals_registry.csv"]
            st.download_button(
                label="📥 Download Projects Proposals Registry (CSV)",
                data=df2.to_csv(index=False).encode("utf-8"),
                file_name="infrastructure_proposals_registry.csv",
                mime="text/csv",
                use_container_width=True
            )

        with d_col2:
            # Dataset 3
            st.markdown("""
            <div style="background: #1E293B; border-left: 4px solid #FBBF24; padding: 14px; border-radius: 6px; margin-bottom: 15px;">
                <h5 style="margin:0; color:#FBBF24;">3. AI Freight Projections Matrix (2027 – 2030)</h5>
                <div style="font-size:0.85rem; color:#94A3B8; margin-top:4px;">Machine Learning predicted cargo growth volumes and 95% confidence intervals across all 38 districts through 2030.</div>
            </div>
            """, unsafe_allow_html=True)
            df3 = datasets["ai_freight_projections_2027_2030.csv"]
            st.download_button(
                label="📥 Download 2027-2030 AI Projections Matrix (CSV)",
                data=df3.to_csv(index=False).encode("utf-8"),
                file_name="ai_freight_projections_2027_2030.csv",
                mime="text/csv",
                use_container_width=True
            )

            # Dataset 4
            st.markdown("""
            <div style="background: #1E293B; border-left: 4px solid #A855F7; padding: 14px; border-radius: 6px; margin-bottom: 15px; margin-top: 15px;">
                <h5 style="margin:0; color:#A855F7;">4. Optimal Capital Budget Allocation Roadmap</h5>
                <div style="font-size:0.85rem; color:#94A3B8; margin-top:4px;">Linear Programming optimized capital allocation roadmap showing selected funded projects for state infrastructure execution.</div>
            </div>
            """, unsafe_allow_html=True)
            df4 = datasets["optimal_budget_allocation_roadmap.csv"]
            st.download_button(
                label="📥 Download Optimal Capital Budget Roadmap (CSV)",
                data=df4.to_csv(index=False).encode("utf-8"),
                file_name="optimal_budget_allocation_roadmap.csv",
                mime="text/csv",
                use_container_width=True
            )

    st.success("✅ **Module 9 Reports Suite Complete**: Executive policy briefing compiler and multi-format CSV export suite active.")

if __name__ == "__main__":
    st.set_page_config(
        page_title="FreightOpt - Module 9 Reports",
        page_icon="📜",
        layout="wide"
    )
    run_module_9()
