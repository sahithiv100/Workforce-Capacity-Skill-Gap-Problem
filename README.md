# Workforce Capacity & Skill Gap Intelligence Platform
**Illustrative Company Prototype: Accenture** | **Business Area: HR & Talent Operations**

> ⚠️ **DISCLAIMER: SYNTHETIC DEMO DATA — NOT REAL COMPANY DATA**  
> All employee profiles, competencies, certifications, project demands, financial benchmarks, and client scenarios are fictional mathematical constructs designed for functional prototype demonstration only. This application does not connect to internal company systems, scrape proprietary data, or automate adverse employment decisions.

---

## 📌 Executive Summary & Business Objective
In large-scale professional services organizations (modeled after Accenture Technology and Consulting practices), rapid technological shifts (Generative AI, Multi-Cloud Platforms, SAP S/4HANA migrations) trigger severe talent allocation imbalances. Delivery managers often face simultaneous constraints:
1. Shortage of high-demand skills threatening critical project delivery milestones.
2. Underutilization of adjacent talent pools in legacy practices.
3. Over-reliance on expensive, short-term contingent contractors that erode project profit margins and build zero internal intellectual property.

This interactive platform computes net deployable capacity over a 12-week horizon, identifies skill deficits at the project milestone level, and uses a multi-attribute optimization engine to recommend the optimal balance of **Internal Reassignment**, **Sprint Upskilling**, **External Direct Hiring**, **Contingent Contractor Bridging**, and **Project Phasing**.

---

## 🚀 Key Features

### 1. Dynamic Net Capacity Forecasting
- Computes gross bi-weekly capacity (80 hours) minus scheduled PTO/leave days and existing project commitments.
- Standardizes technical competencies to a 1–5 proficiency scale (1: Novice to 5: Expert).
- Maps primary and secondary skills across 15 high-demand technology domains.

### 2. Multi-Stage Gap & Severity Engine
- Evaluates skill deficits against project priority tiers (*Tier 1: Strategic / Must Deliver*, *Tier 2: Commercial Growth*, *Tier 3: Flexible Phasing*).
- Flags high-risk gaps into **Critical (<4 weeks to delivery)**, **High**, and **Medium** categories.

### 3. Multi-Attribute Tradeoff Decision Engine
- Evaluates 5 strategic resolution levers for every requirement:
  - **Internal Reallocation:** Fast deployment (1.5 wks), minimal friction cost ($1,200).
  - **Sprint Upskilling:** Intensive certification (2–4 wks), highest firm IP and long-term retention.
  - **External Direct Hire:** Comprehensive permanent capacity (6–10 wks recruitment lag).
  - **Contingent Contractor:** Rapid surge capacity (1–2 wks), premium hourly expense ($145–$210/hr).
  - **Project Phasing:** Controlled client renegotiation for flexible-tier deliverables.
- Generates composite utility score balancing deployment speed, cost efficiency, firm retention, and feasibility.

### 4. Interactive Allocation Planner & Workload Guardrails
- Priority heuristic assigns qualified internal staff to Tier 1 projects first.
- Strict enforcement of user-adjustable workload ceilings (80% to 120% utilization) to prevent burnout.

### 5. Stress-Testing & Shock Simulator
- Interactive scenario sliders for:
  - Hiring lead-time inflation (1.0x to 2.0x)
  - Unplanned senior attrition shock (0% to 25%)
  - Project milestone acceleration (1 to 4 weeks earlier)
  - Contingent contractor rate inflation (0% to 30%)
- Recalculates critical gap count, total shortfall hours, resolution budget, and delivery risk index in real time.

### 6. Managerial Inquiries (Drilldown Modules)
- **Q1:** Imminent delivery breach risks on Tier-1 GenAI and Cloud migrations.
- **Q2:** Contractor surge expenditure vs. internal bench reallocation economics within 4 weeks.
- **Q3:** Multi-quarter ROI analysis of cohort upskilling vs. paying external executive recruiting search fees.

### 7. Actionable Data Exports
- One-click exports of:
  - Executive Briefing Memo (`.txt`)
  - Strategic Action Plan (`.csv`)
  - Skill Gap Ledger (`.csv`)
  - Staff-to-Project Allocation Schedule (`.csv`)
  - Filtered synthetic employee and project rosters (`.csv`)

