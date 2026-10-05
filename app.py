"""
AI, Data Science & Statistics Talent Supply & Demand Dashboard
Interactive analytical platform analyzing graduate supply, market demand, and skill mismatch.
Stack: Streamlit, Plotly Express & Graph Objects, Pandas
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
    SKILLS_TAXONOMY
)

# ---------------------------------------------------------
# Page Configuration
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
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
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
    return supply, demand, mismatch


raw_supply_df, raw_demand_df, base_mismatch = load_all_data()

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
    st.markdown("### Open Data Benchmarks")
    st.markdown("""
    - [AI Job Market Global 2026 (Kaggle)](https://www.kaggle.com/datasets/atharvasoundankar/ai-job-market-global-2026)
    - [Data Science Salaries (Kaggle CC0)](https://www.kaggle.com/datasets/ruchi798/data-science-job-salaries)
    - [U.S. BLS OEWS (Statisticians & DS)](https://www.bls.gov/oes/)
    - [ILOSTAT Global Labor Portal](https://ilostat.ilo.org/data/)
    """)
    st.markdown("---")
    st.caption("AI & Data Science Talent Supply & Demand Dashboard v1.0.0")

# ---------------------------------------------------------
# Dashboard Header & Executive Title
# ---------------------------------------------------------
st.markdown("""
<div style="padding: 10px 0 20px 0;">
    <h1 style="margin-bottom: 6px; font-weight: 800; font-size: 2.2rem;">
        AI, Data Science & Statistics Talent Supply & Demand Dashboard
    </h1>
    <p style="color: #94A3B8; font-size: 1.05rem; margin-top: 0;">
        Equilibrium analysis of Higher Education Curriculum Supply vs. Market Labor Demand & Skill Mismatch Diagnosis
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

# Determine Top 3 In-Demand Skills
demand_skills_exploded = raw_demand_df.explode("required_skills")
top_3_skills = demand_skills_exploded["required_skills"].value_counts().head(3).index.tolist()
top_3_skills_str = ", ".join(top_3_skills)

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
        delta=f"{len(raw_demand_df):,} Postings"
    )
with kpi3:
    st.metric(
        label=f"Annual Graduates ({latest_year})",
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

st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 15px 0 25px 0;'>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Tab Architecture
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "Graduate Supply & Curriculum",
    "Market Demand & Compensation",
    "Skill Mismatch & Policy Analysis"
])

# =========================================================
# TAB 1: Graduate Supply & Curriculum Skills
# =========================================================
with tab1:
    st.markdown("### Higher Education Production Capacity & Academic Curriculum")
    st.caption("Investigate annual graduate output, core curriculum course distribution, tuition fees, and career placement rates.")

    # Tab 1 Cross-Filters
    t1_c1, t1_c2, t1_c3, t1_c4 = st.columns([1.5, 1.5, 2, 1])
    with t1_c1:
        t1_field = st.selectbox(
            "Field Filter:",
            options=["All Fields", "AI", "Data Science", "Statistics"],
            key="t1_field"
        )
    with t1_c2:
        t1_degree = st.selectbox(
            "Degree Level:",
            options=["All Degrees", "Bachelor's", "Master's", "Doctorate"],
            key="t1_degree"
        )
    with t1_c3:
        year_min, year_max = int(raw_supply_df["year"].min()), int(raw_supply_df["year"].max())
        t1_year_range = st.slider(
            "Graduation Year Range:",
            min_value=year_min,
            max_value=year_max,
            value=(year_min, year_max),
            key="t1_year_range"
        )
    with t1_c4:
        st.write("")
        st.write("")
        if st.button("Reset Filters", key="t1_reset"):
            st.session_state["t1_field"] = "All Fields"
            st.session_state["t1_degree"] = "All Degrees"
            st.session_state["t1_year_range"] = (year_min, year_max)
            st.rerun()

    # Filter Supply Data
    filtered_supply = raw_supply_df[
        (raw_supply_df["year"] >= t1_year_range[0]) &
        (raw_supply_df["year"] <= t1_year_range[1])
    ]
    if t1_field != "All Fields":
        filtered_supply = filtered_supply[filtered_supply["field"] == t1_field]
    if t1_degree != "All Degrees":
        filtered_supply = filtered_supply[filtered_supply["degree"] == t1_degree]

    # Chart 1.1 & Chart 1.2
    c11, c12 = st.columns(2)
    with c11:
        st.markdown("#### 1.1 Production Capacity by Discipline & Year")
        grad_trend = filtered_supply.groupby(["year", "field"])["graduates_count"].sum().reset_index()
        fig1_1 = px.bar(
            grad_trend,
            x="year",
            y="graduates_count",
            color="field",
            barmode="group",
            labels={"graduates_count": "Annual Graduates", "year": "Year", "field": "Field"},
            color_discrete_map={"AI": "#6366F1", "Data Science": "#06B6D4", "Statistics": "#F59E0B"},
            template="plotly_dark"
        )
        fig1_1.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig1_1, use_container_width=True)

    with c12:
        st.markdown("#### 1.2 Core Required Skills in University Curricula")
        # Explode core skills
        skills_supply = filtered_supply.explode("core_skills")
        total_unique_progs = len(filtered_supply["program_id"].unique())
        if total_unique_progs > 0:
            skills_freq = skills_supply["core_skills"].value_counts().reset_index()
            skills_freq.columns = ["Skill", "Program_Count"]
            skills_freq["Percentage"] = (skills_freq["Program_Count"] / total_unique_progs * 100).round(1)
        else:
            skills_freq = pd.DataFrame(columns=["Skill", "Program_Count", "Percentage"])

        fig1_2 = px.bar(
            skills_freq.head(10),
            x="Percentage",
            y="Skill",
            orientation="h",
            labels={"Percentage": "% of Compulsory Curricula", "Skill": "Curriculum Subject"},
            color="Percentage",
            color_continuous_scale="Blues",
            template="plotly_dark"
        )
        fig1_2.update_layout(
            yaxis=dict(autorange="reversed"),
            margin=dict(l=20, r=20, t=30, b=20),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig1_2, use_container_width=True)

    # Chart 1.3 & Chart 1.4
    c13, c14 = st.columns(2)
    with c13:
        st.markdown("#### 1.3 Longitudinal Post-Graduation Employment Rate")
        # Employment rate evolution Year 1, Year 2, Year 3 by field
        emp_rates = filtered_supply.groupby("field")[["employment_rate_yr1", "employment_rate_yr2", "employment_rate_yr3"]].mean().reset_index()
        emp_melted = pd.melt(
            emp_rates,
            id_vars=["field"],
            value_vars=["employment_rate_yr1", "employment_rate_yr2", "employment_rate_yr3"],
            var_name="Milestone",
            value_name="Rate"
        )
        emp_melted["Milestone"] = emp_melted["Milestone"].map({
            "employment_rate_yr1": "Year 1 Post-Grad",
            "employment_rate_yr2": "Year 2 Post-Grad",
            "employment_rate_yr3": "Year 3 Post-Grad"
        })
        fig1_3 = px.bar(
            emp_melted,
            x="Milestone",
            y="Rate",
            color="field",
            barmode="group",
            text="Rate",
            labels={"Rate": "Employed Graduates (%)", "Milestone": "Career Horizon", "field": "Field"},
            color_discrete_map={"AI": "#6366F1", "Data Science": "#06B6D4", "Statistics": "#F59E0B"},
            template="plotly_dark"
        )
        fig1_3.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig1_3.update_layout(
            yaxis_range=[50, 105],
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig1_3, use_container_width=True)

    with c14:
        st.markdown("#### 1.4 Tuition Fee vs. Year 1 Employment Success")
        tuition_col = "tuition_fee_thb" if is_thb else "tuition_fee_usd"
        fig1_4 = px.scatter(
            filtered_supply,
            x=tuition_col,
            y="employment_rate_yr1",
            size="graduates_count",
            color="field",
            hover_name="program_name",
            hover_data=["university", "degree", "graduates_count"],
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

    with st.expander("View Program & Curriculum Records"):
        display_cols = ["program_id", "program_name", "university", "field", "degree", "year", "graduates_count", tuition_col, "employment_rate_yr1"]
        st.dataframe(filtered_supply[display_cols].sort_values(by="year", ascending=False), use_container_width=True)


# =========================================================
# TAB 2: Market Demand & Compensation
# =========================================================
with tab2:
    st.markdown("### Labor Market Demand, In-Demand Skills & Compensation Trends")
    st.caption("Grounded in Kaggle AI Job Market Global, Global Data Science Salaries, and U.S. BLS open benchmarks.")

    # Tab 2 Cross-Filters
    t2_c1, t2_c2, t2_c3, t2_c4 = st.columns([1.5, 1.5, 1.5, 1])
    with t2_c1:
        all_industries = ["All Industries"] + sorted(raw_demand_df["industry"].unique().tolist())
        t2_ind = st.selectbox("Industry Sector:", options=all_industries, key="t2_ind")
    with t2_c2:
        all_exp = ["All Experience Levels", "Entry-Level", "Mid-Level", "Senior", "Executive"]
        t2_exp = st.selectbox("Experience Level:", options=all_exp, key="t2_exp")
    with t2_c3:
        all_locs = ["All Locations"] + sorted(raw_demand_df["location"].unique().tolist())
        t2_loc = st.selectbox("Location / Region:", options=all_locs, key="t2_loc")
    with t2_c4:
        st.write("")
        st.write("")
        if st.button("Reset Filters", key="t2_reset"):
            st.session_state["t2_ind"] = "All Industries"
            st.session_state["t2_exp"] = "All Experience Levels"
            st.session_state["t2_loc"] = "All Locations"
            st.rerun()

    # Filter Demand Data
    filtered_demand = raw_demand_df.copy()
    if t2_ind != "All Industries":
        filtered_demand = filtered_demand[filtered_demand["industry"] == t2_ind]
    if t2_exp != "All Experience Levels":
        filtered_demand = filtered_demand[filtered_demand["experience_level"] == t2_exp]
    if t2_loc != "All Locations":
        filtered_demand = filtered_demand[filtered_demand["location"] == t2_loc]

    # Chart 2.1 & Chart 2.2
    c21, c22 = st.columns(2)
    with c21:
        st.markdown("#### 2.1 Open Job Vacancies Trend by Discipline")
        vac_trend = filtered_demand.groupby(["posting_year_month", "field"])["vacancies"].sum().reset_index()
        fig2_1 = px.area(
            vac_trend,
            x="posting_year_month",
            y="vacancies",
            color="field",
            labels={"vacancies": "Open Vacancies", "posting_year_month": "Month", "field": "Field"},
            color_discrete_map={"AI": "#6366F1", "Data Science": "#06B6D4", "Statistics": "#F59E0B"},
            template="plotly_dark"
        )
        fig2_1.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig2_1, use_container_width=True)

    with c22:
        st.markdown("#### 2.2 Top In-Demand Technical & Applied Skills")
        demand_skills_exp = filtered_demand.explode("required_skills")
        total_vac = filtered_demand["vacancies"].sum()
        if total_vac > 0:
            skill_demand_counts = demand_skills_exp.groupby("required_skills")["vacancies"].sum().reset_index()
            skill_demand_counts.columns = ["Skill", "Vacancies"]
            skill_demand_counts = skill_demand_counts.sort_values(by="Vacancies", ascending=False).head(10)
        else:
            skill_demand_counts = pd.DataFrame(columns=["Skill", "Vacancies"])

        fig2_2 = px.bar(
            skill_demand_counts,
            x="Vacancies",
            y="Skill",
            orientation="h",
            labels={"Vacancies": "Requested Vacancies Count", "Skill": "Required Skill"},
            color="Vacancies",
            color_continuous_scale="Purples",
            template="plotly_dark"
        )
        fig2_2.update_layout(
            yaxis=dict(autorange="reversed"),
            margin=dict(l=20, r=20, t=30, b=20),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig2_2, use_container_width=True)

    # Chart 2.3 & Chart 2.4
    c23, c24 = st.columns(2)
    with c23:
        st.markdown("#### 2.3 Top Hiring Employers & Market Share")
        comp_vac = filtered_demand.groupby(["company_name", "industry"])["vacancies"].sum().reset_index()
        comp_vac = comp_vac.sort_values(by="vacancies", ascending=False).head(10)
        fig2_3 = px.bar(
            comp_vac,
            x="vacancies",
            y="company_name",
            color="industry",
            orientation="h",
            labels={"vacancies": "Open Postings (Vacancies)", "company_name": "Employer", "industry": "Sector"},
            template="plotly_dark"
        )
        fig2_3.update_layout(
            yaxis=dict(autorange="reversed"),
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig2_3, use_container_width=True)

    with c24:
        st.markdown(f"#### 2.4 Compensation Distribution by Career Level ({sal_prefix})")
        fig2_4 = px.box(
            filtered_demand,
            x="experience_level",
            y=sal_col,
            color="field",
            category_orders={"experience_level": ["Entry-Level", "Mid-Level", "Senior", "Executive"]},
            labels={sal_col: f"Salary ({sal_prefix})", "experience_level": "Career Level", "field": "Field"},
            color_discrete_map={"AI": "#6366F1", "Data Science": "#06B6D4", "Statistics": "#F59E0B"},
            template="plotly_dark"
        )
        fig2_4.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig2_4, use_container_width=True)

    with st.expander("View Open Job Vacancy Postings"):
        demand_cols = ["job_id", "company_name", "industry", "field", "job_title", "experience_level", "vacancies", sal_col, "location", "posting_date"]
        st.dataframe(filtered_demand[demand_cols].sort_values(by="posting_date", ascending=False), use_container_width=True)


