"""
Executive Report Generation & Export Engine
Synthesizes analytics across all FreightOpt modules into comprehensive executive Markdown policy documents,
formal plain-text government memorandums (.txt), and multi-format data export suites.
"""

import pandas as pd
from typing import Dict, Any, List
from datetime import datetime

from src.database.repository import get_all_districts_df, get_state_kpis
from src.database.projects_repository import get_all_projects_df
from src.logic.deficit_engine import compute_state_benchmarks, calculate_multi_pillar_deficit, get_deficit_tier
from src.logic.ml_prediction_engine import load_trained_model_payload, generate_statewide_projections_2027_2030
from src.logic.budget_optimizer import optimize_budget_allocation

def generate_executive_report_markdown(
    target_audience: str = "State Cabinet / Chief Minister's Office",
    include_sections: List[str] = None,
    budget_limit_cr: float = 1500.0
) -> str:
    """
    Compiles a rich Markdown executive briefing report (.md).
    """
    if include_sections is None:
        include_sections = ["Executive Summary", "Deficit Analysis", "AI Forecasts", "Budget Optimization", "Recommendations"]

    now_str = datetime.now().strftime("%B %d, %Y")
    
    # Fetch Data
    kpis = get_state_kpis(year=2026)
    districts_df = get_all_districts_df(year=2026)

    # Compute Deficit Top 5
    top_deficit = districts_df.sort_values(by="infrastructure_deficit_score", ascending=False).head(5)

    # ML Payload & Projections
    ml_payload = load_trained_model_payload()
    ml_metrics = ml_payload["metrics"]
    proj_df = generate_statewide_projections_2027_2030()
    proj_2030 = proj_df[proj_df["year"] == 2030]
    total_proj_2030_freight = proj_2030["predicted_freight_mton"].sum()

    # Budget Optimization Result
    opt_res = optimize_budget_allocation(total_budget_cr=budget_limit_cr)
    sel_projects = opt_res.get("selected_projects_df", pd.DataFrame())

    # Build Document Markdown
    doc = []
    doc.append("# 🏛️ GOVERNMENT OF TAMIL NADU")
    doc.append("## HIGH-LEVEL EXECUTIVE LOGISTICS BRIEFING & CAPITAL ALLOCATION STRATEGY")
    doc.append(f"**Document Reference:** `TN-LOG-OPT/2026/EXEC-01` | **Date:** {now_str}")
    doc.append(f"**Target Audience:** {target_audience} | **Classification:** Official Government Policy Briefing\n")

    doc.append("---")

    # Section 1: Executive Summary
    if "Executive Summary" in include_sections:
        doc.append("### 1. Executive Summary & Key Indicators")
        doc.append(f"""
Tamil Nadu's freight movement spans 38 industrial and maritime districts, handling an estimated **{kpis['total_freight_mton']:.1f} Million Tonnes** of cargo in 2026 with a combined Gross District Domestic Product (GDDP) of **₹ {kpis['total_gdp_cr']:,.0f} Cr**.

- **Total State Districts Analyzed:** {kpis['total_districts']} Districts
- **Top Freight Generation Hub:** **{kpis['top_freight_district']}**
- **State Average Road Network Density:** {kpis['avg_road_density']:.2f} km per 100 sq km
- **Average Traffic Congestion Index:** {kpis.get('avg_congestion', 19.8):.1f} / 100
        """)

    # Section 2: Deficit Analysis
    if "Deficit Analysis" in include_sections:
        doc.append("\n### 2. High-Vulnerability Infrastructure Deficit Districts")
        doc.append("Based on multi-pillar deficit index scoring (Road Gap, Congestion Severity, Storage Capacity, Connectivity), the top 5 districts requiring urgent state intervention are:\n")
        
        doc.append("| Rank | District Name | Deficit Score | Congestion Index | Warehouses | Rec. Budget (₹ Cr) |")
        doc.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
        for idx, (_, r) in enumerate(top_deficit.iterrows()):
            doc.append(f"| #{idx+1} | **{r['district_name']}** | `{r['infrastructure_deficit_score']:.1f}` | `{r['congestion_index']:.1f}` | `{r['warehouses']}` | ₹ {r['recommended_budget_cr']:,.0f} Cr |")

    # Section 3: AI Forecasts
    if "AI Forecasts" in include_sections:
        doc.append("\n### 3. AI Machine Learning Freight Demand Forecast (2027 – 2030)")
        doc.append(f"""
Using trained Scikit-Learn **{ml_payload['model_name']} Regressor** AI models (**$R^2$ Accuracy = {ml_metrics['r2']*100:.2f}%**, MAE = {ml_metrics['mae']:.2f} M Tonnes), state cargo volume is projected to grow from **{kpis['total_freight_mton']:.1f} M Tonnes** (2026) to **{total_proj_2030_freight:.1f} M Tonnes** by 2030.

- **Primary Cargo Growth Drivers:** Industrial Output (Weight = {ml_payload['feature_importance_df'].iloc[-1]['importance']:.3f}), GDDP, and Road Network Density.
- **High Growth Corridors:** Western Industrial Cluster (Coimbatore-Tiruppur-Salem) and Northern Maritime Belt (Chennai-Tiruvallur-Chengalpattu).
        """)

    # Section 4: Budget Optimization
    if "Budget Optimization" in include_sections:
        doc.append(f"\n### 4. Optimal Capital Budget Allocation Roadmap (₹ {budget_limit_cr:,.0f} Cr)")
        doc.append(f"""
Scipy Linear Programming (Knapsack Solver) optimized the allocation of **₹ {opt_res['total_allocated_cr']:,.1f} Cr** across **{opt_res['selected_count']} high-impact infrastructure projects** with a capital utilisation rate of **{opt_res['utilisation_pct']:.1f}%**.

- **Estimated State Deficit Score Reduction:** **-{opt_res['predicted_deficit_reduction_pts']:.1f} Points**
- **Portfolio Average ROI Multiplier:** **{opt_res['avg_roi_multiplier']:.2f}x Efficiency Return**
        """)
        
        if not sel_projects.empty:
            doc.append("\n**Key Funded Infrastructure Projects:**\n")
            doc.append("| Project ID | District | Project Title | Category | Cost (₹ Cr) | ROI | Priority |")
            doc.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
            for _, pr in sel_projects.head(8).iterrows():
                doc.append(f"| `{pr['project_id']}` | {pr['district_name']} | {pr['project_name']} | {pr['project_type']} | ₹ {pr['cost_estimate_cr']:,.0f} Cr | `{pr['expected_roi_multiplier']:.1f}x` | {pr['priority_level']} |")

    # Section 5: Recommendations
    if "Recommendations" in include_sections:
        doc.append("\n### 5. Strategic Policy Recommendations")
        doc.append("""
1. **Prioritize Multimodal Freight Corridors**: Fast-track approval for Coimbatore MMLP and Sriperumbudur Heavy Freight Bypass to relieve port & highway chokepoints.
2. **Expand Agro Cold Storage Infrastructure**: Establish cold storage hubs in Salem, Madurai, and Dindigul to reduce post-harvest agricultural wastage.
3. **Institutionalize Multi-Year Predictive Planning**: Integrate AI demand forecasting into state budget formulation cycles.
        """)

    doc.append("\n---")
    doc.append("*Report generated by FreightOpt Strategic Planning System for the Government of Tamil Nadu.*")

    return "\n".join(doc)

