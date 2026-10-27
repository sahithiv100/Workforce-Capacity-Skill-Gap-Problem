"""
algorithm.py
Tailored workforce capacity, skill gap analysis, and multi-lever strategic decision engine.
Contains real computational logic for Accenture illustrative prototype.
"""

import numpy as np
import pandas as pd


def compute_employee_net_availability(employees_df):
    """
    Computes net available deployable hours per employee across periods P1-P6
    after subtracting scheduled PTO/leave and current committed hours.
    Gross hours per bi-weekly period = 80 hrs.
    """
    df = employees_df.copy()
    for p in range(1, 7):
        leave_col = f"leave_days_p{p}"
        comm_col = f"committed_p{p}"
        net_col = f"net_avail_p{p}"
        
        # Effective capacity = 80 hrs - (leave_days * 8 hrs)
        effective_cap = df["gross_hours_per_period"] - (df[leave_col] * 8)
        # Net deployable hours cannot be negative
        df[net_col] = np.maximum(0, effective_cap - df[comm_col])
        
    # Total net available over the 12-week horizon
    df["total_net_avail_hrs"] = sum(df[f"net_avail_p{p}"] for p in range(1, 7))
    df["total_committed_hrs"] = sum(df[f"committed_p{p}"] for p in range(1, 7))
    df["total_gross_hrs"] = df["gross_hours_per_period"] * 6
    df["total_leave_hrs"] = sum(df[f"leave_days_p{p}"] * 8 for p in range(1, 7))
    
    # Net deployable utilization %
    df["projected_utilization"] = np.round(
        (df["total_committed_hrs"] / np.maximum(1, df["total_gross_hrs"] - df["total_leave_hrs"])) * 100, 1
    )
    return df


def aggregate_skill_capacity_and_demand(employees_df, requirements_df, skills_df):
    """
    Computes skill-hours supply vs demand across bi-weekly periods P1-P6.
    Matches employees with proficiency >= 3 as qualified deployable supply.
    """
    emp_avail = compute_employee_net_availability(employees_df)
    
    skill_rows = []
    
    for _, skill in skills_df.iterrows():
        s_id = skill["skill_id"]
        s_name = skill["skill_name"]
        domain = skill["domain"]
        
        # Find qualified employees (primary or secondary skill with proficiency >= 3)
        # Weighting: Primary skill gets 100% availability, Secondary gets 70% of available hours
        primary_mask = (emp_avail["primary_skill_id"] == s_id) & (emp_avail["primary_proficiency"] >= 3)
        secondary_mask = (emp_avail["secondary_skill_id"] == s_id) & (emp_avail["secondary_proficiency"] >= 3)
        
        p_emps = emp_avail[primary_mask]
        s_emps = emp_avail[secondary_mask]
        
        # Total qualified headcount
        headcount = len(p_emps) + len(s_emps)
        primary_headcount = len(p_emps)
        avg_prof = 0.0
        if len(p_emps) > 0:
            avg_prof = p_emps["primary_proficiency"].mean()
            
        # Requirements for this skill
        req_subset = requirements_df[requirements_df["skill_id"] == s_id]
        
        row_dict = {
            "skill_id": s_id,
            "skill_name": s_name,
            "domain": domain,
            "headcount_qualified": headcount,
            "primary_headcount": primary_headcount,
            "avg_proficiency": round(avg_prof, 2),
            "training_weeks": skill["training_weeks"],
            "training_cost": skill["training_cost"],
            "hiring_lead_weeks": skill["hiring_lead_weeks"],
            "hiring_cost": skill["hiring_cost"],
            "contractor_rate_hr": skill["contractor_rate_hr"]
        }
        
        tot_demand = 0
        tot_supply = 0
        tot_deficit = 0
        
        for p in range(1, 7):
            p_demand = req_subset[f"req_hrs_p{p}"].sum() if len(req_subset) > 0 else 0
            
            p_sup_primary = p_emps[f"net_avail_p{p}"].sum() if len(p_emps) > 0 else 0
            p_sup_secondary = (s_emps[f"net_avail_p{p}"].sum() * 0.70) if len(s_emps) > 0 else 0
            p_supply = int(p_sup_primary + p_sup_secondary)
            
            p_gap = p_demand - p_supply
            p_deficit = max(0, p_gap)
            p_surplus = max(0, -p_gap)
            
            row_dict[f"demand_p{p}"] = p_demand
            row_dict[f"supply_p{p}"] = p_supply
            row_dict[f"gap_p{p}"] = p_gap
            row_dict[f"deficit_p{p}"] = p_deficit
            row_dict[f"surplus_p{p}"] = p_surplus
            
            tot_demand += p_demand
            tot_supply += p_supply
            tot_deficit += p_deficit
            
        row_dict["total_demand_hrs"] = tot_demand
        row_dict["total_supply_hrs"] = tot_supply
        row_dict["net_deficit_hrs"] = tot_deficit
        row_dict["net_balance_hrs"] = tot_supply - tot_demand
        row_dict["coverage_ratio"] = round((tot_supply / tot_demand * 100), 1) if tot_demand > 0 else 100.0
        
        skill_rows.append(row_dict)
        
    return pd.DataFrame(skill_rows)


