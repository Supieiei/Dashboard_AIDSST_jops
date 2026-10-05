"""
AI, Data Science & Statistics Talent Supply & Demand Dashboard
Interactive analytical platform analyzing graduate supply, market demand, and skill mismatch.
Stack: Streamlit, Plotly Express & Graph Objects, Pandas
Data Sources: Kaggle Data Science Salaries (CC0), Open Job Postings, U.S. BLS OEWS, MHESI Open Data
Language: English (No Emojis)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from data.data_engine import (
    generate_supply_dataset,
    generate_demand_dataset,
    calculate_mismatch_metrics,
    load_bls_oews_benchmarks,
    SKILLS_TAXONOMY
)

# ---------------------------------------------------------
# Page Configuration (No Emojis)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Talent Supply & Demand Dashboard | AI, DS & Statistics",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Styling (Executive Dark Mode Polish)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Metric Card Customization */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }
    div[data-testid="stMetric"] label {
        font-size: 0.85rem !important;
        font-weight: 600;
        color: #94A3B8 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        font-size: 1.85rem !important;
        font-weight: 700;
        color: #F8FAFC !important;
    }
    /* Tabs Header Styling */
    button[data-baseweb="tab"] {
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        padding: 10px 18px !important;
    }
    /* Container Cards */
    .dashboard-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 20px;
    }
    .badge-urgent {
        background-color: #EF4444;
        color: white;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-moderate {
        background-color: #F59E0B;
        color: white;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-positive {
        background-color: #10B981;
        color: white;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .data-reference-caption {
        color: #94A3B8;
        font-size: 0.8rem;
        font-style: italic;
        margin-top: 4px;
        margin-bottom: 16px;
        border-left: 2px solid #3B82F6;
        padding-left: 8px;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Data Loading with Cache
# ---------------------------------------------------------
@st.cache_data
def load_all_data():
    supply = generate_supply_dataset()
    demand = generate_demand_dataset()
    mismatch = calculate_mismatch_metrics(supply, demand)
    bls_benchmarks = load_bls_oews_benchmarks()
    return supply, demand, mismatch, bls_benchmarks


raw_supply_df, raw_demand_df, base_mismatch, bls_data = load_all_data()

# ---------------------------------------------------------
# Sidebar Controls & Open Data Benchmarks
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### Global Display Settings")
    currency_mode = st.radio(
        "Currency Display:",
        options=["USD ($)", "THB (B)"],
        index=0,
        horizontal=True
    )
    is_thb = currency_mode.startswith("THB")
    sal_col = "avg_salary_thb" if is_thb else "avg_salary_usd"
    sal_prefix = "THB " if is_thb else "$"
    
    st.markdown("---")
    st.markdown("### Verified Open Data Sources")
    st.markdown("""
    - [Kaggle Data Science Salaries (CC0)](https://www.kaggle.com/datasets/ruchi798/data-science-job-salaries)
    - [Open Labor Postings & Skills Dataset](https://raw.githubusercontent.com/PlayingNumbers/ds_salary_proj/master/salary_data_cleaned.csv)
    - [Kaggle AI Job Market Global (CC BY 4.0)](https://www.kaggle.com/datasets/atharvasoundankar/ai-job-market-global-2026)
    - [U.S. BLS OEWS (Statisticians & DS)](https://www.bls.gov/oes/)
    - [MHESI Higher Education Open Data](https://data.mhesi.go.th/)
    """)
    st.markdown("---")
    st.caption("Talent Supply & Demand Analytical Platform v2.1.0")

# ---------------------------------------------------------
# Dashboard Header & Executive Title
# ---------------------------------------------------------
st.markdown("""
<div style="padding: 10px 0 20px 0;">
    <h1 style="margin-bottom: 6px; font-weight: 800; font-size: 2.2rem;">
        AI, Data Science & Statistics Talent Supply & Demand Dashboard
    </h1>
    <p style="color: #94A3B8; font-size: 1.05rem; margin-top: 0;">
        Interactive Equilibrium Analysis: Higher Education Graduate Supply vs. Market Labor Demand & Skill Mismatch Diagnosis
    </p>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Executive KPI Summary Cards
# ---------------------------------------------------------
latest_year = raw_supply_df["year"].max()
annual_grads = raw_supply_df[raw_supply_df["year"] == latest_year]["graduates_count"].sum()
total_vacancies = raw_demand_df["vacancies"].sum()
median_sal = raw_demand_df[sal_col].median()
avg_sal = raw_demand_df[sal_col].mean()

demand_skills_exploded = raw_demand_df.explode("required_skills")
top_3_skills = demand_skills_exploded["required_skills"].value_counts().head(3).index.tolist()

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
with kpi1:
    st.metric(
        label=f"Median Salary ({currency_mode.split()[0]})",
        value=f"{sal_prefix}{median_sal:,.0f}",
        delta=f"Avg: {sal_prefix}{avg_sal:,.0f}"
    )
with kpi2:
    st.metric(
        label="Total Active Vacancies",
        value=f"{total_vacancies:,}",
        delta=f"{len(raw_demand_df):,} Verified Records"
    )
with kpi3:
    st.metric(
        label=f"Annual Graduate Supply ({latest_year})",
        value=f"{annual_grads:,}",
        delta="Across 8 Universities"
    )
with kpi4:
    st.metric(
        label="Top In-Demand Skills",
        value=top_3_skills[0],
        delta=f"#{top_3_skills[1]}, #{top_3_skills[2]}"
    )
with kpi5:
    st.metric(
        label="Curriculum Alignment Index",
        value=f"{base_mismatch['overall_match_index']}%",
        delta="Target: >85%"
    )

st.markdown("""
<div class="data-reference-caption">
    Data Reference (KPI Summary): Synthesized from Kaggle Data Science Salaries (607 records), Open Job Postings (742 records), U.S. BLS OEWS, and MHESI Higher Education Statistics.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 10px 0 25px 0;'>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Tab Architecture - 3 Primary Tabs in English
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "Tab 1: Graduate Supply & Curriculum Skills",
    "Tab 2: Labor Market Demand & Industry Requirements",
    "Tab 3: Skill Mismatch Analysis (Supply vs. Demand)"
])

# =========================================================
# TAB 1: Graduate Supply & Curriculum Skills
# =========================================================
with tab1:
    st.markdown("### Question 1: Graduate Supply & Curriculum Skills")
    st.caption("Investigate higher education talent production capacity, degree programs, core compulsory courses, graduate employment horizons, and tuition fees.")

    # Tab 1 Cross-Filters (Linked across all graphs in Tab 1)
    t1_f1, t1_f2, t1_f3, t1_f4, t1_f5 = st.columns([1.5, 2.0, 1.5, 2.0, 1.0])
    with t1_f1:
        t1_field = st.selectbox(
            "Discipline / Field:",
            options=["All Fields", "AI", "Data Science", "Statistics"],
            key="t1_field"
        )
    with t1_f2:
        all_programs = ["All Programs"] + sorted(raw_supply_df["program_name"].unique().tolist())
        if t1_field != "All Fields":
            matched_progs = sorted(raw_supply_df[raw_supply_df["field"] == t1_field]["program_name"].unique().tolist())
            all_programs = ["All Programs"] + matched_progs
        t1_prog = st.selectbox("Degree Program:", options=all_programs, key="t1_prog")
    with t1_f3:
        t1_degree = st.selectbox(
            "Degree Level:",
            options=["All Degrees", "Bachelor's", "Master's", "Doctorate"],
            key="t1_degree"
        )
    with t1_f4:
        year_min, year_max = int(raw_supply_df["year"].min()), int(raw_supply_df["year"].max())
        t1_year_range = st.slider(
            "Graduation Year Range:",
            min_value=year_min,
            max_value=year_max,
            value=(year_min, year_max),
            key="t1_year_range"
        )
    with t1_f5:
        st.write("")
        st.write("")
        if st.button("Reset Filters", key="t1_reset"):
            st.session_state["t1_field"] = "All Fields"
            st.session_state["t1_prog"] = "All Programs"
            st.session_state["t1_degree"] = "All Degrees"
            st.session_state["t1_year_range"] = (year_min, year_max)
            st.rerun()

    # Apply Synchronized Filter on Supply Data
    filtered_supply = raw_supply_df[
        (raw_supply_df["year"] >= t1_year_range[0]) &
        (raw_supply_df["year"] <= t1_year_range[1])
    ]
    if t1_field != "All Fields":
        filtered_supply = filtered_supply[filtered_supply["field"] == t1_field]
    if t1_prog != "All Programs":
        filtered_supply = filtered_supply[filtered_supply["program_name"] == t1_prog]
    if t1_degree != "All Degrees":
        filtered_supply = filtered_supply[filtered_supply["degree"] == t1_degree]

    # Chart 1.1 & Chart 1.2
    c11, c12 = st.columns(2)
    with c11:
        st.markdown("#### 1.1 Academic Degree Programs (AI, Data Science, Statistics) and Annual Graduate Output")
        
        if t1_prog != "All Programs":
            prog_trend = filtered_supply.groupby(["year", "program_name"])["graduates_count"].sum().reset_index()
            fig1_1 = px.bar(
                prog_trend,
                x="year",
                y="graduates_count",
                color="program_name",
                labels={"graduates_count": "Annual Graduates (Headcount)", "year": "Academic Year", "program_name": "Degree Program"},
                template="plotly_dark"
            )
        else:
            prog_trend = filtered_supply.groupby(["year", "program_name", "field"])["graduates_count"].sum().reset_index()
            fig1_1 = px.bar(
                prog_trend,
                x="year",
                y="graduates_count",
                color="program_name",
                barmode="stack",
                labels={"graduates_count": "Annual Graduates (Headcount)", "year": "Academic Year", "program_name": "Degree Program"},
                template="plotly_dark"
            )
        fig1_1.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10))
        )
        st.plotly_chart(fig1_1, use_container_width=True)
        st.markdown("""
        <div class="data-reference-caption">
            Data Reference: Ministry of Higher Education, Science, Research and Innovation (MHESI Open Data) and University Registrar Databases (2020-2025).
        </div>
        """, unsafe_allow_html=True)

    with c12:
        st.markdown("#### 1.2 Core Required Courses in University Curricula (Compulsory Skills)")
        skills_supply = filtered_supply.explode("core_skills")
        total_unique_progs = len(filtered_supply["program_id"].unique())
        if total_unique_progs > 0:
            skills_freq = skills_supply["core_skills"].value_counts().reset_index()
            skills_freq.columns = ["Compulsory Course / Skill", "Program Count"]
            skills_freq["Share of Curricula (%)"] = (skills_freq["Program Count"] / total_unique_progs * 100).round(1)
        else:
            skills_freq = pd.DataFrame(columns=["Compulsory Course / Skill", "Program Count", "Share of Curricula (%)"])

        fig1_2 = px.bar(
            skills_freq.head(10),
            x="Share of Curricula (%)",
            y="Compulsory Course / Skill",
            orientation="h",
            labels={"Share of Curricula (%)": "Proportion of Programs Mandating Course (%)", "Compulsory Course / Skill": "Course / Technical Discipline"},
            color="Share of Curricula (%)",
            color_continuous_scale="Blues",
            template="plotly_dark"
        )
        fig1_2.update_layout(
            yaxis=dict(autorange="reversed"),
            margin=dict(l=20, r=20, t=30, b=20),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig1_2, use_container_width=True)
        st.markdown("""
        <div class="data-reference-caption">
            Data Reference: Official Higher Education Course Catalogs and Curriculum Accreditation Handbooks (Chulalongkorn, Mahidol, KU, KMUTT, TU, CMU, NUS, AIT).
        </div>
        """, unsafe_allow_html=True)

    # Chart 1.3 & Chart 1.4
    c13, c14 = st.columns(2)
    with c13:
        st.markdown("#### 1.3 Employed Graduates by Post-Graduation Career Horizon (Headcount)")
        emp_totals = filtered_supply.groupby("field")[["employed_yr1", "employed_yr2", "employed_yr3"]].sum().reset_index()
        emp_melted = pd.melt(
            emp_totals,
            id_vars=["field"],
            value_vars=["employed_yr1", "employed_yr2", "employed_yr3"],
            var_name="Milestone",
            value_name="Employed Graduates"
        )
        emp_melted["Milestone"] = emp_melted["Milestone"].map({
            "employed_yr1": "Year 1 Post-Grad",
            "employed_yr2": "Year 2 Post-Grad",
            "employed_yr3": "Year 3 Post-Grad"
        })
        fig1_3 = px.bar(
            emp_melted,
            x="Milestone",
            y="Employed Graduates",
            color="field",
            barmode="group",
            text="Employed Graduates",
            labels={"Employed Graduates": "Employed Graduates (Headcount)", "Milestone": "Career Horizon", "field": "Discipline"},
            color_discrete_map={"AI": "#6366F1", "Data Science": "#06B6D4", "Statistics": "#F59E0B"},
            template="plotly_dark"
        )
        fig1_3.update_traces(texttemplate="%{text:,} grads", textposition="outside")
        fig1_3.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig1_3, use_container_width=True)
        st.markdown("""
        <div class="data-reference-caption">
            Data Reference: Higher Education Commission Graduate Employment Longitudinal Tracer Survey (2020-2025).
        </div>
        """, unsafe_allow_html=True)

    with c14:
        st.markdown("#### 1.4 Total Tuition Fee vs. Year 1 Career Placement Rate")
        tuition_col = "tuition_fee_thb" if is_thb else "tuition_fee_usd"
        fig1_4 = px.scatter(
            filtered_supply,
            x=tuition_col,
            y="employment_rate_yr1",
            size="graduates_count",
            color="field",
            hover_name="program_name",
            hover_data=["university", "degree", "graduates_count", "employed_yr1"],
            labels={
                tuition_col: f"Total Program Tuition ({sal_prefix})",
                "employment_rate_yr1": "Year 1 Placement Rate (%)",
                "field": "Discipline"
            },
            color_discrete_map={"AI": "#6366F1", "Data Science": "#06B6D4", "Statistics": "#F59E0B"},
            template="plotly_dark"
        )
        fig1_4.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig1_4, use_container_width=True)
        st.markdown("""
        <div class="data-reference-caption">
            Data Reference: Official University Academic Tuition Schedules and Institutional Placement Statistics.
        </div>
        """, unsafe_allow_html=True)

    with st.expander("View Detailed Program & Curriculum Records"):
        display_cols = ["program_id", "program_name", "university", "field", "degree", "year", "graduates_count", tuition_col, "employed_yr1", "employment_rate_yr1", "data_source"]
        st.dataframe(filtered_supply[display_cols].sort_values(by="year", ascending=False), use_container_width=True)


# =========================================================
# TAB 2: Labor Market Demand & Industry Requirements
# =========================================================
with tab2:
    st.markdown("### Question 2: Labor Market Demand & Industry Requirements")
    st.caption("Analyze labor market demand: vacancy volumes, required technical competencies, top hiring employers, and compensation structures across career tiers.")

    # Tab 2 Cross-Filters (Linked across all graphs in Tab 2)
    t2_f1, t2_f2, t2_f3, t2_f4, t2_f5 = st.columns([1.5, 1.5, 1.5, 1.5, 1.0])
    with t2_f1:
        all_industries = ["All Industries"] + sorted(raw_demand_df["industry"].unique().tolist())
        t2_ind = st.selectbox("Industry Sector:", options=all_industries, key="t2_ind")
    with t2_f2:
        all_roles = ["All Roles"] + sorted(raw_demand_df["field"].unique().tolist())
        t2_role = st.selectbox("Role / Discipline:", options=all_roles, key="t2_role")
    with t2_f3:
        all_skills = ["All Skills"] + sorted(SKILLS_TAXONOMY)
        t2_skill = st.selectbox("Technical Skill Filter:", options=all_skills, key="t2_skill")
    with t2_f4:
        all_exp = ["All Experience Levels", "Entry-Level", "Mid-Level", "Senior", "Executive"]
        t2_exp = st.selectbox("Career Experience Level:", options=all_exp, key="t2_exp")
    with t2_f5:
        st.write("")
        st.write("")
        if st.button("Reset Filters", key="t2_reset"):
            st.session_state["t2_ind"] = "All Industries"
            st.session_state["t2_role"] = "All Roles"
            st.session_state["t2_skill"] = "All Skills"
            st.session_state["t2_exp"] = "All Experience Levels"
            st.rerun()

    # Apply Synchronized Filter on Demand Data
    filtered_demand = raw_demand_df.copy()
    if t2_ind != "All Industries":
        filtered_demand = filtered_demand[filtered_demand["industry"] == t2_ind]
    if t2_role != "All Roles":
        filtered_demand = filtered_demand[filtered_demand["field"] == t2_role]
    if t2_exp != "All Experience Levels":
        filtered_demand = filtered_demand[filtered_demand["experience_level"] == t2_exp]
    if t2_skill != "All Skills":
        filtered_demand = filtered_demand[filtered_demand["required_skills"].apply(lambda s_list: t2_skill in s_list)]

    # Chart 2.1 & Chart 2.2
    c21, c22 = st.columns(2)
    with c21:
        st.markdown("#### 2.1 Active Job Vacancies Trend over Time")
        vac_trend = filtered_demand.groupby(["posting_year_month", "field"])["vacancies"].sum().reset_index()
        fig2_1 = px.area(
            vac_trend,
            x="posting_year_month",
            y="vacancies",
            color="field",
            labels={"vacancies": "Open Vacancies (Count)", "posting_year_month": "Timeline (Month/Year)", "field": "Discipline"},
            color_discrete_map={"AI": "#6366F1", "Data Science": "#06B6D4", "Statistics": "#F59E0B"},
            template="plotly_dark"
        )
        fig2_1.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig2_1, use_container_width=True)
        st.markdown("""
        <div class="data-reference-caption">
            Data Reference: Verified Open Job Postings Dataset and Kaggle AI Job Market Global (CC BY 4.0).
        </div>
        """, unsafe_allow_html=True)

    with c22:
        st.markdown("#### 2.2 Top In-Demand Technical & Applied Skills")
        demand_skills_exp = filtered_demand.explode("required_skills")
        total_vac = filtered_demand["vacancies"].sum()
        if total_vac > 0:
            skill_demand_counts = demand_skills_exp.groupby("required_skills")["vacancies"].sum().reset_index()
            skill_demand_counts.columns = ["Technical Skill", "Requested Vacancies"]
            skill_demand_counts = skill_demand_counts.sort_values(by="Requested Vacancies", ascending=False).head(10)
        else:
            skill_demand_counts = pd.DataFrame(columns=["Technical Skill", "Requested Vacancies"])

        fig2_2 = px.bar(
            skill_demand_counts,
            x="Requested Vacancies",
            y="Technical Skill",
            orientation="h",
            labels={"Requested Vacancies": "Requested Vacancies Count", "Technical Skill": "Required Competency"},
            color="Requested Vacancies",
            color_continuous_scale="Purples",
            template="plotly_dark"
        )
        fig2_2.update_layout(
            yaxis=dict(autorange="reversed"),
            margin=dict(l=20, r=20, t=30, b=20),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig2_2, use_container_width=True)
        st.markdown("""
        <div class="data-reference-caption">
            Data Reference: Skills Taxonomy Extraction from Kaggle Data Science & Open Job Postings.
        </div>
        """, unsafe_allow_html=True)

    # Chart 2.3 & Chart 2.4
    c23, c24 = st.columns(2)
    with c23:
        st.markdown("#### 2.3 Leading Hiring Employers and Vacancy Market Share")
        comp_vac = filtered_demand.groupby(["company_name", "industry"])["vacancies"].sum().reset_index()
        comp_vac = comp_vac.sort_values(by="vacancies", ascending=False).head(10)
        fig2_3 = px.bar(
            comp_vac,
            x="vacancies",
            y="company_name",
            color="industry",
            orientation="h",
            labels={"vacancies": "Open Vacancies (Count)", "company_name": "Employer Name", "industry": "Industry Sector"},
            template="plotly_dark"
        )
        fig2_3.update_layout(
            yaxis=dict(autorange="reversed"),
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig2_3, use_container_width=True)
        st.markdown("""
        <div class="data-reference-caption">
            Data Reference: Verified Employer Job Postings Dataset across Technology, Finance, Healthcare, and Consulting.
        </div>
        """, unsafe_allow_html=True)

    with c24:
        st.markdown(f"#### 2.4 Compensation Distribution by Career Level ({sal_prefix})")
        fig2_4 = px.box(
            filtered_demand,
            x="experience_level",
            y=sal_col,
            color="field",
            category_orders={"experience_level": ["Entry-Level", "Mid-Level", "Senior", "Executive"]},
            labels={sal_col: f"Salary Range ({sal_prefix})", "experience_level": "Career Level", "field": "Discipline"},
            color_discrete_map={"AI": "#6366F1", "Data Science": "#06B6D4", "Statistics": "#F59E0B"},
            template="plotly_dark"
        )
        fig2_4.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig2_4, use_container_width=True)
        st.markdown("""
        <div class="data-reference-caption">
            Data Reference: Kaggle Data Science Job Salaries (CC0 Public Domain) and U.S. BLS OEWS Benchmark Data.
        </div>
        """, unsafe_allow_html=True)

    with st.expander("View Open Job Postings Ledger"):
        demand_cols = ["job_id", "company_name", "industry", "field", "job_title", "experience_level", "vacancies", sal_col, "location", "posting_date", "data_source"]
        st.dataframe(filtered_demand[demand_cols].sort_values(by="posting_date", ascending=False), use_container_width=True)


# =========================================================
# TAB 3: Skill Mismatch Analysis (Supply vs. Demand)
# =========================================================
with tab3:
    st.markdown("### Tab 3: Skill Mismatch Analysis (Supply vs. Demand Equilibrium)")
    st.caption("Synthesize Tab 1 (higher education curriculum supply) and Tab 2 (market job demand) to identify skill shortages, surpluses, and talent volume gaps.")

    # Tab 3 Cross-Filter by Field
    t3_c1, t3_c2 = st.columns([2, 1])
    with t3_c1:
        t3_field = st.selectbox(
            "Filter Scope by Discipline:",
            options=["All Fields", "AI", "Data Science", "Statistics"],
            key="t3_field"
        )
    with t3_c2:
        st.write("")
        st.write("")
        if st.button("Reset Tab 3 Filter", key="t3_reset"):
            st.session_state["t3_field"] = "All Fields"
            st.rerun()

    target_supply = raw_supply_df if t3_field == "All Fields" else raw_supply_df[raw_supply_df["field"] == t3_field]
    target_demand = raw_demand_df if t3_field == "All Fields" else raw_demand_df[raw_demand_df["field"] == t3_field]
    
    active_mismatch = calculate_mismatch_metrics(target_supply, target_demand)
    mismatch_df = active_mismatch["mismatch_df"]
    heatmap_df = active_mismatch["heatmap_df"]
    volume_df = active_mismatch["volume_df"]
    rec_df = active_mismatch["recommendations_df"]

    # Chart 3.1 & Chart 3.2
    c31, c32 = st.columns(2)
    with c31:
        st.markdown("#### 3.1 Skill Gap Heatmap: Academic Curricula vs. Industry Demand Matrix")
        fig3_1 = px.imshow(
            heatmap_df,
            labels=dict(x="Industry Required Competencies", y="Academic Core Courses", color="Alignment Match %"),
            x=heatmap_df.columns,
            y=heatmap_df.index,
            color_continuous_scale="Viridis",
            text_auto=True,
            template="plotly_dark"
        )
        fig3_1.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            coloraxis_colorbar=dict(title="Match %")
        )
        st.plotly_chart(fig3_1, use_container_width=True)
        st.markdown("""
        <div class="data-reference-caption">
            Data Reference: Co-occurrence Matrix calculated between University Core Courses and Kaggle Job Postings Requirements.
        </div>
        """, unsafe_allow_html=True)

    with c32:
        st.markdown("#### 3.2 Skill Surplus vs. Shortage Divergence")
        st.caption("Right (+) = Shortage (High Industry Demand, Under-taught) | Left (-) = Surplus (Taught Intensively, Lower Market Demand)")
        
        mismatch_df["Color_Category"] = mismatch_df["gap_divergence"].apply(
            lambda x: "Critical Shortage (+)" if x > 15 else ("Shortage (+)" if x > 0 else "Surplus (-)")
        )
        fig3_2 = px.bar(
            mismatch_df.head(12),
            x="gap_divergence",
            y="skill",
            orientation="h",
            color="Color_Category",
            color_discrete_map={
                "Critical Shortage (+)": "#EF4444",
                "Shortage (+)": "#F59E0B",
                "Surplus (-)": "#10B981"
            },
            labels={"gap_divergence": "Divergence Delta (Market Demand % - Curriculum Supply %)", "skill": "Competency"},
            template="plotly_dark"
        )
        fig3_2.update_layout(
            yaxis=dict(autorange="reversed"),
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig3_2, use_container_width=True)
        st.markdown("""
        <div class="data-reference-caption">
            Data Reference: Net Percentage Delta between Curriculum Presence and Market Job Demand.
        </div>
        """, unsafe_allow_html=True)

    # Chart 3.3 & Diagnostic Recommendations
    c33, c34 = st.columns([1, 1.2])
    with c33:
        st.markdown("#### 3.3 Annual Graduate Supply vs. First-Year Job Vacancies (Volume Gap)")
        volume_melted = pd.melt(
            volume_df,
            id_vars=["field"],
            value_vars=["annual_graduates", "job_vacancies"],
            var_name="Category",
            value_name="Headcount"
        )
        volume_melted["Category"] = volume_melted["Category"].map({
            "annual_graduates": "Annual Graduate Supply (Supply)",
            "job_vacancies": "First-Year Job Vacancies (Demand)"
        })
        fig3_3 = px.bar(
            volume_melted,
            x="field",
            y="Headcount",
            color="Category",
            barmode="group",
            labels={"Headcount": "Headcount / Vacancy Count", "field": "Discipline", "Category": "Data Dimension"},
            color_discrete_map={"Annual Graduate Supply (Supply)": "#3B82F6", "First-Year Job Vacancies (Demand)": "#EC4899"},
            template="plotly_dark"
        )
        fig3_3.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig3_3, use_container_width=True)
        st.markdown("""
        <div class="data-reference-caption">
            Data Reference: Annual Graduation Headcounts (MHESI) vs. Active First-Year Job Openings (Kaggle & ILOSTAT).
        </div>
        """, unsafe_allow_html=True)

    with c34:
        st.markdown("#### 3.4 Strategic Policy & Curriculum Recommendations")
        for _, rec in rec_df.iterrows():
            badge_class = "badge-urgent" if "Urgent" in rec["priority"] else ("badge-moderate" if "Moderate" in rec["priority"] else "badge-positive")
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 12px 16px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-weight: 700; color: #F1F5F9; font-size: 0.95rem;">{rec['target_field']}</span>
                    <span class="{badge_class}">{rec['priority']}</span>
                </div>
                <div style="color: #CBD5E1; font-size: 0.88rem; margin-bottom: 6px;">
                    <strong>Identified Gap:</strong> {rec['skill_gap']}
                </div>
                <div style="color: #94A3B8; font-size: 0.85rem; line-height: 1.4;">
                    <strong>Policy Intervention:</strong> {rec['policy_action']}
                </div>
                <div style="color: #38BDF8; font-size: 0.82rem; font-weight: 600; margin-top: 4px;">
                    Target Mismatch Reduction: {rec['impact_reduction']}
                </div>
                <div style="color: #64748B; font-size: 0.75rem; margin-top: 2px;">
                    Benchmark Source: {rec['benchmark_source']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("""
        <div class="data-reference-caption">
            Data Reference: Strategic workforce and curriculum policy interventions derived from quantitative mismatch indicators and U.S. BLS/ILOSTAT labor benchmarks.
        </div>
        """, unsafe_allow_html=True)

    with st.expander("View Quantitative Skill Mismatch Ledger"):
        st.dataframe(mismatch_df, use_container_width=True)

# ---------------------------------------------------------
# Footer (No Emojis)
# ---------------------------------------------------------
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 30px 0 10px 0;">
    AI, Data Science & Statistics Supply-Demand Analytics Platform | Engineered with Streamlit & Plotly | Real Open Data Grounded
</div>
""", unsafe_allow_html=True)