# =========================================================
# TAB 3: Skill Mismatch & Policy Analysis
# =========================================================
with tab3:
    st.markdown("### Supply vs. Demand Equilibrium & Skill Mismatch Diagnosis")
    st.caption("Quantitative identification of curriculum blindspots, skill shortages, and strategic workforce interventions.")

    # Re-calculate mismatch based on active global/current data
    active_mismatch = calculate_mismatch_metrics(raw_supply_df, raw_demand_df)
    mismatch_df = active_mismatch["mismatch_df"]
    heatmap_df = active_mismatch["heatmap_df"]
    volume_df = active_mismatch["volume_df"]
    rec_df = active_mismatch["recommendations_df"]

    # Chart 3.1 & Chart 3.2
    c31, c32 = st.columns(2)
    with c31:
        st.markdown("#### 3.1 Skill Gap Heatmap: Academic Curricula vs. Industry Demand")
        fig3_1 = px.imshow(
            heatmap_df,
            labels=dict(x="Industry Required Skills", y="Academic Core Courses", color="Alignment Match %"),
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

    with c32:
        st.markdown("#### 3.2 Skill Surplus vs. Shortage Divergence")
        st.caption("Right (+) = Shortage (High Demand, Under-taught) | Left (-) = Surplus (Taught widely, Low relative demand)")
        
        # Color scale based on gap divergence
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
            labels={"gap_divergence": "Divergence (Demand % - Supply %)", "skill": "Skill"},
            template="plotly_dark"
        )
        fig3_2.update_layout(
            yaxis=dict(autorange="reversed"),
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig3_2, use_container_width=True)

    # Chart 3.3 & Diagnostic Recommendations
    c33, c34 = st.columns([1, 1.2])
    with c33:
        st.markdown("#### 3.3 Talent Volume vs. Job Vacancies Gap")
        volume_melted = pd.melt(
            volume_df,
            id_vars=["field"],
            value_vars=["annual_graduates", "job_vacancies"],
            var_name="Category",
            value_name="Count"
        )
        volume_melted["Category"] = volume_melted["Category"].map({
            "annual_graduates": "Annual Graduate Supply",
            "job_vacancies": "First-Year Job Vacancies"
        })
        fig3_3 = px.bar(
            volume_melted,
            x="field",
            y="Count",
            color="Category",
            barmode="group",
            labels={"Count": "Headcount", "field": "Discipline", "Category": "Category"},
            color_discrete_map={"Annual Graduate Supply": "#3B82F6", "First-Year Job Vacancies": "#EC4899"},
            template="plotly_dark"
        )
        fig3_3.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig3_3, use_container_width=True)

    with c34:
        st.markdown("#### 3.4 Diagnostic Policy & Curriculum Recommendations")
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
                    <strong>Intervention:</strong> {rec['policy_action']}
                </div>
                <div style="color: #38BDF8; font-size: 0.82rem; font-weight: 600; margin-top: 4px;">
                    Projected Impact: {rec['impact_reduction']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    with st.expander("Complete Quantitative Mismatch Ledger"):
        st.dataframe(mismatch_df, use_container_width=True)

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 30px 0 10px 0;">
    AI, Data Science & Statistics Supply-Demand Analytics Platform | Engineered with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