def analyze_requirement_gaps(requirements_df, employees_df, skills_df):
    """
    Evaluates each specific project requirement against matching employee capacity.
    Calculates exact deficit, severity rating, and lead-time constraints.
    """
    emp_avail = compute_employee_net_availability(employees_df)
    skill_lookup = {r["skill_id"]: r for _, r in skills_df.iterrows()}
    
    analysis_records = []
    
    for _, req in requirements_df.iterrows():
        s_id = req["skill_id"]
        min_prof = req["min_proficiency"]
        start_p = req["start_period"]
        end_p = req["end_period"]
        tier = req["priority_tier"]
        skill_info = skill_lookup[s_id]
        
        # Qualified employees with proficiency >= min_proficiency
        matched_emps = emp_avail[
            ((emp_avail["primary_skill_id"] == s_id) & (emp_avail["primary_proficiency"] >= min_prof)) |
            ((emp_avail["secondary_skill_id"] == s_id) & (emp_avail["secondary_proficiency"] >= min_prof))
        ]
        
        # Employees eligible for upskilling: proficiency == min_prof - 1 or primary in same domain
        upskillable_emps = emp_avail[
            ((emp_avail["primary_skill_id"] == s_id) & (emp_avail["primary_proficiency"] == (min_prof - 1))) |
            ((emp_avail["secondary_skill_id"] == s_id) & (emp_avail["secondary_proficiency"] == (min_prof - 1)))
        ]
        
        # Calculate available hours across the requirement's active periods
        req_demand_hrs = 0
        req_avail_hrs = 0
        
        for p in range(start_p, end_p + 1):
            req_demand_hrs += req[f"req_hrs_p{p}"]
            p_avail = matched_emps[f"net_avail_p{p}"].sum() if len(matched_emps) > 0 else 0
            req_avail_hrs += p_avail
            
        # Requirement deficit
        deficit_hrs = max(0, req_demand_hrs - req_avail_hrs)
        
        # Weeks until project start (each period is 2 weeks; P1 starts immediately, week 0-1)
        lead_time_weeks = (start_p - 1) * 2
        
        # Severity evaluation
        # Critical: Tier 1 + Deficit > 0 + Lead time <= 4 weeks
        # High: (Tier 1 + Deficit > 0) OR (Tier 2 + Deficit > 80 hrs + Lead time <= 4 weeks)
        # Medium: Tier 2 or 3 with Deficit > 0
        # Low / Balanced: Deficit == 0
        if deficit_hrs == 0:
            severity = "Fulfilled (No Gap)"
            severity_rank = 4
        elif "Tier 1" in tier and lead_time_weeks <= 4:
            severity = "Critical (Immediate Risk)"
            severity_rank = 1
        elif "Tier 1" in tier or ("Tier 2" in tier and lead_time_weeks <= 4 and deficit_hrs >= 80):
            severity = "High (Strategic Watch)"
            severity_rank = 2
        else:
            severity = "Medium (Manageable)"
            severity_rank = 3
            
        record = {
            "requirement_id": req["requirement_id"],
            "project_id": req["project_id"],
            "project_name": req["project_name"],
            "client_industry": req["client_industry"],
            "priority_tier": tier,
            "role_description": req["role_description"],
            "skill_id": s_id,
            "skill_name": req["skill_name"],
            "domain": skill_info["domain"],
            "min_proficiency": min_prof,
            "start_period": start_p,
            "end_period": end_p,
            "lead_time_weeks": lead_time_weeks,
            "deadline_week": req["deadline_week"],
            "demand_hours": req_demand_hrs,
            "available_qualified_hours": req_avail_hrs,
            "deficit_hours": deficit_hrs,
            "matched_headcount": len(matched_emps),
            "upskillable_candidates_count": len(upskillable_emps),
            "severity": severity,
            "severity_rank": severity_rank,
            "risk_penalty_per_week": req["risk_penalty_per_week"],
            "training_weeks": skill_info["training_weeks"],
            "training_cost": skill_info["training_cost"],
            "hiring_lead_weeks": skill_info["hiring_lead_weeks"],
            "hiring_cost": skill_info["hiring_cost"],
            "contractor_rate_hr": skill_info["contractor_rate_hr"]
        }
        analysis_records.append(record)
        
    res_df = pd.DataFrame(analysis_records)
    res_df = res_df.sort_values(by=["severity_rank", "deficit_hours"], ascending=[True, False]).reset_index(drop=True)
    return res_df


