"""
synthetic_data.py
Synthetic workforce, skills, and project demand generator for Accenture illustrative prototype.
All data is 100% fictional and mathematically cohesive for capacity simulation.
"""

import numpy as np
import pandas as pd
from datetime import datetime

# Standard Proficiency Level scale
PROFICIENCY_LEVELS = {
    1: "1 - Novice (Foundational Concepts)",
    2: "2 - Beginner (Guided Execution)",
    3: "3 - Competent (Autonomous Execution)",
    4: "4 - Proficient (Advanced Architecture)",
    5: "5 - Expert (SME / Thought Leadership)"
}

SKILL_TAXONOMY = [
    {
        "skill_id": "SKL-01",
        "domain": "Generative AI & Data",
        "skill_name": "GenAI & LLM Application Engineering",
        "training_weeks": 3,
        "training_cost": 4200,
        "hiring_lead_weeks": 8,
        "hiring_cost": 28000,
        "contractor_rate_hr": 195,
        "certifications": ["Azure OpenAI Certified Specialist", "Databricks GenAI Professional"]
    },
    {
        "skill_id": "SKL-02",
        "domain": "Generative AI & Data",
        "skill_name": "Databricks & PySpark Data Platform",
        "training_weeks": 4,
        "training_cost": 3800,
        "hiring_lead_weeks": 7,
        "hiring_cost": 25000,
        "contractor_rate_hr": 175,
        "certifications": ["Databricks Certified Data Engineer", "Spark Certified Developer"]
    },
    {
        "skill_id": "SKL-03",
        "domain": "Cloud Architecture",
        "skill_name": "AWS Solutions Architecture & Migration",
        "training_weeks": 3,
        "training_cost": 3500,
        "hiring_lead_weeks": 7,
        "hiring_cost": 26000,
        "contractor_rate_hr": 180,
        "certifications": ["AWS Certified Solutions Architect - Professional", "AWS Migration SME"]
    },
    {
        "skill_id": "SKL-04",
        "domain": "Cloud Architecture",
        "skill_name": "Azure Enterprise Cloud & Landing Zones",
        "training_weeks": 3,
        "training_cost": 3400,
        "hiring_lead_weeks": 6,
        "hiring_cost": 24000,
        "contractor_rate_hr": 170,
        "certifications": ["Microsoft Certified: Azure Solutions Architect Expert"]
    },
    {
        "skill_id": "SKL-05",
        "domain": "Cloud Architecture",
        "skill_name": "GCP Data & Multi-Cloud Infrastructure",
        "training_weeks": 4,
        "training_cost": 3900,
        "hiring_lead_weeks": 8,
        "hiring_cost": 27000,
        "contractor_rate_hr": 185,
        "certifications": ["Google Cloud Certified Professional Cloud Architect"]
    },
    {
        "skill_id": "SKL-06",
        "domain": "Enterprise Platforms",
        "skill_name": "SAP S/4HANA Finance & Supply Chain",
        "training_weeks": 5,
        "training_cost": 5500,
        "hiring_lead_weeks": 9,
        "hiring_cost": 32000,
        "contractor_rate_hr": 210,
        "certifications": ["SAP Certified Application Associate - S/4HANA", "SAP Activate PM"]
    },
    {
        "skill_id": "SKL-07",
        "domain": "Enterprise Platforms",
        "skill_name": "Salesforce Core & Industry CRM",
        "training_weeks": 3,
        "training_cost": 3200,
        "hiring_lead_weeks": 6,
        "hiring_cost": 23000,
        "contractor_rate_hr": 165,
        "certifications": ["Salesforce Certified Technical Architect", "Salesforce Application Architect"]
    },
    {
        "skill_id": "SKL-08",
        "domain": "Enterprise Platforms",
        "skill_name": "ServiceNow Enterprise ITSM & SecOps",
        "training_weeks": 3,
        "training_cost": 3100,
        "hiring_lead_weeks": 5,
        "hiring_cost": 21000,
        "contractor_rate_hr": 155,
        "certifications": ["ServiceNow Certified Implementation Specialist", "ITIL v4 Managing Professional"]
    },
    {
        "skill_id": "SKL-09",
        "domain": "Cybersecurity & Trust",
        "skill_name": "Zero-Trust Architecture & Cloud Security",
        "training_weeks": 4,
        "training_cost": 4800,
        "hiring_lead_weeks": 8,
        "hiring_cost": 31000,
        "contractor_rate_hr": 205,
        "certifications": ["CISSP - Certified Information Systems Security Professional", "CCSP Cloud Security"]
    },
    {
        "skill_id": "SKL-10",
        "domain": "Cybersecurity & Trust",
        "skill_name": "DevSecOps & Kubernetes Security",
        "training_weeks": 3,
        "training_cost": 3600,
        "hiring_lead_weeks": 6,
        "hiring_cost": 25000,
        "contractor_rate_hr": 175,
        "certifications": ["Certified Kubernetes Security Specialist (CKS)", "HashiCorp Certified Terraform"]
    },
    {
        "skill_id": "SKL-11",
        "domain": "Generative AI & Data",
        "skill_name": "MLOps, Feature Stores & LLM Monitoring",
        "training_weeks": 4,
        "training_cost": 4500,
        "hiring_lead_weeks": 8,
        "hiring_cost": 29000,
        "contractor_rate_hr": 190,
        "certifications": ["AWS Certified Machine Learning - Specialty", "MLOps World Professional"]
    },
    {
        "skill_id": "SKL-12",
        "domain": "Agile & Transformation",
        "skill_name": "Agile Delivery & SAFe Program Lead",
        "training_weeks": 2,
        "training_cost": 2400,
        "hiring_lead_weeks": 5,
        "hiring_cost": 19000,
        "contractor_rate_hr": 145,
        "certifications": ["PMI-PMP", "SAFe 6.0 Practice Consultant (SPC)", "Certified Scrum Master"]
    },
    {
        "skill_id": "SKL-13",
        "domain": "Agile & Transformation",
        "skill_name": "Org Change Management & AI Adoption",
        "training_weeks": 2,
        "training_cost": 2600,
        "hiring_lead_weeks": 5,
        "hiring_cost": 20000,
        "contractor_rate_hr": 150,
        "certifications": ["Prosci Certified Change Practitioner", "CCMP Certified"]
    },
    {
        "skill_id": "SKL-14",
        "domain": "Agile & Transformation",
        "skill_name": "Digital Strategy & Enterprise Value",
        "training_weeks": 3,
        "training_cost": 3500,
        "hiring_lead_weeks": 7,
        "hiring_cost": 28000,
        "contractor_rate_hr": 185,
        "certifications": ["TOGAF Enterprise Architect", "McKinsey/Accenture Strategy Frameworks"]
    },
    {
        "skill_id": "SKL-15",
        "domain": "Cloud Architecture",
        "skill_name": "Fullstack Cloud Native App Development",
        "training_weeks": 3,
        "training_cost": 3000,
        "hiring_lead_weeks": 5,
        "hiring_cost": 22000,
        "contractor_rate_hr": 160,
        "certifications": ["Node.js Application Developer", "Meta Certified React Architect"]
    }
]

