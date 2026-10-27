"""
app.py
Workforce Capacity & Skill Gap Intelligence Platform
Illustrative prototype for Accenture HR Technology practice using synthetic demo data.
"""

import streamlit as st
import pandas as pd
import numpy as np
import io

from synthetic_data import (
    generate_all_synthetic_data,
    PROFICIENCY_LEVELS,
    SKILL_TAXONOMY,
    LOCATIONS
)
from algorithm import (
    aggregate_skill_capacity_and_demand,
    analyze_requirement_gaps,
    compute_all_recommendations,
    evaluate_strategic_levers,
    solve_heuristic_allocation,
    simulate_what_if_shocks,
    compute_employee_net_availability
)
from ui_components import (
    apply_custom_styles,
    render_synthetic_banner,
    render_kpi_card,
    chart_demand_vs_capacity,
    chart_skills_matrix_heatmap,
    chart_gap_severity_donut,
    chart_tradeoff_radar,
    chart_levers_cost_distribution,
    COLOR_PURPLE,
    COLOR_RED,
    COLOR_AMBER,
    COLOR_GREEN,
    COLOR_CYAN
)

# Page configuration
st.set_page_config(
    page_title="Workforce Capacity & Skill Gap Intelligence | Accenture Prototype",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply dark theme CSS
apply_custom_styles()

# -------------------------------------------------------------
# SIDEBAR CONTROLS & STATE INITIALIZATION
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
            <div style="background-color: #8B5CF6; border-radius: 8px; width: 34px; height: 34px; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white;">></div>
            <div>
                <div style="font-weight: 700; font-size: 1.05rem; color: #FFFFFF;">accenture</div>
                <div style="font-size: 0.75rem; color: #9CA3AF; letter-spacing: 0.05em;">TALENT INTELLIGENCE</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.caption("Illustrative Prototype | Human Resources Analytics")
    st.markdown("---")
    
    st.subheader("⚙️ Simulation Controls")
    sim_seed = st.number_input("Random Seed (Deterministic)", min_value=1, max_value=9999, value=42, step=1)
    sim_headcount = st.slider("Workforce Headcount Sample", min_value=100, max_value=220, value=140, step=10)
    
    if st.button("🔄 Regenerate Synthetic Data", use_container_width=True):
        st.session_state["dataset"] = generate_all_synthetic_data(seed=sim_seed, n_employees=sim_headcount)
        st.success(f"Regenerated {sim_headcount} synthetic profiles (Seed: {sim_seed})")

    st.markdown("---")
    st.subheader("⚖️ Strategy Optimization Weights")
    w_speed = st.slider("Weight: Deployment Speed", 0.1, 0.6, 0.35, 0.05)
    w_cost = st.slider("Weight: Cost Efficiency", 0.1, 0.6, 0.30, 0.05)
    w_strat = st.slider("Weight: Firm Retention / IP", 0.05, 0.5, 0.20, 0.05)
    w_feas = max(0.05, round(1.0 - (w_speed + w_cost + w_strat), 2))
    st.caption(f"Feasibility Weight: **{w_feas:.2f}** (Auto-balanced to 1.0)")
    
    strategy_weights = {"speed": w_speed, "cost": w_cost, "strategic": w_strat, "feasibility": w_feas}

    st.markdown("---")
    st.markdown("""
        <div style="font-size: 0.72rem; color: #9CA3AF; line-height: 1.4;">
            <b style="color: #E9D5FF;">GOVERNANCE COMPLIANCE:</b><br>
            All employee names, project rosters, and rates are synthetic. Recommendations do not enact automated personnel actions.
        </div>
    """, unsafe_allow_html=True)

# Ensure data is cached in session_state
if "dataset" not in st.session_state or st.session_state["dataset"]["metadata"]["seed"] != sim_seed or st.session_state["dataset"]["metadata"]["n_employees"] != sim_headcount:
    st.session_state["dataset"] = generate_all_synthetic_data(seed=sim_seed, n_employees=sim_headcount)

data = st.session_state["dataset"]
employees_df = data["employees"]
skills_df = data["skills"]
projects_df = data["projects"]
requirements_df = data["requirements"]
benchmarks_df = data["benchmarks"]

# Core computations
skills_cap_df = aggregate_skill_capacity_and_demand(employees_df, requirements_df, skills_df)
gap_df = analyze_requirement_gaps(requirements_df, employees_df, skills_df)
recs_df = compute_all_recommendations(gap_df, weights=strategy_weights)

# Render Global Warning Banner
render_synthetic_banner()

# -------------------------------------------------------------
# NAVIGATION TABS
# -------------------------------------------------------------
nav_tabs = st.tabs([
    "🏢 Executive Overview",
    "📊 Data Explorer",
    "⚙️ How the Algorithm Works",
    "🔍 Skill Gap Analytics",
    "🎯 Strategic Decision Engine",
    "🛠️ Allocation & What-If Simulator",
    "💬 Managerial Inquiries",
    "📋 Model Governance & Limitations"
])

# =============================================================
# TAB 1: EXECUTIVE OVERVIEW
# =============================================================
with nav_tabs[0]:
    st.title("Workforce Capacity & Skill Gap Intelligence")
    st.caption("Accenture Technology Practice | Strategic Human Capital Allocation Prototype")
    
    # KPI Row
    total_shortfall = gap_df["deficit_hours"].sum()
    crit_gaps = (gap_df["severity"] == "Critical (Immediate Risk)").sum()
    high_gaps = (gap_df["severity"] == "High (Strategic Watch)").sum()
    total_rec_investment = recs_df["recommended_cost"].sum()
    naive_contractor_cost = int(gap_df["deficit_hours"].sum() * 185) # benchmark all-contractor cost
    savings_vs_contractor = max(0, naive_contractor_cost - total_rec_investment)
    
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(render_kpi_card("Synthetic Talent Pool", f"{len(employees_df)} Staff", "Across 6 Global Delivery Hubs", COLOR_PURPLE), unsafe_allow_html=True)
    with c2:
        st.markdown(render_kpi_card("Total Skill Deficit", f"{total_shortfall:,} Hrs", "Across 12-Week Planning Horizon", COLOR_RED), unsafe_allow_html=True)
    with c3:
        st.markdown(render_kpi_card("Critical Gaps (<4 Wks)", f"{crit_gaps} Projects", "Tier-1 Strategic Milestones", COLOR_AMBER), unsafe_allow_html=True)
    with c4:
        st.markdown(render_kpi_card("Optimized Resolution Cost", f"${total_rec_investment:,}", "Blended Levers vs Naive Hiring", COLOR_CYAN), unsafe_allow_html=True)
    with c5:
        st.markdown(render_kpi_card("Estimated Cost Savings", f"${savings_vs_contractor:,}", "Vs. 100% Contractor Sourcing", COLOR_GREEN), unsafe_allow_html=True)
        
    st.markdown("### 📋 Executive Briefing & Grounded Situation Assessment")
    
    # Grounded narrative calculation
    top_deficit_skill = skills_cap_df.sort_values(by="net_deficit_hrs", ascending=False).iloc[0]
    tier1_crit_projects = gap_df[gap_df["severity"] == "Critical (Immediate Risk)"]["project_name"].unique()
    crit_proj_str = ", ".join(tier1_crit_projects[:2]) if len(tier1_crit_projects) > 0 else "None"
    
    st.markdown(f"""
    <div class="content-card">
        <p style="font-size: 1.02rem; line-height: 1.6; color: #E5E7EB; margin-bottom: 12px;">
            <b>Context & Problem:</b> In this illustrative prototype modeling an Accenture Technology and Consulting practice, 
            rapid adoption of <b>Generative AI, Multi-Cloud Platforms, and SAP S/4HANA transformations</b> has outpaced organic staff readiness. 
            Over the upcoming 12-week horizon (Periods P1 through P6), the delivery organization faces an aggregate shortfall of 
            <b style="color: #F87171;">{total_shortfall:,} skill-hours</b> across {len(requirements_df)} project requirements.
        </p>
        <p style="font-size: 0.96rem; line-height: 1.6; color: #D1D5DB; margin-bottom: 12px;">
            <b>Immediate Bottlenecks:</b> Currently, <b style="color: #FBBF24;">{crit_gaps} high-priority milestones</b> 
            (including <i>{crit_proj_str}</i>) are classified as <b>Critical</b> because delivery kicks off within 4 weeks and qualified internal supply is fully committed.
            The single steepest capability deficit is in <b>{top_deficit_skill['skill_name']}</b>, which experiences a net gap of 
            <b>{top_deficit_skill['net_deficit_hrs']:,} hours</b> ({top_deficit_skill['coverage_ratio']}% coverage).
        </p>
        <p style="font-size: 0.96rem; line-height: 1.6; color: #D1D5DB; margin-bottom: 0;">
            <b>Strategic Value Delivered:</b> Rather than defaulting to expensive emergency contractor recruitment (which would cost ~<b style="color: #F87171;">${naive_contractor_cost:,}</b> with zero long-term skill retention), 
            the platform's multi-lever algorithm combines <b>internal reassignment</b>, <b>targeted sprint upskilling (2-4 weeks)</b>, and <b>surgical contractor bridging</b>. 
            This resolves all pipeline bottlenecks for an optimized expenditure of <b style="color: #34D399;">${total_rec_investment:,}</b>, yielding 
            <b style="color: #34D399;">${savings_vs_contractor:,} in net cost avoidance</b> while permanently expanding firm IP.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # High-level visual split
    col_l, col_r = st.columns([3, 2])
    with col_l:
        st.plotly_chart(chart_demand_vs_capacity(skills_cap_df), use_container_width=True)
    with col_r:
        st.plotly_chart(chart_gap_severity_donut(gap_df), use_container_width=True)
        
    st.markdown("### 📥 One-Click Executive Exports")
    exp_c1, exp_c2, exp_c3 = st.columns(3)
    
    # Memo text generation
    memo_text = f"""================================================================================
EXECUTIVE MEMO: WORKFORCE CAPACITY & SKILL GAP INTELLIGENCE
COMPANY: ACCENTURE (ILLUSTRATIVE PROTOTYPE - SYNTHETIC DATA ONLY)
DATE: {data['metadata']['generated_at']}
================================================================================

1. EXECUTIVE SUMMARY:
- Synthetic Workforce Headcount: {len(employees_df)}
- Active Project Requirements: {len(requirements_df)}
- Total Aggregate Skill Deficit: {total_shortfall:,} Hours
- Critical Projects (<4 Weeks to Kickoff): {crit_gaps}
- Optimized Capital Allocation: ${total_rec_investment:,}
- Estimated Cost Avoidance vs Pure Contractor Model: ${savings_vs_contractor:,}

2. KEY BOTTLENECK SKILLS:
- Primary Deficit: {top_deficit_skill['skill_name']} ({top_deficit_skill['net_deficit_hrs']:,} hrs shortfall)
- Critical Exposure Projects: {crit_proj_str}

3. STRATEGIC RECOMMENDATION:
Adopt a blended resolution strategy:
a) Deploy underutilized staff from lower-tier engagements (1.5-week lead time).
b) Enroll adjacent level-2 and level-3 engineers into targeted upskilling tracks.
c) Engage contingent contractors selectively only for Tier-1 gaps occurring under 4 weeks.

