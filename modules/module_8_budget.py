"""
Module 8: Budget Optimization & Capital Allocation Engine
Independently runnable module for Linear Programming (scipy.optimize.linprog) capital budget optimization,
regional allocation distribution, and optimal infrastructure execution roadmaps.
"""

import sys
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Ensure parent root is in Python path for standalone execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.config import apply_custom_css
from src.components.header import render_header
from src.logic.budget_optimizer import optimize_budget_allocation

def run_module_8(role: str = "Administrator"):
    """
    Executes Module 8 Budget Optimization UI & LP solver workflows.
    """
    apply_custom_css()
    render_header(module_title="Module 8: Budget Optimization", role=role)

    st.markdown("### 💰 AI-Powered Infrastructure Capital Budget Optimizer")
    st.info("Utilize Scipy Linear Programming (Knapsack Algorithm) to optimize Tamil Nadu state capital budget allocation across high-vulnerability districts and project proposals.")

    # Sidebar Controls
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ Optimization Parameters")

    total_budget = st.sidebar.slider(
        "💵 Total Available State Budget (₹ Cr):",
        min_value=100.0,
        max_value=5000.0,
        value=1500.0,
        step=50.0,
        key="opt_budget"
    )

    objective = st.sidebar.selectbox(
        "🎯 Optimization Target Objective:",
        options=["Balanced Multi-Objective", "Maximize Deficit Reduction", "Maximize ROI Multiplier"],
        index=0,
        key="opt_obj"
    )

    # Run Optimization Solver
    opt_res = optimize_budget_allocation(
        total_budget_cr=total_budget,
        objective=objective
    )

    if not opt_res:
        st.error("No candidate projects available for budget optimization.")
        return

    sel_df = opt_res["selected_projects_df"]
    unsel_df = opt_res["unselected_projects_df"]

    # Executive Portfolio KPI Cards
    st.markdown("### 📊 Capital Allocation Portfolio Overview")
    k_col1, k_col2, k_col3, k_col4 = st.columns(4)

    with k_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Allocated Budget</div>
            <div class="metric-value">₹ {opt_res['total_allocated_cr']:,.1f} Cr</div>
            <div class="metric-badge badge-green">{opt_res['utilisation_pct']:.1f}% Utilised</div>
        </div>
        """, unsafe_allow_html=True)

    with k_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Selected Projects</div>
            <div class="metric-value" style="color: #60A5FA;">{opt_res['selected_count']} / {opt_res['total_candidate_count']}</div>
            <div class="metric-badge badge-blue">Optimized Roadmap</div>
        </div>
        """, unsafe_allow_html=True)

    with k_col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Deficit Score Reduction</div>
            <div class="metric-value" style="color: #34D399;">-{opt_res['predicted_deficit_reduction_pts']:.1f} Pts</div>
            <div class="metric-badge badge-green">State Impact</div>
        </div>
        """, unsafe_allow_html=True)

    with k_col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Portfolio Avg ROI</div>
            <div class="metric-value">{opt_res['avg_roi_multiplier']:.2f} x</div>
            <div class="metric-badge badge-amber">Efficiency Gain</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Visual Breakdown Charts
    st.markdown("### 📈 Visual Budget Distribution Breakdown")
    ch_col1, ch_col2 = st.columns(2)

    with ch_col1:
        reg_alloc = sel_df.groupby("region")["cost_estimate_cr"].sum().reset_index()
        fig_reg = px.pie(
            reg_alloc,
            values="cost_estimate_cr",
            names="region",
            hole=0.45,
            color_discrete_sequence=["#3B82F6", "#34D399", "#FBBF24", "#A855F7", "#EC4899"],
            title="🌐 Budget Allocation Share by Region"
        )
        fig_reg.update_layout(
            paper_bgcolor="rgba(15, 23, 42, 0)",
            plot_bgcolor="rgba(15, 23, 42, 0)",
            font=dict(color="#F8FAFC", size=12),
            height=360,
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(orientation="h", y=-0.1, x=0.2)
        )
        fig_reg.update_traces(hovertemplate="<b>%{label} Region</b><br>Allocated: <b>₹ %{value:,.1f} Cr</b> (%{percent})<extra></extra>")
        st.plotly_chart(fig_reg, use_container_width=True)

    with ch_col2:
        cat_alloc = sel_df.groupby("project_type")["cost_estimate_cr"].sum().reset_index().sort_values(by="cost_estimate_cr", ascending=True)
        fig_cat = px.bar(
            cat_alloc,
            x="cost_estimate_cr",
            y="project_type",
            orientation="h",
            text_auto=", .1f",
            color="cost_estimate_cr",
            color_continuous_scale=["#1E3A8A", "#3B82F6", "#60A5FA"],
            title="🏭 Budget Allocation by Infrastructure Category (₹ Cr)"
        )
        fig_cat.update_layout(
            paper_bgcolor="rgba(15, 23, 42, 0)",
            plot_bgcolor="rgba(15, 23, 42, 0)",
            font=dict(color="#F8FAFC", size=11),
            coloraxis_showscale=False,
            height=360,
            margin=dict(l=10, r=20, t=40, b=20),
            xaxis_title="Allocated Capital (₹ Cr)",
            yaxis_title="Category"
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    st.divider()

    # Optimized Execution Roadmap Table
    st.markdown("### 📋 Optimal Selected Infrastructure Projects Roadmap")
    st.write(f"Displaying **{len(sel_df)}** funded projects totaling **₹ {opt_res['total_allocated_cr']:,.1f} Cr**.")

    st.dataframe(
        sel_df[[
            "project_id", "district_name", "region", "project_name",
            "project_type", "cost_estimate_cr", "expected_roi_multiplier",
            "priority_level", "source"
        ]],
        column_config={
            "project_id": st.column_config.TextColumn("Project ID"),
            "district_name": st.column_config.TextColumn("District"),
            "region": st.column_config.TextColumn("Region"),
            "project_name": st.column_config.TextColumn("Project Title"),
            "project_type": st.column_config.TextColumn("Category"),
            "cost_estimate_cr": st.column_config.NumberColumn("Cost (₹ Cr)", format="₹ %,d"),
            "expected_roi_multiplier": st.column_config.NumberColumn("ROI", format="%.2fx"),
            "priority_level": st.column_config.TextColumn("Priority"),
            "source": st.column_config.TextColumn("Source")
        },
        use_container_width=True,
        hide_index=True
    )

    # Export CSV
    csv_opt = sel_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=f"📥 Export Optimal Capital Allocation Roadmap for ₹ {total_budget:,.0f} Cr Budget (CSV)",
        data=csv_opt,
        file_name=f"tn_optimal_capital_budget_roadmap_{int(total_budget)}cr.csv",
        mime="text/csv"
    )

    # Unfunded Backlog Section
    if not unsel_df.empty:
        with st.expander(f"📌 View Unfunded Project Backlog ({len(unsel_df)} Projects)"):
            st.dataframe(
                unsel_df[["project_id", "district_name", "project_name", "cost_estimate_cr", "expected_roi_multiplier", "priority_level"]],
                use_container_width=True,
                hide_index=True
            )
if __name__ == "__main__":
    st.set_page_config(
        page_title="FreightOpt - Module 8 Budget Optimization",
        page_icon="💰",
        layout="wide"
    )
    run_module_8()