LOCATIONS = ["Bengaluru", "London", "New York", "Frankfurt", "Singapore", "Toronto"]
JOB_GRADES = [
    ("Analyst", 70, 0.20),
    ("Consultant", 95, 0.30),
    ("Senior Consultant", 130, 0.25),
    ("Manager", 160, 0.15),
    ("Senior Manager", 190, 0.07),
    ("Technology Architect", 215, 0.03)
]

PRACTICES = [
    "Cloud First",
    "Applied Intelligence",
    "Enterprise Strategy",
    "Security & Resiliency",
    "Industry X"
]

FIRST_NAMES = [
    "Aarav", "Priya", "Rahul", "Ananya", "Liam", "Emma", "Noah", "Olivia",
    "Marcus", "Chloe", "Julian", "Sophie", "Lucas", "Elena", "Chen", "Mei",
    "Dev", "Kavya", "Alexander", "Zara", "Vikram", "Natasha", "Mateo", "Camila",
    "Siddharth", "Aisha", "Benjamin", "Hannah", "David", "Grace", "Ethan", "Maya",
    "Arjun", "Sneha", "Kiran", "Tanvi", "Leo", "Mia", "Gabriel", "Isabella"
]

LAST_NAMES = [
    "Sharma", "Patel", "Verma", "Rao", "Smith", "Johnson", "Williams", "Brown",
    "Müller", "Schmidt", "Schneider", "Fischer", "Tan", "Lim", "Wong", "Zhang",
    "Dubois", "Moreau", "Garcia", "Rodriguez", "Nair", "Iyer", "Mukherjee", "Kapoor",
    "Taylor", "Anderson", "Thomas", "Jackson", "Weber", "Meyer", "Lau", "Chua"
]