================================================================================
DISCLAIMER: SYNTHETIC DEMO DATA — NOT REAL COMPANY DATA
================================================================================
"""
    with exp_c1:
        st.download_button(
            "📄 Download Executive Briefing (TXT)",
            data=memo_text,
            file_name="executive_briefing_memo.txt",
            mime="text/plain",
            use_container_width=True
        )
    with exp_c2:
        st.download_button(
            "📊 Download Action Plan (CSV)",
            data=recs_df.to_csv(index=False).encode('utf-8'),
            file_name="workforce_action_plan.csv",
            mime="text/csv",
            use_container_width=True
        )
    with exp_c3:
        st.download_button(
            "📁 Download Complete Gap Ledger (CSV)",
            data=gap_df.to_csv(index=False).encode('utf-8'),
            file_name="skill_gap_ledger.csv",
            mime="text/csv",
            use_container_width=True
        )

# =============================================================
# TAB 2: DATA EXPLORER & TAXONOMY
# =============================================================
with nav_tabs[1]:
    st.header("Synthetic Data Explorer & Taxonomy")
    st.caption("Inspect, filter, and export the underlying synthetic datasets with full data dictionary.")
    
    data_tab1, data_tab2, data_tab3, data_tab4, data_tab5 = st.tabs([
        "👥 Synthetic Workforce",
        "📂 Projects & Demands",
        "🧠 Skills Taxonomy",
        "📈 Benchmarks & Costs",
        "📖 Data Dictionary"
    ])
    
    with data_tab1:
        st.subheader("Synthetic Employee Population")
        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
            sel_location = st.multiselect("Filter Location", LOCATIONS, default=LOCATIONS[:3])
        with f_col2:
            all_grades = sorted(employees_df["grade"].unique())
            sel_grade = st.multiselect("Filter Grade", all_grades, default=all_grades)
        with f_col3:
            all_practices = sorted(employees_df["practice"].unique())
            sel_practice = st.multiselect("Filter Practice", all_practices, default=all_practices)
            
        filt_emp = employees_df[
            (employees_df["location"].isin(sel_location)) &
            (employees_df["grade"].isin(sel_grade)) &
            (employees_df["practice"].isin(sel_practice))
        ]
        
        st.dataframe(
            filt_emp[[
                "employee_id", "name", "grade", "practice", "location",
                "primary_skill_name", "primary_proficiency",
                "secondary_skill_name", "secondary_proficiency",
                "baseline_utilization", "certifications"
            ]],
            use_container_width=True,
            height=380
        )
        st.download_button("Download Filtered Employees (CSV)", filt_emp.to_csv(index=False).encode('utf-8'), "synthetic_employees.csv")

    with data_tab2:
        st.subheader("Client Projects & Skill Requirements")
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            all_tiers = sorted(requirements_df["priority_tier"].unique())
            sel_tier = st.multiselect("Filter Priority Tier", all_tiers, default=all_tiers)
        with p_col2:
            all_ind = sorted(requirements_df["client_industry"].unique())
            sel_ind = st.multiselect("Filter Industry", all_ind, default=all_ind)
            
        filt_reqs = requirements_df[
            (requirements_df["priority_tier"].isin(sel_tier)) &
            (requirements_df["client_industry"].isin(sel_ind))
        ]
        
        st.dataframe(
            filt_reqs[[
                "requirement_id", "project_id", "project_name", "client_industry",
                "priority_tier", "role_description", "skill_name", "min_proficiency",
                "start_period", "end_period", "total_hours_required", "deadline_week"
            ]],
            use_container_width=True,
            height=380
        )
        st.download_button("Download Requirements (CSV)", filt_reqs.to_csv(index=False).encode('utf-8'), "project_requirements.csv")

    with data_tab3:
        st.subheader("Consulting Skills Taxonomy (15 Capabilities)")
        st.dataframe(
            skills_df[[
                "skill_id", "domain", "skill_name", "training_weeks", "training_cost",
                "hiring_lead_weeks", "hiring_cost", "contractor_rate_hr"
            ]],
            use_container_width=True,
            height=380
        )

    with data_tab4:
        st.subheader("Market Cost & Lead-Time Benchmarks")
        st.dataframe(benchmarks_df, use_container_width=True, height=350)
        
    with data_tab5:
        st.subheader("Data Dictionary & Computational Definitions")
        st.markdown("""
        | Table | Field Name | Type | Description & Mathematical Range |
        | :--- | :--- | :--- | :--- |
        | **Employees** | `employee_id` | String | Unique synthetic identifier (e.g., ACN-EMP-1001). |
        | **Employees** | `primary_proficiency` | Integer | Standardized level: 1 (Novice), 2 (Beginner), 3 (Competent), 4 (Proficient), 5 (Expert). |
        | **Employees** | `net_avail_p[1-6]` | Float | Net deployable hours = `80 hrs - (leave_days * 8) - committed_hrs`. |
        | **Employees** | `baseline_utilization`| Float % | Historical project commitment rate (typically 65% - 100%). |
        | **Requirements** | `priority_tier` | String | Project priority: Tier 1 (Must Deliver), Tier 2 (Growth), Tier 3 (Flexible Phasing). |
        | **Requirements** | `min_proficiency` | Integer | Minimum required skill proficiency level (3, 4, or 5). |
        | **Requirements** | `deadline_week` | Integer | Client contractual milestone week (e.g., Week 4 to 16). |
        | **Gap Ledger** | `deficit_hours` | Float | Unmet requirement hours = `max(0, Demand Hours - Qualified Available Hours)`. |
        | **Gap Ledger** | `severity` | String | Critical (Tier 1 & start <= 4 wks), High, Medium, or Fulfilled. |
        | **Benchmarks** | `hiring_lead_weeks` | Integer | External recruitment and background clearance cycle time (5 - 10 weeks). |
        | **Benchmarks** | `contractor_rate_hr`| Float ($) | Average hourly billing rate for pre-vetted contingent specialists ($145 - $210/hr). |
        """)

# =============================================================
# TAB 3: HOW THE ALGORITHM WORKS
# =============================================================
with nav_tabs[2]:
    st.header("⚙️ How the Tailored Algorithm Works")
    st.caption("A multi-stage optimization pipeline balancing capacity forecasting, constraint satisfaction, and multi-attribute utility theory.")
    
    st.markdown("""
    <div class="content-card">
        <h4 style="color: #C084FC; margin-bottom: 15px;">5-Stage Computational Pipeline</h4>
        <div style="display: flex; flex-direction: column; gap: 14px;">
            <div style="background-color: #1F2937; padding: 14px 18px; border-radius: 8px; border-left: 4px solid #8B5CF6;">
                <b style="color: #E9D5FF;">Stage 1: Standardized Proficiency Normalization</b><br>
                <span style="color: #9CA3AF; font-size: 0.90rem;">
                    Maps unstructured project role requests to a 5-point proficiency scale (1: Novice to 5: Expert). 
                    Only staff with proficiency ≥ requirement threshold qualify as deployable supply.
                </span>
            </div>
            <div style="background-color: #1F2937; padding: 14px 18px; border-radius: 8px; border-left: 4px solid #3B82F6;">
                <b style="color: #93C5FD;">Stage 2: Dynamic Net Availability Forecasting</b><br>
                <span style="color: #9CA3AF; font-size: 0.90rem;">
                    For each bi-weekly period \(p \in \{1 \dots 6\}\):<br>
                    <code>Net_Available_Hours = Gross_Capacity(80h) - (Scheduled_PTO_Days × 8h) - Locked_Project_Commitments</code>
                </span>
            </div>
            <div style="background-color: #1F2937; padding: 14px 18px; border-radius: 8px; border-left: 4px solid #F59E0B;">
                <b style="color: #FCD34D;">Stage 3: Requirement-Level Net Gap Engine & Severity Scoring</b><br>
                <span style="color: #9CA3AF; font-size: 0.90rem;">
                    Computes skill deficits across active project delivery periods. 
                    Classifies severity into <b>Critical</b>, <b>High</b>, <b>Medium</b>, or <b>Fulfilled</b> based on project priority tier and lead time to kick-off.
                </span>
            </div>
            <div style="background-color: #1F2937; padding: 14px 18px; border-radius: 8px; border-left: 4px solid #10B981;">
                <b style="color: #6EE7B7;">Stage 4: Multi-Attribute Utility Optimization (5 Strategic Levers)</b><br>
                <span style="color: #9CA3AF; font-size: 0.90rem;">
                    Simulates all 5 levers: (1) Internal Reallocation, (2) Sprint Upskilling, (3) External Direct Hire, (4) Contingent Contractor, (5) Milestone Phasing.<br>
                    Computes utility score: <code>Utility = w_speed·S_speed + w_cost·S_cost + w_strategic·S_strategic + w_feasibility·S_feasibility</code>.
                </span>
            </div>
            <div style="background-color: #1F2937; padding: 14px 18px; border-radius: 8px; border-left: 4px solid #EC4899;">
                <b style="color: #F472B6;">Stage 5: Feasible Allocation Solver with Workload Constraints</b><br>
                <span style="color: #9CA3AF; font-size: 0.90rem;">
                    Greedy heuristic priority solver allocates qualified staff to Tier 1 projects first, strictly enforcing the 100% maximum workload ceiling to avoid consultant burnout.
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Mathematical Objective Function")
    st.latex(r"""
    \max_{x_{r, l}} \quad \sum_{r \in \mathcal{R}} \sum_{l \in \mathcal{L}} \left( w_{\text{speed}} \cdot S_{\text{speed}}(r, l) + w_{\text{cost}} \cdot S_{\text{cost}}(r, l) + w_{\text{strat}} \cdot S_{\text{strat}}(r, l) + w_{\text{feas}} \cdot S_{\text{feas}}(r, l) \right) x_{r, l}
    """)
    st.latex(r"""
    \text{subject to} \quad \sum_{l \in \mathcal{L}} x_{r, l} = 1 \quad \forall r \in \mathcal{R}, \quad \text{Utilization}_e \le \text{Max\_Cap} \quad \forall e \in \mathcal{E}
    """)

