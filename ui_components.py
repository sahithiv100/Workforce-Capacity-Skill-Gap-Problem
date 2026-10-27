"""
ui_components.py
Reusable UI components, custom styling, badges, and Plotly visualization builders
with dark navy/charcoal styling and restrained purple accents.
"""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import numpy as np

# Color Palette Constants
THEME_BG = "#0B0F19"
THEME_CARD = "#111827"
THEME_CARD_BORDER = "#1F2937"
THEME_TEXT = "#F3F4F6"
THEME_MUTED = "#9CA3AF"
COLOR_PURPLE = "#8B5CF6"
COLOR_PURPLE_DARK = "#6D28D9"
COLOR_CYAN = "#06B6D4"
COLOR_RED = "#EF4444"
COLOR_AMBER = "#F59E0B"
COLOR_GREEN = "#10B981"
COLOR_BLUE = "#3B82F6"

SEVERITY_COLORS = {
    "Critical (Immediate Risk)": "#EF4444",
    "High (Strategic Watch)": "#F59E0B",
    "Medium (Manageable)": "#3B82F6",
    "Fulfilled (No Gap)": "#10B981"
}


def apply_custom_styles():
    """
    Injects custom CSS for a dark navy/charcoal theme with purple accents.
    """
    st.markdown("""
        <style>
            /* Main background and font */
            .stApp {
                background-color: #0B0F19;
                color: #F3F4F6;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
            
            /* Sidebar styling */
            section[data-testid="stSidebar"] {
                background-color: #111827 !important;
                border-right: 1px solid #1F2937;
            }
            
            /* Metric Card styling */
            .metric-box {
                background: linear-gradient(135deg, #111827 0%, #161F30 100%);
                border: 1px solid #232D3F;
                border-radius: 10px;
                padding: 18px 20px;
                margin-bottom: 12px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
                position: relative;
                overflow: hidden;
            }
            .metric-box::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 4px;
                height: 100%;
                background: #8B5CF6;
            }
            .metric-title {
                color: #9CA3AF;
                font-size: 0.85rem;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 6px;
            }
            .metric-value {
                color: #FFFFFF;
                font-size: 1.85rem;
                font-weight: 700;
                line-height: 1.2;
            }
            .metric-subtitle {
                color: #A78BFA;
                font-size: 0.82rem;
                margin-top: 6px;
            }
            
            /* Synthetic Demo Warning Banner */
            .synthetic-banner {
                background: linear-gradient(90deg, #3B0764 0%, #1E1B4B 50%, #111827 100%);
                border: 1px solid #7C3AED;
                border-radius: 8px;
                padding: 10px 18px;
                margin-bottom: 22px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .banner-text-main {
                color: #E9D5FF;
                font-weight: 700;
                font-size: 0.90rem;
                letter-spacing: 0.05em;
            }
            .banner-text-sub {
                color: #C4B5FD;
                font-size: 0.80rem;
            }
            
            /* Status Pill Badges */
            .badge-pill {
                display: inline-block;
                padding: 3px 10px;
                border-radius: 9999px;
                font-size: 0.75rem;
                font-weight: 600;
                letter-spacing: 0.03em;
            }
            .badge-critical { background-color: rgba(239, 68, 68, 0.2); color: #FCA5A5; border: 1px solid #EF4444; }
            .badge-high { background-color: rgba(245, 158, 11, 0.2); color: #FCD34D; border: 1px solid #F59E0B; }
            .badge-medium { background-color: rgba(59, 130, 246, 0.2); color: #93C5FD; border: 1px solid #3B82F6; }
            .badge-fulfilled { background-color: rgba(16, 185, 129, 0.2); color: #6EE7B7; border: 1px solid #10B981; }
            .badge-purple { background-color: rgba(139, 92, 246, 0.2); color: #D8B4FE; border: 1px solid #8B5CF6; }
            
            /* Card Containers */
            .content-card {
                background-color: #111827;
                border: 1px solid #1F2937;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 18px;
            }
            
            /* Tabs styling */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
                border-bottom: 1px solid #1F2937;
            }
            .stTabs [data-baseweb="tab"] {
                background-color: #111827;
                border: 1px solid #1F2937;
                border-radius: 6px 6px 0 0;
                color: #9CA3AF;
                padding: 10px 18px;
            }
            .stTabs [aria-selected="true"] {
                background-color: #1F2937 !important;
                color: #C084FC !important;
                border-color: #8B5CF6 !important;
            }
            
            /* Table enhancements */
            div[data-testid="stDataFrame"] {
                border: 1px solid #1F2937;
                border-radius: 8px;
                overflow: hidden;
            }
        </style>
    """, unsafe_allow_html=True)