CLIENT_PROJECTS = [
    {
        "project_id": "PRJ-101",
        "project_name": "Global Tier-1 Bank: Cloud Core Modernization",
        "client_industry": "Financial Services",
        "priority_tier": "Tier 1 (Strategic / Must Deliver)",
        "budget": 2400000,
        "start_period": 1,
        "end_period": 6,
        "deadline_week": 6,
        "lead_partner": "Sarah Jenkins",
        "risk_penalty_per_week": 85000
    },
    {
        "project_id": "PRJ-102",
        "project_name": "Pharma Major: GenAI Clinical Trials Co-Pilot",
        "client_industry": "Health & Life Sciences",
        "priority_tier": "Tier 1 (Strategic / Must Deliver)",
        "budget": 1850000,
        "start_period": 1,
        "end_period": 4,
        "deadline_week": 4,
        "lead_partner": "Dr. Aris Thorne",
        "risk_penalty_per_week": 95000
    },
    {
        "project_id": "PRJ-103",
        "project_name": "Retail Conglomerate: SAP S/4HANA Supply Overhaul",
        "client_industry": "Retail & CPG",
        "priority_tier": "Tier 1 (Strategic / Must Deliver)",
        "budget": 3200000,
        "start_period": 2,
        "end_period": 6,
        "deadline_week": 8,
        "lead_partner": "Markus Weber",
        "risk_penalty_per_week": 75000
    },
    {
        "project_id": "PRJ-104",
        "project_name": "Global Telecom: AI Contact Center Transformation",
        "client_industry": "Communications & High Tech",
        "priority_tier": "Tier 2 (Growth / Commercial)",
        "budget": 1400000,
        "start_period": 1,
        "end_period": 5,
        "deadline_week": 8,
        "lead_partner": "Pooja Singhania",
        "risk_penalty_per_week": 45000
    },
    {
        "project_id": "PRJ-105",
        "project_name": "Federal Health Agency: Zero-Trust Security Uplift",
        "client_industry": "Public Sector",
        "priority_tier": "Tier 1 (Strategic / Must Deliver)",
        "budget": 2100000,
        "start_period": 1,
        "end_period": 6,
        "deadline_week": 6,
        "lead_partner": "David Vance",
        "risk_penalty_per_week": 80000
    },
    {
        "project_id": "PRJ-106",
        "project_name": "Auto OEM: Connected Vehicle Cloud Fabric",
        "client_industry": "Automotive & Manufacturing",
        "priority_tier": "Tier 2 (Growth / Commercial)",
        "budget": 1750000,
        "start_period": 2,
        "end_period": 6,
        "deadline_week": 10,
        "lead_partner": "Klaus Lindner",
        "risk_penalty_per_week": 40000
    },
    {
        "project_id": "PRJ-107",
        "project_name": "Energy Multinational: Databricks ESG Carbon Lake",
        "client_industry": "Resources & Energy",
        "priority_tier": "Tier 2 (Growth / Commercial)",
        "budget": 1250000,
        "start_period": 2,
        "end_period": 5,
        "deadline_week": 8,
        "lead_partner": "Fiona MacLeod",
        "risk_penalty_per_week": 35000
    },
    {
        "project_id": "PRJ-108",
        "project_name": "Insurance Leader: Claims Automation & RAG Agent",
        "client_industry": "Financial Services",
        "priority_tier": "Tier 1 (Strategic / Must Deliver)",
        "budget": 1600000,
        "start_period": 1,
        "end_period": 5,
        "deadline_week": 4,
        "lead_partner": "Rajesh Gupta",
        "risk_penalty_per_week": 90000
    },
    {
        "project_id": "PRJ-109",
        "project_name": "Luxury Retailer: Omnichannel Salesforce Core",
        "client_industry": "Retail & CPG",
        "priority_tier": "Tier 2 (Growth / Commercial)",
        "budget": 980000,
        "start_period": 3,
        "end_period": 6,
        "deadline_week": 12,
        "lead_partner": "Claire Dupont",
        "risk_penalty_per_week": 30000
    },
    {
        "project_id": "PRJ-110",
        "project_name": "Fintech Scaleup: DevSecOps & Kubernetes Pipeline",
        "client_industry": "Financial Services",
        "priority_tier": "Tier 3 (Flexible Phasing)",
        "budget": 750000,
        "start_period": 2,
        "end_period": 5,
        "deadline_week": 12,
        "lead_partner": "Samira Al-Hassan",
        "risk_penalty_per_week": 20000
    },
    {
        "project_id": "PRJ-111",
        "project_name": "Airlines Alliance: ServiceNow Enterprise Incident Hub",
        "client_industry": "Travel & Logistics",
        "priority_tier": "Tier 3 (Flexible Phasing)",
        "budget": 820000,
        "start_period": 3,
        "end_period": 6,
        "deadline_week": 14,
        "lead_partner": "Thomas Becker",
        "risk_penalty_per_week": 25000
    },
    {
        "project_id": "PRJ-112",
        "project_name": "Global Chemical Corp: AI Operating Model & OCM",
        "client_industry": "Resources & Energy",
        "priority_tier": "Tier 3 (Flexible Phasing)",
        "budget": 650000,
        "start_period": 1,
        "end_period": 4,
        "deadline_week": 10,
        "lead_partner": "Evelyn Reed",
        "risk_penalty_per_week": 20000
    }
]