def evaluate_strategic_levers(gap_record, weights=None):
    """
    Evaluates the 5 strategic levers for a single requirement gap record:
    1. Internal Reallocation
    2. Internal Upskilling / Training
    3. External Direct Hire
    4. Contingent Contractor
    5. Project Phasing / Milestone Deferral
    
    Computes real estimated costs, lead times, delivery slippage risk, and composite fitness score.
    """
    if weights is None:
        weights = {"cost": 0.30, "speed": 0.35, "strategic": 0.20, "feasibility": 0.15}
        
    deficit_hrs = gap_record["deficit_hours"]
    lead_time_weeks = gap_record["lead_time_weeks"]
    start_p = gap_record["start_period"]
    tier = gap_record["priority_tier"]
    is_tier_1 = "Tier 1" in tier
    
    training_weeks = gap_record["training_weeks"]
    training_cost = gap_record["training_cost"]
    hiring_lead_weeks = gap_record["hiring_lead_weeks"]
    hiring_cost = gap_record["hiring_cost"]
    contractor_rate = gap_record["contractor_rate_hr"]
    matched_headcount = gap_record["matched_headcount"]
    upskill_candidates = gap_record["upskillable_candidates_count"]
    
    # If no deficit, return baseline fulfilled status
    if deficit_hrs == 0:
        fulfilled_lever = {
            "lever": "Internal Allocation",
            "cost": 0,
            "lead_time_weeks": 0,
            "delivery_impact": "On Schedule (Zero Risk)",
            "strategic_value": "Optimal (Utilizes Existing Headcount)",
            "feasibility": "100%",
            "feasibility_val": 1.0,
            "score": 100.0,
            "rationale": "Capacity is already fully matched with qualified internal staff."
        }
        return {
            "recommended_lever": "Internal Allocation",
            "recommended_cost": 0,
            "recommended_lead_time": 0,
            "delivery_impact": "On Schedule (Zero Risk)",
            "score": 100.0,
            "all_levers": [fulfilled_lever],
            "rationale": "Sufficient qualified internal talent available.",
            "assumptions": "Assigned resources remain committed without sudden project churn.",
            "uncertainty": "Low",
            "requires_human_approval": False
        }
        
    # People needed based on deficit hours (assuming 80 hrs/person across 2 periods)
    people_needed = max(1, int(np.ceil(deficit_hrs / 120)))
    
    levers = []
    
    # -------------------------------------------------------------
    # Lever 1: Internal Reallocation (from bench or roll-offs)
    # -------------------------------------------------------------
    realloc_cost = 1200 * people_needed
    realloc_lead_time = 1.5
    # Feasibility is high if qualified headcount exists in the firm, low if firm total is thin
    if matched_headcount >= people_needed:
        realloc_feasibility = 0.85
        realloc_impact = "On Schedule (Negligible Friction)"
        realloc_speed_score = 90.0
    elif matched_headcount > 0:
        realloc_feasibility = 0.45
        realloc_impact = "Partial Fill; Requires Secondary Sourcing"
        realloc_speed_score = 65.0
    else:
        realloc_feasibility = 0.10
        realloc_impact = "High Friction: No Readily Qualified Bench"
        realloc_speed_score = 30.0
        
    realloc_cost_score = 95.0
    realloc_strat_score = 80.0
    
    score_realloc = (
        weights["cost"] * realloc_cost_score +
        weights["speed"] * realloc_speed_score +
        weights["strategic"] * realloc_strat_score +
        weights["feasibility"] * (realloc_feasibility * 100)
    )
    
    levers.append({
        "lever": "Internal Reallocation",
        "cost": realloc_cost,
        "lead_time_weeks": realloc_lead_time,
        "delivery_impact": realloc_impact,
        "strategic_value": "High (Protects Firm Margins & Culture)",
        "feasibility": f"{int(realloc_feasibility*100)}%",
        "feasibility_val": realloc_feasibility,
        "score": round(score_realloc, 1),
        "rationale": f"Mobilize {people_needed} internal resource(s) from lower-priority projects or bench with {realloc_lead_time} wks ramp-up."
    })
    
    # -------------------------------------------------------------
    # Lever 2: Internal Upskilling / Training
    # -------------------------------------------------------------
    # Cost = Course fees + Opportunity cost (half-time study during training)
    train_total_cost = (training_cost + (training_weeks * 20 * 85)) * people_needed
    train_lead_time = training_weeks
    
    # Check if training finishes BEFORE project start week
    time_slack = lead_time_weeks - train_lead_time
    if upskill_candidates >= people_needed:
        base_train_feasibility = 0.90
    elif upskill_candidates > 0:
        base_train_feasibility = 0.60
    else:
        base_train_feasibility = 0.25
        
    if time_slack >= 0:
        train_impact = "On Schedule (Training completes prior to kick-off)"
        train_speed_score = 85.0
        train_feasibility = base_train_feasibility
    else:
        delay_wks = abs(time_slack)
        train_impact = f"Delivery Delay of ~{delay_wks} wks without bridge"
        train_speed_score = max(20.0, 80.0 - (delay_wks * 15.0))
        train_feasibility = base_train_feasibility * 0.70
        
    train_cost_score = 75.0
    train_strat_score = 95.0 # Highest long-term enterprise value!
    
    score_train = (
        weights["cost"] * train_cost_score +
        weights["speed"] * train_speed_score +
        weights["strategic"] * train_strat_score +
        weights["feasibility"] * (train_feasibility * 100)
    )
    
    levers.append({
        "lever": "Internal Upskilling / Training",
        "cost": train_total_cost,
        "lead_time_weeks": train_lead_time,
        "delivery_impact": train_impact,
        "strategic_value": "Exceptional (Permanent Firm IP & Retention)",
        "feasibility": f"{int(train_feasibility*100)}%",
        "feasibility_val": train_feasibility,
        "score": round(score_train, 1),
        "rationale": f"Fast-track {people_needed} candidate(s) through {gap_record['skill_name']} training ({training_weeks} wks curriculum)."
    })
    
    # -------------------------------------------------------------
    # Lever 3: External Direct Hire
    # -------------------------------------------------------------
    hire_total_cost = hiring_cost * people_needed
    hire_lead_time = hiring_lead_weeks
    time_slack_hire = lead_time_weeks - hire_lead_time
    
    if time_slack_hire >= 0:
        hire_impact = "On Schedule (Candidate onboarded in time)"
        hire_speed_score = 70.0
    else:
        delay_hire = abs(time_slack_hire)
        hire_impact = f"Critical Delay: ~{delay_hire} wks recruiting lag"
        hire_speed_score = max(10.0, 60.0 - (delay_hire * 12.0))
        
    hire_cost_score = 40.0 # High recruiting cost
    hire_strat_score = 85.0 # Adds permanent capability to market presence
    hire_feasibility = 0.80 if not is_tier_1 else 0.65
    
    score_hire = (
        weights["cost"] * hire_cost_score +
        weights["speed"] * hire_speed_score +
        weights["strategic"] * hire_strat_score +
        weights["feasibility"] * (hire_feasibility * 100)
    )
    
    levers.append({
        "lever": "External Direct Hire",
        "cost": hire_total_cost,
        "lead_time_weeks": hire_lead_time,
        "delivery_impact": hire_impact,
        "strategic_value": "High (Expands Long-term Practice Capacity)",
        "feasibility": f"{int(hire_feasibility*100)}%",
        "feasibility_val": hire_feasibility,
        "score": round(score_hire, 1),
        "rationale": f"Initiate external executive search for {people_needed} specialist(s); market average {hiring_lead_weeks} wks recruiting cycle."
    })
    
    # -------------------------------------------------------------
    # Lever 4: Contingent Contractor
    # -------------------------------------------------------------
    contractor_total_cost = int(contractor_rate * deficit_hrs)
    contractor_lead_time = 1.5
    contractor_impact = "On Schedule (Fast Vendor Deployment in 1-2 wks)"
    contractor_speed_score = 95.0
    contractor_cost_score = max(20.0, 80.0 - (contractor_total_cost / 1500.0))
    contractor_strat_score = 30.0 # Zero long-term IP retention
    contractor_feasibility = 0.95
    
    score_contractor = (
        weights["cost"] * contractor_cost_score +
        weights["speed"] * contractor_speed_score +
        weights["strategic"] * contractor_strat_score +
        weights["feasibility"] * (contractor_feasibility * 100)
    )
    
    levers.append({
        "lever": "Contingent Contractor",
        "cost": contractor_total_cost,
        "lead_time_weeks": contractor_lead_time,
        "delivery_impact": contractor_impact,
        "strategic_value": "Low (Ephemeral Capacity; Margin Drain)",
        "feasibility": f"{int(contractor_feasibility*100)}%",
        "feasibility_val": contractor_feasibility,
        "score": round(score_contractor, 1),
        "rationale": f"Mobilize vetted ecosystem contractor partner at ${contractor_rate}/hr to bridge {deficit_hrs} hrs."
    })
    
    # -------------------------------------------------------------
    # Lever 5: Project Phasing / Scope Deferral
    # -------------------------------------------------------------
    # Shift start by 3 weeks
    phasing_cost = int(gap_record["risk_penalty_per_week"] * (0.35 if is_tier_1 else 0.15))
    phasing_lead_time = 3.0
    if is_tier_1:
        phasing_impact = "Client Discontent: Milestone SLA Breach Risk"
        phasing_speed_score = 25.0
        phasing_strat_score = 20.0
        phasing_feasibility = 0.25
    else:
        phasing_impact = "Controlled Rescheduling with Client PMO"
        phasing_speed_score = 60.0
        phasing_strat_score = 50.0
        phasing_feasibility = 0.70
        
    phasing_cost_score = 70.0
    
    score_phasing = (
        weights["cost"] * phasing_cost_score +
        weights["speed"] * phasing_speed_score +
        weights["strategic"] * phasing_strat_score +
        weights["feasibility"] * (phasing_feasibility * 100)
    )
    
    levers.append({
        "lever": "Project Phasing / Scope Deferral",
        "cost": phasing_cost,
        "lead_time_weeks": phasing_lead_time,
        "delivery_impact": phasing_impact,
        "strategic_value": "Defensive (Protects Overworked Teams)",
        "feasibility": f"{int(phasing_feasibility*100)}%",
        "feasibility_val": phasing_feasibility,
        "score": round(score_phasing, 1),
        "rationale": "Renegotiate delivery milestone dates with client to allow organic internal ramp-up."
    })
    
    # Sort levers by composite score descending
    levers = sorted(levers, key=lambda x: x["score"], reverse=True)
    best_lever = levers[0]
    
    # Determine assumptions & uncertainty
    if best_lever["lever"] == "Internal Reallocation":
        assumptions = "Assumes releasing project managers agree to roll off resources without secondary staffing delays."
        uncertainty = "Low to Moderate (Subject to project sponsor agreement)"
    elif best_lever["lever"] == "Internal Upskilling / Training":
        assumptions = f"Assumes selected engineers pass certification exam and achieve level {gap_record['min_proficiency']} proficiency upon completion."
        uncertainty = "Moderate (Exam pass rate & practical learning curve)"
    elif best_lever["lever"] == "Contingent Contractor":
        assumptions = f"Assumes approved staffing vendor can provide screened contractors at agreed rate within {contractor_lead_time} weeks."
        uncertainty = "Low (Standard agency master service agreement in place)"
    elif best_lever["lever"] == "External Direct Hire":
        assumptions = f"Assumes talent acquisition pipeline delivers qualified candidate accepting offer within {hiring_lead_weeks} weeks."
        uncertainty = "High (Competitive market dynamics & candidate notice periods)"
    else:
        assumptions = "Assumes client steering committee agrees to revised milestone dates without commercial dispute."
        uncertainty = "High (Dependent on external client negotiation)"
        
    requires_human_approval = is_tier_1 or (best_lever["cost"] > 20000) or ("Delay" in best_lever["delivery_impact"])
    
    return {
        "recommended_lever": best_lever["lever"],
        "recommended_cost": best_lever["cost"],
        "recommended_lead_time": best_lever["lead_time_weeks"],
        "delivery_impact": best_lever["delivery_impact"],
        "score": best_lever["score"],
        "all_levers": levers,
        "rationale": best_lever["rationale"],
        "assumptions": assumptions,
        "uncertainty": uncertainty,
        "requires_human_approval": requires_human_approval
    }


