"""
Plotly Data Visualization Components
Provides beautifully styled, high-contrast Plotly charts for Tamil Nadu logistics metrics.
Fixed layout spacing, legend positioning, and outlier scale formatting.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

DARK_TEMPLATE = "plotly_dark"
THEME_BG = "rgba(15, 23, 42, 0)"  # Transparent background
CARD_BORDER = "#334155"

def render_top_districts_bar_chart(df: pd.DataFrame, n: int = 10) -> go.Figure:
    """
    Renders a horizontal gradient bar chart showing the Top N Freight Districts.
    """
    if df.empty:
        return go.Figure()

    top_df = df.sort_values(by="freight_volume_million_tonnes", ascending=True).tail(n)

    fig = px.bar(
        top_df,
        x="freight_volume_million_tonnes",
        y="district_name",
        orientation="h",
        text_auto=".1f",
        color="freight_volume_million_tonnes",
        color_continuous_scale=["#1E3A8A", "#3B82F6", "#60A5FA"],
        labels={"freight_volume_million_tonnes": "Annual Freight (Million Tonnes)", "district_name": "District"},
        title=f"🚛 Top {n} Freight Volume Districts in Tamil Nadu"
    )

    fig.update_layout(
        template=DARK_TEMPLATE,
        paper_bgcolor=THEME_BG,
        plot_bgcolor=THEME_BG,
        margin=dict(l=10, r=20, t=50, b=40),
        font=dict(family="Inter, sans-serif", color="#F8FAFC", size=12),
        coloraxis_showscale=False,
        height=420
    )
    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Freight Volume: <b>%{x:.2f} M Tonnes</b><extra></extra>"
    )
    return fig

def render_regional_freight_donut(regional_df: pd.DataFrame) -> go.Figure:
    """
    Renders a modern donut pie chart of regional freight distribution across TN.
    """
    if regional_df.empty:
        return go.Figure()

    colors = ["#3B82F6", "#34D399", "#FBBF24", "#A855F7", "#EC4899"]

    fig = px.pie(
        regional_df,
        values="total_freight_mton",
        names="region",
        hole=0.5,
        color_discrete_sequence=colors,
        title="🌐 Regional Freight Share Breakdown"
    )

    fig.update_layout(
        template=DARK_TEMPLATE,
        paper_bgcolor=THEME_BG,
        plot_bgcolor=THEME_BG,
        margin=dict(l=20, r=20, t=50, b=40),
        font=dict(family="Inter, sans-serif", color="#F8FAFC", size=12),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="center",
            x=0.5
        ),
        height=420
    )
    fig.update_traces(
        textposition="outside",
        textinfo="percent+label",
        hovertemplate="<b>%{label} Region</b><br>Freight Volume: <b>%{value:.2f} M Tonnes</b> (%{percent})<extra></extra>"
    )
    return fig

def render_congestion_density_scatter(df: pd.DataFrame) -> go.Figure:
    """
    Renders a scatter plot: Road Network Density vs Congestion Index.
    Legend positioned cleanly on top right to avoid overlap.
    """
    if df.empty:
        return go.Figure()

    fig = px.scatter(
        df,
        x="road_density",
        y="congestion_index",
        size="freight_volume_million_tonnes",
        color="region",
        hover_name="district_name",
        color_discrete_sequence=["#3066BE", "#34D399", "#FBBF24", "#A855F7", "#EC4899"],
        labels={
            "road_density": "Road Density (km / 100 sq km)",
            "congestion_index": "Congestion Index",
            "freight_volume_million_tonnes": "Freight Volume (M Tonnes)",
            "region": "Region"
        },
        title="🔍 Infrastructure Matrix: Road Density vs Congestion Bottlenecks"
    )

    fig.update_layout(
        template=DARK_TEMPLATE,
        paper_bgcolor=THEME_BG,
        plot_bgcolor=THEME_BG,
        margin=dict(l=20, r=20, t=60, b=50),
        font=dict(family="Inter, sans-serif", color="#F8FAFC", size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(showgrid=True, gridcolor="#1E293B", title=dict(font=dict(size=11))),
        yaxis=dict(showgrid=True, gridcolor="#1E293B", title=dict(font=dict(size=11))),
        height=450
    )
    fig.update_traces(
        marker=dict(line=dict(width=1, color="#FFFFFF"), opacity=0.85),
        hovertemplate="<b>%{hovertext}</b><br>Road Density: <b>%{x:.2f}</b><br>Congestion Index: <b>%{y:.2f}</b><extra></extra>"
    )
    return fig

def render_warehouse_capacity_chart(regional_df: pd.DataFrame) -> go.Figure:
    """
    Renders a bar chart displaying total Warehouses & Logistics Parks by Region.
    """
    if regional_df.empty:
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=regional_df["region"],
        y=regional_df["total_warehouses"],
        name="Warehouses",
        marker_color="#3B82F6",
        text=regional_df["total_warehouses"],
        textposition="auto"
    ))

    fig.add_trace(go.Bar(
        x=regional_df["region"],
        y=regional_df["total_logistics_parks"],
        name="Logistics Parks",
        marker_color="#FBBF24",
        text=regional_df["total_logistics_parks"],
        textposition="auto"
    ))

    fig.update_layout(
        template=DARK_TEMPLATE,
        paper_bgcolor=THEME_BG,
        plot_bgcolor=THEME_BG,
        barmode="group",
        margin=dict(l=20, r=20, t=60, b=50),
        font=dict(family="Inter, sans-serif", color="#F8FAFC", size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        title="🏭 Logistics Infrastructure: Warehouses & Logistics Parks",
        xaxis_title="Region",
        yaxis_title="Facility Count",
        height=450
    )
    return fig

def render_multiyear_trend_chart(multiyear_df: pd.DataFrame) -> go.Figure:
    """
    Renders a 2020-2026 Freight Volume Growth Trend Line Chart across regions.
    """
    if multiyear_df.empty:
        return go.Figure()

    trend = multiyear_df.groupby(["year", "region"])["freight_volume_million_tonnes"].sum().reset_index()

    fig = px.line(
        trend,
        x="year",
        y="freight_volume_million_tonnes",
        color="region",
        markers=True,
        color_discrete_sequence=["#3B82F6", "#34D399", "#FBBF24", "#A855F7", "#EC4899"],
        labels={"year": "Year", "freight_volume_million_tonnes": "Freight Volume (M Tonnes)", "region": "Region"},
        title="📈 Multi-Year Freight Growth Trajectory (2020 – 2026)"
    )

    fig.update_layout(
        template=DARK_TEMPLATE,
        paper_bgcolor=THEME_BG,
        plot_bgcolor=THEME_BG,
        margin=dict(l=20, r=20, t=60, b=50),
        font=dict(family="Inter, sans-serif", color="#F8FAFC", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=True, gridcolor="#1E293B", dtick=1),
        yaxis=dict(showgrid=True, gridcolor="#1E293B"),
        height=400
    )
    return fig