def generate_executive_report_plaintext(
    target_audience: str = "State Cabinet / Chief Minister's Office",
    include_sections: List[str] = None,
    budget_limit_cr: float = 1500.0
) -> str:
    """
    Generates a formal, professional plain-text memorandum (.txt) formatted cleanly
    with ASCII dividers, aligned text columns, and official government letterhead.
    Strips raw markdown hashes, pipes, and backticks.
    """
    if include_sections is None:
        include_sections = ["Executive Summary", "Deficit Analysis", "AI Forecasts", "Budget Optimization", "Recommendations"]

    now_str = datetime.now().strftime("%B %d, %Y")
    kpis = get_state_kpis(year=2026)
    districts_df = get_all_districts_df(year=2026)
    top_deficit = districts_df.sort_values(by="infrastructure_deficit_score", ascending=False).head(5)

    ml_payload = load_trained_model_payload()
    ml_metrics = ml_payload["metrics"]
    proj_df = generate_statewide_projections_2027_2030()
    proj_2030 = proj_df[proj_df["year"] == 2030]
    total_proj_2030_freight = proj_2030["predicted_freight_mton"].sum()

    opt_res = optimize_budget_allocation(total_budget_cr=budget_limit_cr)
    sel_projects = opt_res.get("selected_projects_df", pd.DataFrame())

    lines = []
    line_w = 84

    lines.append("=" * line_w)
    lines.append("                        GOVERNMENT OF TAMIL NADU")
    lines.append("             HIGHWAYS AND MINOR PORTS DEPARTMENT / LOGISTICS CELL")
    lines.append("=" * line_w)
    lines.append(f"DOCUMENT REF  : TN-LOG-OPT/2026/EXEC-01")
    lines.append(f"DATE          : {now_str}")
    lines.append(f"TARGET        : {target_audience}")
    lines.append(f"CLASSIFICATION: OFFICIAL GOVERNMENT POLICY BRIEFING")
    lines.append("-" * line_w)
    lines.append("SUBJECT: HIGH-LEVEL LOGISTICS INFRASTRUCTURE & CAPITAL ALLOCATION STRATEGY")
    lines.append("=" * line_w)
    lines.append("")

    # Section 1
    if "Executive Summary" in include_sections:
        lines.append("1. EXECUTIVE SUMMARY & STATE LOGISTICS KEY INDICATORS")
        lines.append("-" * line_w)
        lines.append(f"Tamil Nadu's freight movement spans 38 industrial and maritime districts,")
        lines.append(f"handling an estimated {kpis['total_freight_mton']:.1f} Million Tonnes of cargo in 2026 with a combined")
        lines.append(f"Gross District Domestic Product (GDDP) of Rs. {kpis['total_gdp_cr']:,.0f} Crore.")
        lines.append("")
        lines.append(f"  * Total State Districts Analyzed : {kpis['total_districts']} Districts")
        lines.append(f"  * Top Freight Generation Hub     : {kpis['top_freight_district']}")
        lines.append(f"  * State Average Road Density     : {kpis['avg_road_density']:.2f} km per 100 sq km")
        lines.append(f"  * Average Traffic Congestion     : {kpis.get('avg_congestion', 19.8):.1f} / 100")
        lines.append("")

    # Section 2
    if "Deficit Analysis" in include_sections:
        lines.append("2. HIGH-VULNERABILITY INFRASTRUCTURE DEFICIT DISTRICTS")
        lines.append("-" * line_w)
        lines.append("Based on multi-pillar deficit index scoring (Road Gap, Congestion Severity,")
        lines.append("Storage Capacity, Connectivity Access), the top 5 vulnerable districts are:")
        lines.append("")
        lines.append(f"{'RANK':<6} {'DISTRICT NAME':<18} {'DEFICIT SCORE':<16} {'CONGESTION':<14} {'WAREHOUSES':<12} {'REC. BUDGET':<14}")
        lines.append("-" * line_w)
        for idx, (_, r) in enumerate(top_deficit.iterrows()):
            lines.append(
                f"#{idx+1:<5} {r['district_name']:<18} {r['infrastructure_deficit_score']:<16.1f} "
                f"{r['congestion_index']:<14.1f} {r['warehouses']:<12d} Rs. {r['recommended_budget_cr']:,.0f} Cr"
            )
        lines.append("-" * line_w)
        lines.append("")

    # Section 3
    if "AI Forecasts" in include_sections:
        lines.append("3. AI MACHINE LEARNING FREIGHT DEMAND FORECAST (2027 - 2030)")
        lines.append("-" * line_w)
        lines.append(f"Using trained Scikit-Learn {ml_payload['model_name']} Regressor AI models")
        lines.append(f"(R-Squared Accuracy = {ml_metrics['r2']*100:.2f}%, MAE = {ml_metrics['mae']:.2f} M Tonnes), total cargo")
        lines.append(f"volume is projected to grow from {kpis['total_freight_mton']:.1f} M Tonnes (2026) to {total_proj_2030_freight:.1f} M Tonnes by 2030.")
        lines.append("")
        lines.append(f"  * Primary Cargo Growth Drivers : Industrial Output, GDDP, and Road Density")
        lines.append(f"  * High Growth Corridors        : Western Cluster (Coimbatore-Tiruppur-Salem)")
        lines.append(f"                                   Northern Belt (Chennai-Tiruvallur-Chengalpattu)")
        lines.append("")

    # Section 4
    if "Budget Optimization" in include_sections:
        lines.append(f"4. OPTIMAL CAPITAL BUDGET ALLOCATION ROADMAP (Rs. {budget_limit_cr:,.0f} Crore)")
        lines.append("-" * line_w)
        lines.append(f"Scipy Linear Programming (Knapsack Solver) optimized the allocation of")
        lines.append(f"Rs. {opt_res['total_allocated_cr']:,.1f} Crore across {opt_res['selected_count']} high-impact projects (Utilisation: {opt_res['utilisation_pct']:.1f}%).")
        lines.append("")
        lines.append(f"  * Estimated State Deficit Score Reduction : -{opt_res['predicted_deficit_reduction_pts']:.1f} Points")
        lines.append(f"  * Portfolio Average ROI Multiplier        : {opt_res['avg_roi_multiplier']:.2f}x Efficiency Return")
        lines.append("")
        if not sel_projects.empty:
            lines.append("KEY FUNDED INFRASTRUCTURE PROJECTS:")
            lines.append("-" * line_w)
            lines.append(f"{'ID':<10} {'DISTRICT':<15} {'PROJECT TITLE':<32} {'COST (Rs. Cr)':<14} {'PRIORITY':<10}")
            lines.append("-" * line_w)
            for _, pr in sel_projects.head(8).iterrows():
                title_short = (pr['project_name'][:29] + '...') if len(pr['project_name']) > 31 else pr['project_name']
                lines.append(
                    f"{pr['project_id']:<10} {pr['district_name']:<15} {title_short:<32} "
                    f"Rs. {pr['cost_estimate_cr']:<10,.0f} {pr['priority_level']:<10}"
                )
            lines.append("-" * line_w)
            lines.append("")

    # Section 5
    if "Recommendations" in include_sections:
        lines.append("5. STRATEGIC POLICY RECOMMENDATIONS")
        lines.append("-" * line_w)
        lines.append("1. Fast-track Coimbatore MMLP and Sriperumbudur Heavy Freight Bypass link.")
        lines.append("2. Establish cold storage hubs in Salem, Madurai, and Dindigul for agro exports.")
        lines.append("3. Integrate AI demand forecasting into state annual budget formulation cycles.")
        lines.append("")

    lines.append("=" * line_w)
    lines.append("  Report generated by FreightOpt Strategic Planning System for Government of Tamil Nadu")
    lines.append("=" * line_w)

    return "\n".join(lines)

def get_exportable_datasets() -> Dict[str, pd.DataFrame]:
    """
    Returns dictionary of all master datasets ready for CSV download.
    """
    return {
        "tn_districts_master_2026.csv": get_all_districts_df(year=2026),
        "infrastructure_proposals_registry.csv": get_all_projects_df(),
        "ai_freight_projections_2027_2030.csv": generate_statewide_projections_2027_2030(),
        "optimal_budget_allocation_roadmap.csv": optimize_budget_allocation(1500.0).get("selected_projects_df", pd.DataFrame())
    }

if __name__ == "__main__":
    report_txt = generate_executive_report_plaintext()
    print("Formal Plaintext Report compiled successfully. Character count:", len(report_txt))