def compute_all_recommendations(gap_df, weights=None):
    """
    Computes recommendation profiles for all requirement records in gap_df.
    """
    rec_records = []
    
    for _, gap in gap_df.iterrows():
        eval_res = evaluate_strategic_levers(gap, weights=weights)
        
        row = {
            "requirement_id": gap["requirement_id"],
            "project_id": gap["project_id"],
            "project_name": gap["project_name"],
            "priority_tier": gap["priority_tier"],
            "role_description": gap["role_description"],
            "skill_name": gap["skill_name"],
            "min_proficiency": gap["min_proficiency"],
            "deficit_hours": gap["deficit_hours"],
            "severity": gap["severity"],
            "recommended_lever": eval_res["recommended_lever"],
            "recommended_cost": eval_res.get("recommended_cost", 0),
            "lead_time_weeks": eval_res.get("recommended_lead_time", 0),
            "delivery_impact": eval_res["delivery_impact"],
            "composite_score": eval_res.get("score", 100.0),
            "evidence_rationale": eval_res["rationale"],
            "key_assumptions": eval_res["assumptions"],
            "uncertainty_level": eval_res["uncertainty"],
            "governance_signoff_required": "Yes (Director Review)" if eval_res["requires_human_approval"] else "Standard Auto-Approval"
        }
        rec_records.append(row)
        
    return pd.DataFrame(rec_records)