PROJECT_REQUIREMENTS_SPECS = [
    # PRJ-101 (Tier 1, starts P1)
    {"project_id": "PRJ-101", "skill_id": "SKL-03", "min_prof": 4, "hrs_per_p": 160, "start_p": 1, "end_p": 6, "desc": "AWS Enterprise Cloud Lead Architect"},
    {"project_id": "PRJ-101", "skill_id": "SKL-10", "min_prof": 4, "hrs_per_p": 120, "start_p": 1, "end_p": 5, "desc": "DevSecOps & Kubernetes Pipeline Engineer"},
    {"project_id": "PRJ-101", "skill_id": "SKL-12", "min_prof": 3, "hrs_per_p": 80,  "start_p": 1, "end_p": 6, "desc": "SAFe Cloud Delivery Lead"},
    {"project_id": "PRJ-101", "skill_id": "SKL-15", "min_prof": 3, "hrs_per_p": 160, "start_p": 2, "end_p": 6, "desc": "Fullstack Cloud Native Developer"},

    # PRJ-102 (Tier 1, starts P1, high rush)
    {"project_id": "PRJ-102", "skill_id": "SKL-01", "min_prof": 4, "hrs_per_p": 200, "start_p": 1, "end_p": 4, "desc": "Lead GenAI & RAG Clinical Systems Engineer"},
    {"project_id": "PRJ-102", "skill_id": "SKL-11", "min_prof": 4, "hrs_per_p": 120, "start_p": 1, "end_p": 4, "desc": "LLM MLOps & Guardrails Specialist"},
    {"project_id": "PRJ-102", "skill_id": "SKL-02", "min_prof": 3, "hrs_per_p": 120, "start_p": 1, "end_p": 4, "desc": "Databricks Clinical Lakehouse Engineer"},

    # PRJ-103 (Tier 1, starts P2)
    {"project_id": "PRJ-103", "skill_id": "SKL-06", "min_prof": 4, "hrs_per_p": 240, "start_p": 2, "end_p": 6, "desc": "Senior SAP S/4HANA Finance Solutions Lead"},
    {"project_id": "PRJ-103", "skill_id": "SKL-13", "min_prof": 3, "hrs_per_p": 80,  "start_p": 2, "end_p": 5, "desc": "Supply Chain Change Management SME"},
    {"project_id": "PRJ-103", "skill_id": "SKL-14", "min_prof": 4, "hrs_per_p": 80,  "start_p": 2, "end_p": 4, "desc": "Enterprise Value Transformation Lead"},

    # PRJ-104 (Tier 2, starts P1)
    {"project_id": "PRJ-104", "skill_id": "SKL-01", "min_prof": 3, "hrs_per_p": 160, "start_p": 1, "end_p": 5, "desc": "GenAI Conversational Voicebot Engineer"},
    {"project_id": "PRJ-104", "skill_id": "SKL-04", "min_prof": 3, "hrs_per_p": 80,  "start_p": 1, "end_p": 4, "desc": "Azure Landing Zone Engineer"},
    {"project_id": "PRJ-104", "skill_id": "SKL-12", "min_prof": 3, "hrs_per_p": 80,  "start_p": 1, "end_p": 5, "desc": "Agile Scrum Master"},

    # PRJ-105 (Tier 1, starts P1)
    {"project_id": "PRJ-105", "skill_id": "SKL-09", "min_prof": 5, "hrs_per_p": 160, "start_p": 1, "end_p": 6, "desc": "Zero-Trust Cyber Architect"},
    {"project_id": "PRJ-105", "skill_id": "SKL-10", "min_prof": 4, "hrs_per_p": 120, "start_p": 1, "end_p": 6, "desc": "Kubernetes FedRAMP Compliance Engineer"},
    {"project_id": "PRJ-105", "skill_id": "SKL-04", "min_prof": 4, "hrs_per_p": 120, "start_p": 1, "end_p": 5, "desc": "Azure GovCloud Security Engineer"},

    # PRJ-106 (Tier 2, starts P2)
    {"project_id": "PRJ-106", "skill_id": "SKL-05", "min_prof": 4, "hrs_per_p": 160, "start_p": 2, "end_p": 6, "desc": "GCP Connected Telemetry Architect"},
    {"project_id": "PRJ-106", "skill_id": "SKL-02", "min_prof": 3, "hrs_per_p": 120, "start_p": 2, "end_p": 6, "desc": "High-Throughput PySpark Engineer"},

    # PRJ-107 (Tier 2, starts P2)
    {"project_id": "PRJ-107", "skill_id": "SKL-02", "min_prof": 4, "hrs_per_p": 160, "start_p": 2, "end_p": 5, "desc": "Databricks ESG Lakehouse Lead"},
    {"project_id": "PRJ-107", "skill_id": "SKL-03", "min_prof": 3, "hrs_per_p": 80,  "start_p": 2, "end_p": 5, "desc": "AWS Data Pipeline Specialist"},

    # PRJ-108 (Tier 1, starts P1, high rush)
    {"project_id": "PRJ-108", "skill_id": "SKL-01", "min_prof": 4, "hrs_per_p": 160, "start_p": 1, "end_p": 4, "desc": "RAG Document Intelligence Architect"},
    {"project_id": "PRJ-108", "skill_id": "SKL-04", "min_prof": 3, "hrs_per_p": 80,  "start_p": 1, "end_p": 4, "desc": "Azure AI Services Specialist"},
    {"project_id": "PRJ-108", "skill_id": "SKL-15", "min_prof": 3, "hrs_per_p": 120, "start_p": 1, "end_p": 4, "desc": "React Claims Frontend Specialist"},

    # PRJ-109 (Tier 2, starts P3)
    {"project_id": "PRJ-109", "skill_id": "SKL-07", "min_prof": 4, "hrs_per_p": 160, "start_p": 3, "end_p": 6, "desc": "Salesforce Tech Architect"},
    {"project_id": "PRJ-109", "skill_id": "SKL-15", "min_prof": 3, "hrs_per_p": 80,  "start_p": 3, "end_p": 6, "desc": "Headless Commerce Developer"},

    # PRJ-110 (Tier 3, starts P2)
    {"project_id": "PRJ-110", "skill_id": "SKL-10", "min_prof": 3, "hrs_per_p": 120, "start_p": 2, "end_p": 5, "desc": "GitOps Terraform Automation Engineer"},
    {"project_id": "PRJ-110", "skill_id": "SKL-03", "min_prof": 3, "hrs_per_p": 80,  "start_p": 2, "end_p": 5, "desc": "AWS Cloud Ops Specialist"},

    # PRJ-111 (Tier 3, starts P3)
    {"project_id": "PRJ-111", "skill_id": "SKL-08", "min_prof": 4, "hrs_per_p": 160, "start_p": 3, "end_p": 6, "desc": "ServiceNow Senior ITSM Consultant"},
    {"project_id": "PRJ-111", "skill_id": "SKL-12", "min_prof": 3, "hrs_per_p": 80,  "start_p": 3, "end_p": 6, "desc": "Agile Delivery Lead"},

    # PRJ-112 (Tier 3, starts P1)
    {"project_id": "PRJ-112", "skill_id": "SKL-13", "min_prof": 4, "hrs_per_p": 120, "start_p": 1, "end_p": 4, "desc": "AI Adoption & Org Change Lead"},
    {"project_id": "PRJ-112", "skill_id": "SKL-14", "min_prof": 3, "hrs_per_p": 80,  "start_p": 1, "end_p": 3, "desc": "Operating Model Strategist"}
]