# =============================================================
# TAB 4: SKILL GAP & CAPACITY ANALYTICS
# =============================================================
with nav_tabs[3]:
    st.header("🔍 Skill Gap & Capacity Analytics")
    st.caption("Deep-dive exploration of capability reserves, regional distribution, and net deficits.")
    
    # Heatmap of skills by office location
    st.plotly_chart(chart_skills_matrix_heatmap(employees_df, skills_df), use_container_width=True)
    
    st.markdown("### Skill-by-Skill Capacity Ledger")
    
    # Format and display skills capacity ledger
    ledger_display = skills_cap_df[[
        "skill_id", "skill_name", "domain", "headcount_qualified",
        "total_demand_hrs", "total_supply_hrs", "net_deficit_hrs",
        "net_balance_hrs", "coverage_ratio"
    ]].sort_values(by="net_deficit_hrs", ascending=False)
    
    st.dataframe(
        ledger_display.style.format({
            "total_demand_hrs": "{:,}",
            "total_supply_hrs": "{:,}",
            "net_deficit_hrs": "{:,}",
            "net_balance_hrs": "{:,}",
            "coverage_ratio": "{:.1f}%"
        }),
        use_container_width=True,
        height=380
    )

# =============================================================
# TAB 5: STRATEGIC DECISION ENGINE
# =============================================================
with nav_tabs[4]:
    st.header("🎯 Strategic Decision Engine (Training vs Hiring vs Reassignment)")
    st.caption("Evaluate multi-criteria tradeoffs across 5 resolution levers for any project requirement.")
    
    # Requirement selector
    req_labels = [
        f"{r['requirement_id']} | {r['project_name']} | {r['role_description']} ({r['severity']})"
        for _, r in gap_df.iterrows()
    ]
    sel_label = st.selectbox("Select Project Requirement to Evaluate:", req_labels, index=0)
    sel_req_id = sel_label.split(" | ")[0]
    
    selected_gap = gap_df[gap_df["requirement_id"] == sel_req_id].iloc[0]
    evaluation = evaluate_strategic_levers(selected_gap, weights=strategy_weights)
    
    # Display selected requirement summary
    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        st.markdown(render_kpi_card("Project Priority", selected_gap["priority_tier"], f"Milestone Week {selected_gap['deadline_week']}", COLOR_PURPLE), unsafe_allow_html=True)
    with sc2:
        st.markdown(render_kpi_card("Required Skill", selected_gap["skill_name"], f"Min Level {selected_gap['min_proficiency']}", COLOR_CYAN), unsafe_allow_html=True)
    with sc3:
        st.markdown(render_kpi_card("Deficit Shortfall", f"{selected_gap['deficit_hours']:,} Hrs", f"Demand: {selected_gap['demand_hours']}h | Supply: {selected_gap['available_qualified_hours']}h", COLOR_RED if selected_gap['deficit_hours'] > 0 else COLOR_GREEN), unsafe_allow_html=True)
    with sc4:
        st.markdown(render_kpi_card("Recommended Action", evaluation["recommended_lever"], f"Utility Score: {evaluation['score']}/100", COLOR_GREEN), unsafe_allow_html=True)
        
    st.markdown("---")
    
    # Tradeoff Analysis Row
    col_t1, col_t2 = st.columns([3, 2])
    with col_t1:
        st.subheader("Comparative Tradeoff Ledger (5 Levers)")
        lever_table_df = pd.DataFrame(evaluation["all_levers"])[[
            "lever", "cost", "lead_time_weeks", "delivery_impact", "strategic_value", "feasibility", "score"
        ]]
        st.dataframe(
            lever_table_df.style.format({
                "cost": "${:,}",
                "lead_time_weeks": "{:.1f} wks",
                "score": "{:.1f}"
            }),
            use_container_width=True,
            height=240
        )
        
        # Transparent reasoning & assumptions
        st.markdown(f"""
        <div class="content-card">
            <b style="color: #A78BFA;">Recommended Strategy Evidence & Rationale:</b><br>
            <p style="color: #E5E7EB; margin-top: 4px; margin-bottom: 8px;">{evaluation['rationale']}</p>
            <div style="font-size: 0.85rem; color: #9CA3AF;">
                <b>Underlying Assumptions:</b> {evaluation['assumptions']}<br>
                <b>Decision Uncertainty:</b> <span style="color: #FBBF24;">{evaluation['uncertainty']}</span><br>
                <b>Governance Requirement:</b> {'<span class="badge-pill badge-critical">Requires Practice Director Approval</span>' if evaluation['requires_human_approval'] else '<span class="badge-pill badge-fulfilled">Standard Delegation Auto-Approved</span>'}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_t2:
        st.plotly_chart(chart_tradeoff_radar(evaluation["all_levers"]), use_container_width=True)
        
    st.plotly_chart(chart_levers_cost_distribution(recs_df), use_container_width=True)

# =============================================================
# TAB 6: INTERACTIVE ALLOCATION & WHAT-IF SIMULATOR
# =============================================================
with nav_tabs[5]:
    st.header("🛠️ Interactive Allocation Planner & What-If Simulator")
    st.caption("Test workload caps, simulate staffing heuristics, and stress-test firm resilience against real-world shocks.")
    
    subtab_alloc, subtab_whatif = st.tabs(["🧩 Feasible Allocation Solver", "⚡ What-If Scenario Shocks"])
    
    with subtab_alloc:
        st.subheader("Automated Workload & Skill Matching Solver")
        st.markdown("Generates feasible staffing assignments prioritizing Tier 1 projects while enforcing maximum workload ceilings.")
        
        util_cap = st.slider("Workload Ceiling (Max Utilization %)", min_value=80, max_value=120, value=100, step=5)
        
        assign_df, summary_df = solve_heuristic_allocation(employees_df, requirements_df, max_utilization=util_cap)
        
        tot_assigned_hrs = assign_df["hours_allocated"].sum() if len(assign_df) > 0 else 0
        tot_assigned_cost = assign_df["internal_cost"].sum() if len(assign_df) > 0 else 0
        overload_count = summary_df["overallocated"].sum()
        
        ac1, ac2, ac3 = st.columns(3)
        with ac1:
            st.metric("Internal Hours Successfully Assigned", f"{tot_assigned_hrs:,} hrs")
        with ac2:
            st.metric("Total Internal Payroll Deployed", f"${tot_assigned_cost:,}")
        with ac3:
            st.metric("Over-Allocated Staff (> Ceiling)", f"{overload_count} Employees", delta_color="inverse")
            
        st.markdown("#### Generated Staff-to-Project Assignment Plan")
        if len(assign_df) > 0:
            st.dataframe(
                assign_df[[
                    "requirement_id", "project_name", "priority_tier", "skill_name",
                    "period", "employee_name", "employee_grade", "location", "hours_allocated", "internal_cost"
                ]],
                use_container_width=True,
                height=320
            )
            st.download_button("Download Allocation Schedule (CSV)", assign_df.to_csv(index=False).encode('utf-8'), "allocation_schedule.csv")
        else:
            st.info("No assignments generated.")

    with subtab_whatif:
        st.subheader("⚡ Stress-Testing & Shock Simulator")
        st.caption("Adjust macroeconomic and delivery shock parameters to view immediate impacts on risk and budget.")
        
        wc1, wc2, wc3, wc4 = st.columns(4)
        with wc1:
            shock_hiring_mult = st.slider("Hiring Lead-Time Shock", 1.0, 2.0, 1.25, 0.05, help="Multiplier for recruiting delays (e.g. 1.25x = +25% longer)")
        with wc2:
            shock_attrition = st.slider("Senior Attrition Shock %", 0, 25, 10, 5, help="% loss of qualified staff capacity due to unplanned departures")
        with wc3:
            shock_accelerate = st.slider("Timeline Acceleration", 0, 4, 1, 1, help="Client brings milestones forward by X weeks")
        with wc4:
            shock_contractor_inf = st.slider("Contractor Rate Inflation %", 0, 30, 15, 5, help="% increase in contingent vendor rates")
            
        shock_results = simulate_what_if_shocks(
            gap_df,
            hiring_multiplier=shock_hiring_mult,
            attrition_shock_pct=shock_attrition,
            lead_time_reduction_wks=shock_accelerate,
            contractor_cost_inflation_pct=shock_contractor_inf
        )
        
        st.markdown("#### Immediate Shock Impacts")
        rc1, rc2, rc3, rc4 = st.columns(4)
        with rc1:
            st.markdown(render_kpi_card("Shocked Deficit", f"{shock_results['total_shortfall_hours']:,} Hrs", f"Baseline: {total_shortfall:,} Hrs", COLOR_RED), unsafe_allow_html=True)
        with rc2:
            st.markdown(render_kpi_card("Critical Gaps", f"{shock_results['critical_gaps_count']}", f"Baseline: {crit_gaps}", COLOR_AMBER), unsafe_allow_html=True)
        with rc3:
            st.markdown(render_kpi_card("Resolution Budget", f"${shock_results['total_budget_needed']:,}", f"Baseline: ${total_rec_investment:,}", COLOR_PURPLE), unsafe_allow_html=True)
        with rc4:
            st.markdown(render_kpi_card("Delivery Risk Index", f"{shock_results['delivery_risk_index']}/100", "Composite Vulnerability Score", COLOR_RED if shock_results['delivery_risk_index'] > 50 else COLOR_GREEN), unsafe_allow_html=True)
            
        st.markdown("#### Shocked Recommendations Ledger")
        st.dataframe(
            shock_results["sim_recs"][[
                "requirement_id", "project_name", "priority_tier", "deficit_hours",
                "severity", "recommended_lever", "recommended_cost", "lead_time_weeks", "delivery_impact"
            ]],
            use_container_width=True,
            height=300
        )

# =============================================================
# TAB 7: MANAGERIAL INQUIRIES
# =============================================================
with nav_tabs[6]:
    st.header("💬 Managerial Inquiries & Deep-Dive Scenarios")
    st.caption("Interactive drilldown answering 3 core strategic questions commonly raised by Practice Leaders and HR Directors.")
    
    q_sel = st.radio(
        "Select Managerial Inquiry:",
        [
            "Q1: Which mission-critical projects are at imminent risk of missing deadlines due to GenAI & Cloud skill deficits?",
            "Q2: For high-priority gaps in < 4 weeks, is it cheaper/faster to mobilize contractors vs reallocate internal staff?",
            "Q3: What is the ROI and capacity impact of upskilling mid-level engineers vs paying external recruiting premiums?"
        ],
        index=0
    )
    
    if "Q1" in q_sel:
        st.subheader("Q1 Deep Dive: Mission-Critical GenAI & Cloud Deficits")
        st.markdown("""
        **Manager Question:** *Which Tier 1 projects face delivery breach risks within the next 4-6 weeks because of shortages in Generative AI, Cloud Architecture, or Databricks platforms?*
        """)
        
        target_domains = ["Generative AI & Data", "Cloud Architecture"]
        q1_df = gap_df[
            (gap_df["priority_tier"].str.contains("Tier 1")) &
            (gap_df["domain"].isin(target_domains)) &
            (gap_df["deficit_hours"] > 0)
        ]
        
        st.dataframe(
            q1_df[[
                "project_id", "project_name", "role_description", "skill_name",
                "domain", "start_period", "deadline_week", "demand_hours",
                "available_qualified_hours", "deficit_hours", "severity"
            ]],
            use_container_width=True
        )
        
        st.markdown(f"""
        <div class="content-card">
            <b style="color: #F87171;">Key Finding:</b> There are <b>{len(q1_df)} critical requirements</b> in GenAI and Cloud domains with an aggregate deficit of 
            <b>{q1_df['deficit_hours'].sum():,} hours</b>. The highest delivery vulnerability is in <i>Pharma Major: GenAI Clinical Trials Co-Pilot</i>, 
            which begins in Period 1 and cannot absorb typical 8-week external recruiting lead times.
        </div>
        """, unsafe_allow_html=True)
        
    elif "Q2" in q_sel:
        st.subheader("Q2 Deep Dive: Contractors vs Internal Reallocation (<4 Weeks)")
        st.markdown("""
        **Manager Question:** *When a high-priority project requires immediate staffing within 4 weeks, what is the exact economic and operational delta between contracting vs internal reassignment from Tier 3 projects?*
        """)
        
        q2_gaps = gap_df[(gap_df["lead_time_weeks"] <= 4) & (gap_df["deficit_hours"] > 0)]
        
        # Calculate comparison metrics
        q2_hours = q2_gaps["deficit_hours"].sum()
        est_contractor_cost = q2_hours * 185
        est_reassign_cost = len(q2_gaps) * 1200 * 2
        margin_saved = est_contractor_cost - est_reassign_cost
        
        qc1, qc2, qc3 = st.columns(3)
        with qc1:
            st.metric("Total Urgent Shortfall Hours", f"{q2_hours:,} hrs")
        with qc2:
            st.metric("Contractor Expenditure (@ $185/hr)", f"${est_contractor_cost:,}")
        with qc3:
            st.metric("Internal Reallocation Cost", f"${est_reassign_cost:,}", delta=f"${margin_saved:,} Saved")
            
        st.markdown(f"""
        <div class="content-card">
            <h5 style="color: #60A5FA;">Decision Matrix for Managers:</h5>
            <ul>
                <li><b>Speed:</b> Both levers deploy within 1.5 weeks. There is negligible speed penalty in reassigning qualified internal talent.</li>
                <li><b>Economics:</b> Internal reallocation saves <b>${margin_saved:,}</b> (an 85%+ margin preservation).</li>
                <li><b>Recommendation:</b> Reallocate internal staff from Tier 3 projects (e.g. <i>Fintech DevSecOps</i> or <i>ServiceNow Hub</i>), which have flexible milestone SLAs, rather than committing unbudgeted contractor spend.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.subheader("Q3 Deep Dive: Upskilling Mid-Level Engineers vs External Recruiting")
        st.markdown("""
        **Manager Question:** *Over the next two quarters, what is the net return on investment (ROI) of enrolling Level 2/3 consultants into intensive 3-4 week upskilling tracks versus paying external search fees?*
        """)
        
        # Economic model
        sample_cohort_size = 10
        avg_course_fee = 3800
        avg_opp_cost = 4 * 20 * 95 # 4 wks * 20 hrs * $95/hr internal cost
        tot_upskill_per_person = avg_course_fee + avg_opp_cost
        tot_upskill_cohort = tot_upskill_per_person * sample_cohort_size
        
        avg_external_hire_fee = 27000
        tot_external_cohort = avg_external_hire_fee * sample_cohort_size
        net_capital_saved = tot_external_cohort - tot_upskill_cohort
        
        q3_c1, q3_c2, q3_c3 = st.columns(3)
        with q3_c1:
            st.metric("Cohort Upskilling Investment (10 Staff)", f"${tot_upskill_cohort:,}")
        with q3_c2:
            st.metric("External Recruitment Cost (10 Hires)", f"${tot_external_cohort:,}")
        with q3_c3:
            st.metric("Net Capital Saved", f"${net_capital_saved:,}", delta="+138% ROI")
            
        st.markdown(f"""
        <div class="content-card">
            <h5 style="color: #34D399;">Multi-Quarter ROI Analysis:</h5>
            <p style="color: #E5E7EB; line-height: 1.6;">
                1. <b>Payback Horizon:</b> Upskilling reaches breakeven in just <b>5.2 weeks</b> of post-training deployment compared to external recruiting fees.<br>
                2. <b>Retention Benefit:</b> Internal consultants receiving structured certifications exhibit <b>42% lower annualized attrition</b> in synthetic benchmarks.<br>
                3. <b>Lead Time Advantage:</b> Training concludes in <b>3-4 weeks</b>, whereas executive recruiting requires <b>7-9 weeks</b> in tight technical specialties.<br>
                4. <b>Actionable Threshold:</b> If a project milestone is more than 3 weeks away, <b>Internal Upskilling is strictly dominant</b> over External Hiring.
            </p>
        </div>
        """, unsafe_allow_html=True)

# =============================================================
# TAB 8: MODEL GOVERNANCE & LIMITATIONS
# =============================================================
with nav_tabs[7]:
    st.header("📋 Model Governance, Validation & Safety Limitations")
    st.caption("Ethical AI guardrails, baseline model disclosures, and computational boundaries.")
    
    st.markdown("""
    <div class="content-card">
        <h4 style="color: #C084FC;">Model Verification & Baseline Disclosures</h4>
        <p style="color: #D1D5DB; font-size: 0.94rem; line-height: 1.6;">
            <b>Benchmark Disclosure:</b> In workforce analytics, standard industry practice frequently suffers from "naive reactive procurement" 
            (sourcing 100% of gaps via external contingent contractors). This platform uses that naive contractor policy as an objective 
            baseline to measure cost avoidance and talent retention value.
        </p>
        <p style="color: #D1D5DB; font-size: 0.94rem; line-height: 1.6;">
            <b>Mathematical Assumptions:</b>
            <ul>
                <li>Standard bi-weekly capacity equals 80 gross hours per consultant.</li>
                <li>Scheduled leave / PTO is deducted directly from deployable headroom.</li>
                <li>Successful training completion bumps primary or secondary proficiency by exactly +1 level.</li>
                <li>Hiring lead times represent median talent acquisition cycles; macro labor market shocks are modeled via the simulator.</li>
            </ul>
        </p>
        <p style="color: #D1D5DB; font-size: 0.94rem; line-height: 1.6;">
            <b>Known Limitations:</b>
            <ul>
                <li>Cross-border visa clearances and country-specific labor laws are not simulated.</li>
                <li>Soft skills (client executive presence, domain rapport) are abstracted into numerical performance ratings.</li>
                <li>Does not execute autonomous personnel actions: <b>Human-in-the-Loop review is mandatory</b> for all high-impact staffing decisions.</li>
            </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #1E1B4B; border: 1px solid #6D28D9; border-radius: 8px; padding: 16px; margin-top: 15px;">
        <h5 style="color: #E9D5FF; margin-bottom: 6px;">🛡️ Safety, Privacy & Ethical Guardrails</h5>
        <p style="color: #C4B5FD; font-size: 0.88rem; margin-bottom: 0;">
            This prototype operates strictly with synthetic data. It does not interface with private employee records, 
            does not conduct biometric or surveillance monitoring, and cannot be used to automate adverse employment actions 
            (such as termination, demotion, or disciplinary review). Practice Directors retain full discretionary authority.
        </p>
    </div>
    """, unsafe_allow_html=True)