def solve_heuristic_allocation(employees_df, requirements_df, max_utilization=100.0):
    """
    Constructs a feasible staff-to-project allocation plan respecting
    proficiency requirements and workload limits (max_utilization cap).
    Uses a priority-based greedy heuristic matching Tier 1 projects first.
    """
    emp_df = compute_employee_net_availability(employees_df)
    
    # Initialize dynamic remaining available hours tracking for each employee
    emp_caps = {}
    for _, e in emp_df.iterrows():
        emp_id = e["employee_id"]
        # Max allowed hours per period
        gross_p = e["gross_hours_per_period"]
        max_allowed_p = gross_p * (max_utilization / 100.0)
        
        p_caps = {}
        for p in range(1, 7):
            leave_hrs = e[f"leave_days_p{p}"] * 8
            # Effective headroom above existing commitments
            committed = e[f"committed_p{p}"]
            avail = max(0.0, max_allowed_p - leave_hrs - committed)
            p_caps[p] = avail
            
        emp_caps[emp_id] = {
            "name": e["name"],
            "grade": e["grade"],
            "practice": e["practice"],
            "location": e["location"],
            "cost_rate_hr": e["cost_rate_hr"],
            "primary_skill_id": e["primary_skill_id"],
            "primary_prof": e["primary_proficiency"],
            "secondary_skill_id": e["secondary_skill_id"],
            "secondary_prof": e["secondary_proficiency"],
            "p_headroom": p_caps,
            "total_assigned": 0
        }
        
    # Sort requirements by priority (Tier 1 first) then start period
    sorted_reqs = requirements_df.copy()
    tier_order = {"Tier 1 (Strategic / Must Deliver)": 1, "Tier 2 (Growth / Commercial)": 2, "Tier 3 (Flexible Phasing)": 3}
    sorted_reqs["tier_num"] = sorted_reqs["priority_tier"].map(tier_order)
    sorted_reqs = sorted_reqs.sort_values(by=["tier_num", "start_period"]).reset_index(drop=True)
    
    assignments = []
    
    for _, req in sorted_reqs.iterrows():
        r_id = req["requirement_id"]
        s_id = req["skill_id"]
        min_p = req["min_proficiency"]
        start_p = req["start_period"]
        end_p = req["end_period"]
        
        # Determine candidate employees matching proficiency
        candidates = []
        for emp_id, data in emp_caps.items():
            is_match = False
            prof_level = 0
            if data["primary_skill_id"] == s_id and data["primary_prof"] >= min_p:
                is_match = True
                prof_level = data["primary_prof"]
            elif data["secondary_skill_id"] == s_id and data["secondary_prof"] >= min_p:
                is_match = True
                prof_level = data["secondary_prof"]
                
            if is_match:
                # Calculate available headroom across active periods
                active_avail = sum(data["p_headroom"][p] for p in range(start_p, end_p + 1))
                if active_avail > 0:
                    candidates.append((emp_id, prof_level, active_avail, data))
                    
        # Sort candidates: prefer those with exact match or higher headroom
        candidates.sort(key=lambda c: (c[1], c[2]), reverse=True)
        
        for p in range(start_p, end_p + 1):
            needed_hrs = req[f"req_hrs_p{p}"]
            remaining_to_fill = needed_hrs
            
            for emp_id, prof, _, data in candidates:
                if remaining_to_fill <= 0:
                    break
                    
                emp_p_headroom = data["p_headroom"][p]
                if emp_p_headroom > 0:
                    allocated_hrs = min(remaining_to_fill, emp_p_headroom)
                    data["p_headroom"][p] -= allocated_hrs
                    data["total_assigned"] += allocated_hrs
                    remaining_to_fill -= allocated_hrs
                    
                    cost = allocated_hrs * data["cost_rate_hr"]
                    assignments.append({
                        "requirement_id": r_id,
                        "project_id": req["project_id"],
                        "project_name": req["project_name"],
                        "priority_tier": req["priority_tier"],
                        "skill_name": req["skill_name"],
                        "period": f"P{p} (Wk {p*2-1}-{p*2})",
                        "employee_id": emp_id,
                        "employee_name": data["name"],
                        "employee_grade": data["grade"],
                        "location": data["location"],
                        "hours_allocated": int(allocated_hrs),
                        "internal_cost": int(cost)
                    })
                    
    assign_df = pd.DataFrame(assignments)
    
    # Calculate post-allocation utilization summary for employees
    emp_summary = []
    for emp_id, data in emp_caps.items():
        orig_row = emp_df[emp_df["employee_id"] == emp_id].iloc[0]
        tot_assigned = data["total_assigned"]
        tot_comm = orig_row["total_committed_hrs"]
        tot_active = tot_comm + tot_assigned
        gross = orig_row["total_gross_hrs"] - orig_row["total_leave_hrs"]
        new_util = round((tot_active / max(1, gross)) * 100, 1)
        
        emp_summary.append({
            "employee_id": emp_id,
            "name": data["name"],
            "grade": data["grade"],
            "location": data["location"],
            "baseline_utilization": orig_row["baseline_utilization"],
            "new_assigned_hours": tot_assigned,
            "post_allocation_utilization": new_util,
            "overallocated": new_util > max_utilization
        })
        
    summary_df = pd.DataFrame(emp_summary)
    return assign_df, summary_df