def render_synthetic_banner():
    """Renders prominent notice required on all pages."""
    st.markdown("""
        <div class="synthetic-banner">
            <div>
                <span class="banner-text-main">⚠️ SYNTHETIC DEMO DATA — NOT REAL COMPANY DATA</span>
                <span class="banner-text-sub">&nbsp;|&nbsp; Illustrative Workforce Prototype for Accenture HR Case Study</span>
            </div>
            <div>
                <span class="badge-pill badge-purple">PROTOTYPE SIMULATION</span>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_kpi_card(title, value, subtitle="", border_color=COLOR_PURPLE):
    """HTML card for key performance metrics."""
    return f"""
        <div class="metric-box" style="border-left: 4px solid {border_color};">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-subtitle">{subtitle}</div>
        </div>
    """


def get_plotly_layout(title="", margin=None):
    """Returns standardized dark plotly layout settings."""
    if margin is None:
        margin = dict(l=40, r=40, t=50, b=40)
    return dict(
        title=dict(text=title, font=dict(color="#F3F4F6", size=15, family="Inter")),
        paper_bgcolor="rgba(17, 24, 39, 0.7)",
        plot_bgcolor="rgba(17, 24, 39, 0.7)",
        font=dict(color="#9CA3AF", family="Inter"),
        margin=margin,
        xaxis=dict(gridcolor="#1F2937", zerolinecolor="#1F2937"),
        yaxis=dict(gridcolor="#1F2937", zerolinecolor="#1F2937"),
        legend=dict(font=dict(color="#D1D5DB"), bgcolor="rgba(17, 24, 39, 0.5)")
    )


def chart_demand_vs_capacity(skill_cap_df):
    """
    Renders timeline chart of aggregated Demand vs Qualified Supply across periods P1-P6.
    """
    periods = [f"P{p} (Wk {p*2-1}-{p*2})" for p in range(1, 7)]
    demand_vals = [skill_cap_df[f"demand_p{p}"].sum() for p in range(1, 7)]
    supply_vals = [skill_cap_df[f"supply_p{p}"].sum() for p in range(1, 7)]
    deficit_vals = [skill_cap_df[f"deficit_p{p}"].sum() for p in range(1, 7)]
    
    fig = go.Figure()
    
    # Net Supply Area
    fig.add_trace(go.Scatter(
        x=periods,
        y=supply_vals,
        mode="lines+markers",
        name="Net Qualified Supply (Hrs)",
        line=dict(color="#10B981", width=3),
        marker=dict(size=8, symbol="circle"),
        fill='tozeroy',
        fillcolor="rgba(16, 185, 129, 0.12)"
    ))
    
    # Project Demand Line
    fig.add_trace(go.Scatter(
        x=periods,
        y=demand_vals,
        mode="lines+markers",
        name="Project Demand (Hrs)",
        line=dict(color="#8B5CF6", width=3, dash="dash"),
        marker=dict(size=8, symbol="diamond")
    ))
    
    # Unmet Deficit Bar
    fig.add_trace(go.Bar(
        x=periods,
        y=deficit_vals,
        name="Unmet Skill Deficit (Hrs)",
        marker_color="rgba(239, 68, 68, 0.65)"
    ))
    
    fig.update_layout(
        **get_plotly_layout("Workforce Capacity vs Project Demand Timeline (Bi-Weekly Periods)"),
        barmode='group',
        hovermode="x unified"
    )
    fig.update_yaxes(title="Total Hours")
    return fig


def chart_skills_matrix_heatmap(employees_df, skills_df):
    """
    Renders skills vs locations heatmap showing qualified headcount.
    """
    locations = sorted(employees_df["location"].unique())
    skills = skills_df["skill_name"].tolist()
    
    # Build 2D matrix of headcount (primary or secondary prof >= 3)
    matrix = np.zeros((len(skills), len(locations)))
    
    for i, s_name in enumerate(skills):
        for j, loc in enumerate(locations):
            subset = employees_df[
                (employees_df["location"] == loc) &
                (
                    ((employees_df["primary_skill_name"] == s_name) & (employees_df["primary_proficiency"] >= 3)) |
                    ((employees_df["secondary_skill_name"] == s_name) & (employees_df["secondary_proficiency"] >= 3))
                )
            ]
            matrix[i][j] = len(subset)
            
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=locations,
        y=skills,
        colorscale=[
            [0.0, "#0B0F19"],
            [0.2, "#1E1B4B"],
            [0.5, "#6D28D9"],
            [0.8, "#8B5CF6"],
            [1.0, "#C4B5FD"]
        ],
        colorbar=dict(title="Qualified Staff"),
        hovertemplate="Location: %{x}<br>Skill: %{y}<br>Headcount: %{z}<extra></extra>"
    ))
    
    fig.update_layout(
        **get_plotly_layout("Global Skills Distribution Heatmap (Proficiency ≥ Level 3)", margin=dict(l=260, r=40, t=50, b=40)),
        height=520
    )
    return fig


def chart_gap_severity_donut(gap_df):
    """
    Renders gap severity distribution donut chart.
    """
    counts = gap_df["severity"].value_counts()
    colors = [SEVERITY_COLORS.get(cat, "#8B5CF6") for cat in counts.index]
    
    fig = go.Figure(data=[go.Pie(
        labels=counts.index,
        values=counts.values,
        hole=0.6,
        marker=dict(colors=colors, line=dict(color="#111827", width=2)),
        textinfo="label+value+percent",
        textfont=dict(color="#F3F4F6", size=11)
    )])
    
    fig.update_layout(
        **get_plotly_layout("Requirement Status & Gap Severity Breakdown"),
        height=340,
        showlegend=False
    )
    return fig


def chart_tradeoff_radar(evaluated_levers):
    """
    Renders radar chart comparing the 5 levers for a specific gap on multiple axes.
    """
    categories = ["Cost Efficiency", "Speed / Deployment", "Firm Retention / IP", "Execution Feasibility"]
    
    fig = go.Figure()
    
    colors = ["#10B981", "#8B5CF6", "#3B82F6", "#F59E0B", "#EC4899"]
    
    for idx, lev in enumerate(evaluated_levers):
        # Normalize attributes 0-100
        # Cost efficiency: inverse of cost relative to max cost
        cost_eff = max(10, 100 - (lev["cost"] / 350.0))
        speed_eff = max(10, 100 - (lev["lead_time_weeks"] * 10))
        strat_eff = 95 if "Upskilling" in lev["lever"] else (80 if "Internal" in lev["lever"] or "Direct" in lev["lever"] else 30)
        feas = float(lev.get("feasibility_val", 0.70)) * 100
        
        vals = [cost_eff, speed_eff, strat_eff, feas]
        vals.append(vals[0]) # close loop
        
        fig.add_trace(go.Scatterpolar(
            r=vals,
            theta=categories + [categories[0]],
            fill='toself',
            name=lev["lever"],
            line=dict(color=colors[idx % len(colors)], width=2),
            opacity=0.65
        ))
        
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(17, 24, 39, 0.6)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="#1F2937", linecolor="#1F2937"),
            angularaxis=dict(gridcolor="#1F2937", linecolor="#1F2937")
        ),
        paper_bgcolor="rgba(17, 24, 39, 0.7)",
        font=dict(color="#9CA3AF", family="Inter"),
        title=dict(text="Multi-Attribute Tradeoff Radar Comparison", font=dict(color="#F3F4F6", size=14)),
        height=380,
        margin=dict(l=60, r=60, t=50, b=40),
        legend=dict(font=dict(size=10))
    )
    return fig


def chart_levers_cost_distribution(recommendations_df):
    """
    Bar chart showing total financial budget recommended across resolution levers.
    """
    summary = recommendations_df.groupby("recommended_lever")["recommended_cost"].sum().reset_index()
    summary = summary.sort_values(by="recommended_cost", ascending=False)
    
    fig = px.bar(
        summary,
        x="recommended_lever",
        y="recommended_cost",
        labels={"recommended_lever": "Strategic Lever", "recommended_cost": "Total Investment ($)"},
        color="recommended_lever",
        color_discrete_sequence=["#8B5CF6", "#06B6D4", "#F59E0B", "#10B981", "#EC4899"]
    )
    
    fig.update_layout(
        **get_plotly_layout("Capital Allocation by Recommended Resolution Strategy"),
        height=320,
        showlegend=False
    )
    fig.update_yaxes(tickprefix="$", title="Capital Allocation")
    return fig