def generate_synthetic_workforce(seed=42, n_employees=140):
    """
    Deterministically generates synthetic employee population for Accenture prototype.
    """
    np.random.seed(seed)
    
    # Skills lookup
    skill_names = [s["skill_name"] for s in SKILL_TAXONOMY]
    skill_map = {s["skill_id"]: s for s in SKILL_TAXONOMY}
    
    employees = []
    
    grade_names = [g[0] for g in JOB_GRADES]
    grade_costs = {g[0]: g[1] for g in JOB_GRADES}
    grade_probs = [g[2] for g in JOB_GRADES]
    
    for i in range(n_employees):
        emp_id = f"ACN-EMP-{1000 + i + 1}"
        fname = np.random.choice(FIRST_NAMES)
        lname = np.random.choice(LAST_NAMES)
        name = f"{fname} {lname}"
        
        # Pick grade
        grade = np.random.choice(grade_names, p=grade_probs)
        cost_rate = grade_costs[grade] + np.random.randint(-5, 10)
        
        location = np.random.choice(LOCATIONS, p=[0.38, 0.20, 0.16, 0.10, 0.08, 0.08])
        practice = np.random.choice(PRACTICES, p=[0.30, 0.25, 0.15, 0.18, 0.12])
        
        # Determine Primary & Secondary Skill
        primary_skill_item = np.random.choice(SKILL_TAXONOMY)
        primary_skill_id = primary_skill_item["skill_id"]
        primary_skill_name = primary_skill_item["skill_name"]
        
        # Proficiency influenced by seniority
        if grade in ["Analyst"]:
            p_prof = np.random.choice([1, 2, 3], p=[0.25, 0.55, 0.20])
        elif grade in ["Consultant"]:
            p_prof = np.random.choice([2, 3, 4], p=[0.25, 0.60, 0.15])
        elif grade in ["Senior Consultant"]:
            p_prof = np.random.choice([3, 4, 5], p=[0.35, 0.50, 0.15])
        elif grade in ["Manager"]:
            p_prof = np.random.choice([3, 4, 5], p=[0.30, 0.50, 0.20])
        else: # Senior Manager / Architect
            p_prof = np.random.choice([4, 5], p=[0.45, 0.55])
            
        # Secondary skill
        available_secondary = [s for s in SKILL_TAXONOMY if s["skill_id"] != primary_skill_id]
        secondary_skill_item = np.random.choice(available_secondary)
        secondary_skill_id = secondary_skill_item["skill_id"]
        secondary_skill_name = secondary_skill_item["skill_name"]
        s_prof = max(1, p_prof - np.random.choice([1, 2]))
        
        # Certifications
        certs = []
        if p_prof >= 3 and len(primary_skill_item["certifications"]) > 0:
            if np.random.rand() > 0.3:
                certs.append(primary_skill_item["certifications"][0])
        if p_prof >= 4 and len(primary_skill_item["certifications"]) > 1:
            if np.random.rand() > 0.5:
                certs.append(primary_skill_item["certifications"][1])
        if len(certs) == 0:
            certs.append("Accenture Internal Foundations")
            
        # Standard gross hours per period (2-week period = 80 hrs)
        gross_hrs = 80
        
        # Existing commitments per period (P1 through P6)
        # Baseline utilization around 70-95%
        base_util = np.clip(np.random.normal(0.82, 0.18), 0.30, 1.05)
        
        # Realistic variations across periods (some rolling off, some finishing projects)
        rolloff_period = np.random.choice([2, 3, 4, 5, 6, 7], p=[0.15, 0.20, 0.25, 0.20, 0.10, 0.10])
        
        committed_hrs = []
        leave_days = []
        for p in range(1, 7):
            # Scheduled leave days (typically 0-3 days per fortnight)
            p_leave = np.random.choice([0, 1, 2, 4], p=[0.75, 0.15, 0.08, 0.02])
            leave_days.append(p_leave)
            
            if p >= rolloff_period:
                # Rolling off or on bench
                p_comm = int(gross_hrs * np.random.uniform(0.10, 0.40))
            else:
                p_comm = int(gross_hrs * base_util)
                
            # Leave caps committed hours so gross is not exceeded
            avail_cap = gross_hrs - (p_leave * 8)
            p_comm = min(p_comm, avail_cap)
            committed_hrs.append(p_comm)
            
        perf_score = round(float(np.clip(np.random.normal(3.9, 0.5), 3.0, 5.0)), 2)
        
        emp_dict = {
            "employee_id": emp_id,
            "name": name,
            "grade": grade,
            "practice": practice,
            "location": location,
            "cost_rate_hr": cost_rate,
            "performance_score": perf_score,
            "primary_skill_id": primary_skill_id,
            "primary_skill_name": primary_skill_name,
            "primary_proficiency": p_prof,
            "secondary_skill_id": secondary_skill_id,
            "secondary_skill_name": secondary_skill_name,
            "secondary_proficiency": s_prof,
            "certifications": ", ".join(certs),
            "gross_hours_per_period": gross_hrs,
            "committed_p1": committed_hrs[0],
            "committed_p2": committed_hrs[1],
            "committed_p3": committed_hrs[2],
            "committed_p4": committed_hrs[3],
            "committed_p5": committed_hrs[4],
            "committed_p6": committed_hrs[5],
            "leave_days_p1": leave_days[0],
            "leave_days_p2": leave_days[1],
            "leave_days_p3": leave_days[2],
            "leave_days_p4": leave_days[3],
            "leave_days_p5": leave_days[4],
            "leave_days_p6": leave_days[5],
            "baseline_utilization": round(base_util * 100, 1)
        }
        employees.append(emp_dict)
        
    return pd.DataFrame(employees)