def simulate_what_if_shocks(gap_df, hiring_multiplier=1.0, attrition_shock_pct=0.0, lead_time_reduction_wks=0, contractor_cost_inflation_pct=0.0):
    """
    Applies scenario shocks to project requirements and capacity:
    - hiring_multiplier: extends recruiting lead time (e.g. 1.25x = +25% longer)
    - attrition_shock_pct: sudden attrition of staff creating wider deficits
    - lead_time_reduction_wks: projects accelerated by 1-4 weeks
    - contractor_cost_inflation_pct: contractor rate increases
    """
    sim_df = gap_df.copy()
    
    # Apply hiring lead time extension
    sim_df["hiring_lead_weeks"] = np.round(sim_df["hiring_lead_weeks"] * hiring_multiplier, 1)
    
    # Apply contractor inflation
    sim_df["contractor_rate_hr"] = np.round(sim_df["contractor_rate_hr"] * (1.0 + contractor_cost_inflation_pct / 100.0), 1)
    
    # Apply lead time reduction (deadlines brought forward)
    sim_df["lead_time_weeks"] = np.maximum(0, sim_df["lead_time_weeks"] - lead_time_reduction_wks)
    
    # Apply attrition shock: reduces available qualified hours and increases deficit
    if attrition_shock_pct > 0:
        attrition_factor = 1.0 - (attrition_shock_pct / 100.0)
        sim_df["available_qualified_hours"] = np.round(sim_df["available_qualified_hours"] * attrition_factor)
        sim_df["deficit_hours"] = np.maximum(0, sim_df["demand_hours"] - sim_df["available_qualified_hours"])
        
    # Re-evaluate severities under shock conditions
    new_severities = []
    new_ranks = []
    
    for _, row in sim_df.iterrows():
        def_hrs = row["deficit_hours"]
        lt_wks = row["lead_time_weeks"]
        tier = row["priority_tier"]
        
        if def_hrs == 0:
            sev = "Fulfilled (No Gap)"
            rk = 4
        elif "Tier 1" in tier and lt_wks <= 4:
            sev = "Critical (Immediate Risk)"
            rk = 1
        elif "Tier 1" in tier or ("Tier 2" in tier and lt_wks <= 4 and def_hrs >= 80):
            sev = "High (Strategic Watch)"
            rk = 2
        else:
            sev = "Medium (Manageable)"
            rk = 3
            
        new_severities.append(sev)
        new_ranks.append(rk)
        
    sim_df["severity"] = new_severities
    sim_df["severity_rank"] = new_ranks
    
    # Recompute strategic recommendations under shocked parameters
    sim_recs = compute_all_recommendations(sim_df)
    
    # Summary shock metrics
    total_shortfall = sim_df["deficit_hours"].sum()
    crit_count = (sim_df["severity"] == "Critical (Immediate Risk)").sum()
    high_count = (sim_df["severity"] == "High (Strategic Watch)").sum()
    total_budget_needed = sim_recs["recommended_cost"].sum()
    
    # Delivery Risk Index: 0 to 100 composite index
    base_penalty = crit_count * 18.0 + high_count * 8.0 + (total_shortfall / 120.0)
    risk_index = min(100.0, round(base_penalty, 1))
    
    return {
        "sim_df": sim_df,
        "sim_recs": sim_recs,
        "total_shortfall_hours": int(total_shortfall),
        "critical_gaps_count": int(crit_count),
        "high_gaps_count": int(high_count),
        "total_budget_needed": int(total_budget_needed),
        "delivery_risk_index": risk_index
    }