---

## 📁 Repository Structure (All Files in Root)

As required for deployment on Streamlit Community Cloud and GitHub, all files are located directly in the root directory without nested folders:

| File | Purpose |
| :--- | :--- |
| `app.py` | Main Streamlit application with custom dark navy styling, navigation tabs, KPI cards, interactive Plotly charts, and export handlers. |
| `synthetic_data.py` | Deterministic synthetic dataset generator producing realistic employees, skills taxonomy, certifications, client projects, requirements, and market benchmarks. |
| `algorithm.py` | Real computational logic: net capacity calculation, requirement-level deficit engine, multi-attribute lever evaluation, heuristic allocation solver, and shock simulator. |
| `ui_components.py` | UI styling, CSS injection, dark navy/purple Plotly chart builders (Heatmaps, Timelines, Donut charts, Radar charts), and metric card formatters. |
| `requirements.txt` | Dependency specifications (`streamlit`, `pandas`, `numpy`, `plotly`). |
| `README.md` | Full system documentation, execution guide, architecture breakdown, and testing report. |

---

## 💻 Step-by-Step Windows Setup & Execution Guide

### Prerequisites
- Python 3.10+ (Verified on Python 3.11 / 3.12 / 3.13)
- Windows PowerShell or Command Prompt

### Step 1: Open Terminal in the Project Directory
```powershell
cd "C:\Users\DELL\.gemini\antigravity\scratch\workforce_capacity_intelligence"
```

### Step 2: Create and Activate a Virtual Environment
```powershell
# Create virtual environment named .venv
python -m venv .venv

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1
```
*(If PowerShell restricts script execution, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

### Step 3: Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Launch the Streamlit Application
```powershell
streamlit run app.py
```
The application will launch and automatically open in your default browser at `http://localhost:8501`.

---

## 📊 Computational Formulation & Objective Function

The platform solves the multi-criteria allocation and recommendation problem using weighted utility maximization:

$$\max_{x_{r, l}} \sum_{r \in \mathcal{R}} \sum_{l \in \mathcal{L}} \left( w_{\text{speed}} \cdot S_{\text{speed}}(r, l) + w_{\text{cost}} \cdot S_{\text{cost}}(r, l) + w_{\text{strat}} \cdot S_{\text{strat}}(r, l) + w_{\text{feas}} \cdot S_{\text{feas}}(r, l) \right) x_{r, l}$$

Subject to:
1. $\sum_{l \in \mathcal{L}} x_{r, l} = 1 \quad \forall r \in \mathcal{R}$ (Every requirement gap is evaluated).
2. $\text{Utilization}_e \le \text{Max\_Workload\_Cap} \quad \forall e \in \mathcal{E}$ (Overload guardrail).
3. $\text{Proficiency}_e \ge \text{Min\_Required\_Proficiency}_r$ (Skill qualification constraint).

---

## 🛡️ Model Governance, Baseline & Safety Disclosures
- **Transparent Baseline Comparison:** The model benchmarks optimized recommendations against a standard industry baseline of "100% reactive contractor sourcing", quantifying exact capital savings and IP retention deltas.
- **Human-in-the-Loop Requirement:** High-impact staffing adjustments, contractor commitments over \$20,000, and milestone shifts trigger an explicit governance flag requiring Practice Director sign-off.
- **No Adverse Automated Employment Decisions:** The algorithm never recommends demotions, wage decreases, or terminations.
- **Data Privacy:** 100% synthetic data generated deterministically; zero personal identifying information (PII) is accessed or stored.

---

## 🧪 Testing and Validation Report
- **Python Imports & Syntax:** Verified with clean imports across `synthetic_data.py`, `algorithm.py`, `ui_components.py`, and `app.py`.
- **Deterministic Generation:** Verified reproducibility across seeds (default seed 42 produces 140 synthetic profiles, 20 client projects, and 28 requirement lines).
- **Interactive UI Testing:** Verified that all tabs, metric cards, Plotly charts (heatmaps, timelines, radars), scenario sliders, and CSV/text download buttons execute and render without errors.
