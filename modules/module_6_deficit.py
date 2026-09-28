"""
Module 6: Infrastructure Deficit & Vulnerability Analytics
Independently runnable module for evaluating, scoring, and simulating infrastructure gaps
across all 38 Tamil Nadu districts.
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
from src.database.repository import get_all_districts_df, get_available_years
from src.logic.deficit_engine import (
    compute_state_benchmarks,
    calculate_multi_pillar_deficit,
    get_deficit_tier,
    simulate_deficit_reduction
)

def run_module_6(role: str = "Administrator"):
    """
    Executes Module 6 Infrastructure Deficit Page UI & Analytics workflows.
    """
    apply_custom_css()
    render_header(module_title="Module 6: Infrastructure Deficit Page", role=role)

    st.markdown("### ⚠️ Infrastructure Deficit & Vulnerability Analysis")
    st.info("Identify logistics bottlenecks, evaluate multi-pillar infrastructure deficits, and simulate capital investment impact.")

    # Available Years
    years = get_available_years()
    selected_year = st.sidebar.select_slider(
        "📅 Select Analysis Year (2020 - 2026):",
        options=years,
        value=max(years) if years else 2026,
        key="def_year"
    )

    # Fetch Data
    raw_df = get_all_districts_df(year=selected_year)
    benchmarks = compute_state_benchmarks(raw_df)

    # Compute Sub-Pillar Scores for all districts
    df = raw_df.copy()
    pillar_scores = []
    tiers = []
    for _, row in df.iterrows():
        p_res = calculate_multi_pillar_deficit(row, benchmarks)
        tier_name, _, _ = get_deficit_tier(p_res["composite_deficit_score"])
        pillar_scores.append(p_res)
        tiers.append(tier_name)

    pdf = pd.DataFrame(pillar_scores)
    df["road_gap_score"] = pdf["road_gap_score"]
    df["congestion_score"] = pdf["congestion_score"]
    df["storage_gap_score"] = pdf["storage_gap_score"]
    df["conn_gap_score"] = pdf["conn_gap_score"]
    df["calculated_deficit_score"] = pdf["composite_deficit_score"]
    df["deficit_tier"] = tiers

    # Filter Controls
    f_col1, f_col2, f_col3 = st.columns([2, 2, 2])
    with f_col1:
        selected_region = st.selectbox(
            "Filter by Geographic Region:",
            options=["All Regions (State-wide)"] + sorted(list(df["region"].unique())),
            key="def_reg"
        )
    with f_col2:
        selected_tier = st.selectbox(
            "Filter by Deficit Severity Tier:",
            options=["All Tiers", "Critical Deficit", "High Deficit", "Moderate Deficit", "Low Deficit"],
            key="def_tier"
        )
    with f_col3:
        search_district = st.text_input("Search District:", placeholder="e.g. Salem, Chennai, Madurai...", key="def_search")

    # Apply Filters
    f_df = df.copy()
    if selected_region != "All Regions (State-wide)":
        f_df = f_df[f_df["region"] == selected_region]
    if selected_tier != "All Tiers":
        f_df = f_df[f_df["deficit_tier"] == selected_tier]
    if search_district:
        f_df = f_df[f_df["district_name"].str.contains(search_district, case=False, na=False)]

    f_df = f_df.sort_values(by="infrastructure_deficit_score", ascending=False)

    # 1. Top 5 High-Deficit Critical Alerts
    st.markdown(f"### 🛑 Top 5 Critical Deficit Vulnerable Districts ({selected_year})")
    top5_df = df.sort_values(by="infrastructure_deficit_score", ascending=False).head(5)

    alert_cols = st.columns(5)
    for idx, (_, r) in enumerate(top5_df.iterrows()):
        with alert_cols[idx]:
            score = r["infrastructure_deficit_score"]
            tier_name, badge_cls, color_hex = get_deficit_tier(score)
            st.markdown(f"""
            <div class="metric-card" style="border-top: 4px solid {color_hex};">
                <div class="metric-label"># {idx+1} Vulnerable</div>
                <div class="metric-value" style="font-size: 1.15rem; color: {color_hex};">{r['district_name']}</div>
                <div style="font-size: 0.8rem; margin: 4px 0;">Deficit: <strong>{score:.1f}</strong> | Cong: <strong>{r['congestion_index']:.1f}</strong></div>
                <div class="metric-badge {badge_cls}">{tier_name}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # 2. Main Analytics & Visuals (Radar Chart & Ranking Bar)
    st.markdown("### 📊 District Infrastructure Pillar Comparison")
    
    vis_col1, vis_col2 = st.columns([1, 1])

    with vis_col1:
        st.markdown("#### 🎯 Radar Chart: District Pillars vs State Benchmark")
        target_radar_dist = st.selectbox(
            "Select District for Radar Analysis:",
            options=sorted(list(df["district_name"].unique())),
            index=0,
            key="radar_dist"
        )
        dist_row = df[df["district_name"] == target_radar_dist].iloc[0]

        categories = ["Road Gap", "Congestion Bottleneck", "Storage Deficit", "Connectivity Gap"]
        dist_values = [
            dist_row["road_gap_score"],
            dist_row["congestion_score"],
            dist_row["storage_gap_score"],
            dist_row["conn_gap_score"]
        ]
        state_bench_values = [50.0, 30.0, 45.0, 40.0]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=dist_values + [dist_values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            name=f"{target_radar_dist} District",
            line_color="#EF4444"
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=state_bench_values + [state_bench_values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            name="State Benchmark",
            line_color="#3B82F6",
            opacity=0.4
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor="#334155"),
                angularaxis=dict(gridcolor="#334155")
            ),
            paper_bgcolor="rgba(15, 23, 42, 0)",
            plot_bgcolor="rgba(15, 23, 42, 0)",
            font=dict(color="#F8FAFC", size=12),
            height=380,
            margin=dict(l=40, r=40, t=30, b=30),
            legend=dict(orientation="h", y=-0.1, x=0.2)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with vis_col2:
        st.markdown("#### 📉 Regional Deficit Score Ranking")
        region_deficit = f_df.groupby("region")["infrastructure_deficit_score"].mean().reset_index()
        fig_bar = px.bar(
            region_deficit,
            x="infrastructure_deficit_score",
            y="region",
            orientation="h",
            text_auto=".1f",
            color="infrastructure_deficit_score",
            color_continuous_scale=["#10B981", "#F59E0B", "#EF4444"],
            labels={"infrastructure_deficit_score": "Avg Deficit Score", "region": "Region"}
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(15, 23, 42, 0)",
            plot_bgcolor="rgba(15, 23, 42, 0)",
            font=dict(color="#F8FAFC", size=12),
            coloraxis_showscale=False,
            height=380,
            margin=dict(l=10, r=20, t=30, b=30)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # 3. Interactive Infrastructure Deficit Reduction Simulator
    st.markdown("### 🧪 Interactive Infrastructure Deficit Reduction Simulator")
    st.caption("Simulate capital interventions (adding road bypass length or warehousing facilities) to predict the reduction in Deficit Score.")

    sim_col1, sim_col2 = st.columns([1, 1])

    with sim_col1:
        sim_district = st.selectbox(
            "Select Target District to Simulate:",
            options=sorted(list(df["district_name"].unique())),
            index=0,
            key="sim_dist"
        )
        s_row = df[df["district_name"] == sim_district].iloc[0]

        add_road_km = st.slider("Add Proposed Highway Bypass Length (km):", min_value=0.0, max_value=150.0, value=25.0, step=5.0)
        add_warehouses = st.slider("Add Proposed Logistics Warehouses:", min_value=0, max_value=20, value=4, step=1)

    with sim_col2:
        cur_deficit = float(s_row["infrastructure_deficit_score"])
        sim_res = simulate_deficit_reduction(
            current_density=float(s_row["road_density"]),
            current_wh=int(s_row["warehouses"]),
            current_congestion=float(s_row["congestion_index"]),
            added_road_km=add_road_km,
            added_warehouses=add_warehouses,
            area_sq_km=float(s_row.get("area_sq_km", 4000.0))
        )
        new_deficit = max(10.0, round(cur_deficit - sim_res["score_reduction"], 1))
        cur_tier, _, _ = get_deficit_tier(cur_deficit)
        new_tier, new_badge, new_color = get_deficit_tier(new_deficit)

        st.markdown(f"""
        <div style="background: #1E293B; border-left: 4px solid {new_color}; padding: 18px; border-radius: 8px;">
            <h4 style="margin-top:0; color: #60A5FA;">Simulation Results for {sim_district}</h4>
            <div style="font-size: 1.1rem; margin-bottom: 10px;">
                Current Deficit Score: <strong style="color: #EF4444;">{cur_deficit:.1f}</strong> ({cur_tier})<br/>
                Predicted Deficit Score: <strong style="color: {new_color}; font-size: 1.3rem;">{new_deficit:.1f}</strong> ({new_tier})
            </div>
            <div style="color: #34D399; font-weight: bold; font-size: 1rem;">
                🎉 Estimated Deficit Reduction: -{sim_res['score_reduction']:.1f} Points
            </div>
            <hr style="border-top: 1px solid #334155; margin: 10px 0;"/>
            <div style="font-size: 0.85rem; color: #94A3B8;">
                • New Road Density: <strong>{sim_res['new_road_density']:.2f}</strong> km / 100 sq km<br/>
                • Total Warehouses: <strong>{sim_res['new_warehouses']}</strong> Facilities<br/>
                • Reduced Congestion Index: <strong>{sim_res['new_congestion_index']:.1f}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # 4. District Deficit Rank Matrix Table
    st.markdown(f"### 📋 Tamil Nadu District Infrastructure Deficit Matrix ({selected_year})")
    st.dataframe(
        f_df[[
            "district_name", "region", "infrastructure_deficit_score", "deficit_tier",
            "road_density", "congestion_index", "warehouses", "logistics_parks",
            "freight_volume_million_tonnes", "recommended_budget_cr"
        ]],
        column_config={
            "district_name": st.column_config.TextColumn("District Name"),
            "region": st.column_config.TextColumn("Region"),
            "infrastructure_deficit_score": st.column_config.NumberColumn("Deficit Score", format="%.1f"),
            "deficit_tier": st.column_config.TextColumn("Deficit Severity Tier"),
            "road_density": st.column_config.NumberColumn("Road Density", format="%.2f"),
            "congestion_index": st.column_config.NumberColumn("Congestion Index", format="%.1f"),
            "warehouses": st.column_config.NumberColumn("Warehouses", format="%d"),
            "logistics_parks": st.column_config.NumberColumn("Logistics Parks", format="%d"),
            "freight_volume_million_tonnes": st.column_config.NumberColumn("Freight (M Tonnes)", format="%.2f"),
            "recommended_budget_cr": st.column_config.NumberColumn("Rec. Budget (₹ Cr)", format="₹ %,d")
        },
        use_container_width=True,
        hide_index=True
    )

    # Export CSV
    csv_def = f_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=f"📥 Export Infrastructure Deficit Matrix for {selected_year} (CSV)",
        data=csv_def,
        file_name=f"tn_infrastructure_deficit_matrix_{selected_year}.csv",
        mime="text/csv"
    )
if __name__ == "__main__":
    st.set_page_config(
        page_title="FreightOpt - Module 6 Deficit Page",
        page_icon="⚠️",
        layout="wide"
    )
    run_module_6()