def generate_synthetic_requirements(skills_df, projects_df):
    """
    Builds project skill requirements linked to projects and taxonomy.
    """
    reqs = []
    skill_lookup = {r["skill_id"]: r["skill_name"] for _, r in skills_df.iterrows()}
    proj_lookup = {r["project_id"]: r for _, r in projects_df.iterrows()}
    
    req_idx = 1
    for spec in PROJECT_REQUIREMENTS_SPECS:
        req_id = f"REQ-{req_idx:03d}"
        proj = proj_lookup[spec["project_id"]]
        skill_name = skill_lookup[spec["skill_id"]]
        
        # Calculate hours per period
        p_hrs = {}
        total_hrs = 0
        for p in range(1, 7):
            if spec["start_p"] <= p <= spec["end_p"]:
                p_hrs[f"req_hrs_p{p}"] = spec["hrs_per_p"]
                total_hrs += spec["hrs_per_p"]
            else:
                p_hrs[f"req_hrs_p{p}"] = 0
                
        row = {
            "requirement_id": req_id,
            "project_id": spec["project_id"],
            "project_name": proj["project_name"],
            "client_industry": proj["client_industry"],
            "priority_tier": proj["priority_tier"],
            "role_description": spec["desc"],
            "skill_id": spec["skill_id"],
            "skill_name": skill_name,
            "min_proficiency": spec["min_prof"],
            "start_period": spec["start_p"],
            "end_period": spec["end_p"],
            "deadline_week": proj["deadline_week"],
            "total_hours_required": total_hrs,
            "risk_penalty_per_week": proj["risk_penalty_per_week"]
        }
        row.update(p_hrs)
        reqs.append(row)
        req_idx += 1
        
    return pd.DataFrame(reqs)


def generate_all_synthetic_data(seed=42, n_employees=140):
    """
    Master synthetic data assembly function.
    Returns: dict of DataFrames (skills, employees, projects, requirements, benchmarks).
    """
    skills_df = pd.DataFrame(SKILL_TAXONOMY)
    projects_df = pd.DataFrame(CLIENT_PROJECTS)
    employees_df = generate_synthetic_workforce(seed=seed, n_employees=n_employees)
    requirements_df = generate_synthetic_requirements(skills_df, projects_df)
    
    # Benchmarks summary for quick strategy cost lookups
    benchmarks_df = skills_df[[
        "skill_id", "skill_name", "domain", 
        "training_weeks", "training_cost", 
        "hiring_lead_weeks", "hiring_cost", 
        "contractor_rate_hr"
    ]].copy()
    benchmarks_df["internal_reassignment_cost"] = 1200
    benchmarks_df["internal_reassignment_lead_weeks"] = 1.5
    benchmarks_df["training_proficiency_boost"] = "+1 Level"
    benchmarks_df["reassignment_friction"] = "Low (Internal ramp-up)"
    
    metadata = {
        "seed": seed,
        "n_employees": n_employees,
        "n_projects": len(projects_df),
        "n_requirements": len(requirements_df),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "label": "SYNTHETIC DEMO DATA — NOT REAL COMPANY DATA"
    }
    
    return {
        "skills": skills_df,
        "employees": employees_df,
        "projects": projects_df,
        "requirements": requirements_df,
        "benchmarks": benchmarks_df,
        "metadata": metadata
    }
