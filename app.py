"""
AI, Data Science & Statistics Talent Supply & Demand Dashboard
Interactive analytical platform analyzing graduate supply, market demand, and skill mismatch.
Stack: Streamlit, Plotly Express & Graph Objects, Pandas
Data Sources: Kaggle Data Science Salaries (CC0), Open Job Postings, U.S. BLS OEWS, MHESI Open Data
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
        font-size: 1.0rem !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
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
    st.caption("Talent Supply & Demand Analytical Platform v2.0.0")

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
# Tab Architecture - 3 Primary Tabs
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "Tab 1: ปริมาณคนที่จบ และ Skills ที่เรียนมา (Graduate Supply & Curriculum)",
    "Tab 2: ปริมาณงานที่จ้าง และ Skills ที่ต้องการ (Market Demand & Required Skills)",
    "Tab 3: วิเคราะห์ Skills Mismatch (Supply vs. Demand Analysis)"
])

# =========================================================
# TAB 1: ปริมาณคนที่จบ และ Skills ที่เรียนมา
# =========================================================
with tab1:
    st.markdown("### คำถามที่ 1: ปริมาณคนที่จบ และ Skills ที่เรียนมา (Graduate Supply & Curriculum Skills)")
    st.caption("วิเคราะห์ศักยภาพการผลิตกำลังคนของสถาบันการศึกษา จำแนกตามหลักสูตร รายวิชาบังคับ อัตราการได้งานทำ และค่าเทอม")

    # Tab 1 Cross-Filters (เชื่อมโยงทุกกราฟ)
    t1_f1, t1_f2, t1_f3, t1_f4, t1_f5 = st.columns([1.5, 2.0, 1.5, 2.0, 1.0])
    with t1_f1:
        t1_field = st.selectbox(
            "สาขาวิชา (Field):",
            options=["All Fields", "AI", "Data Science", "Statistics"],
            key="t1_field"
        )
    with t1_f2:
        all_programs = ["All Programs"] + sorted(raw_supply_df["program_name"].unique().tolist())
        if t1_field != "All Fields":
            matched_progs = sorted(raw_supply_df[raw_supply_df["field"] == t1_field]["program_name"].unique().tolist())
            all_programs = ["All Programs"] + matched_progs
        t1_prog = st.selectbox("ชื่อหลักสูตร (Program Name):", options=all_programs, key="t1_prog")
    with t1_f3:
        t1_degree = st.selectbox(
            "ระดับการศึกษา (Degree):",
            options=["All Degrees", "Bachelor's", "Master's", "Doctorate"],
            key="t1_degree"
        )
    with t1_f4:
        year_min, year_max = int(raw_supply_df["year"].min()), int(raw_supply_df["year"].max())
        t1_year_range = st.slider(
            "ช่วงปีที่จบ (Year Range):",
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

    # Sub-controls for Graph 1.1 Breakdown
    c11, c12 = st.columns(2)
    with c11:
        st.markdown("#### 1.1 ชื่อหลักสูตรที่ผลิตบัณฑิต (AI, Data Science, Stat) และจำนวนที่ผลิตได้ในแต่ละปี")
        
        # Determine grouping dimension based on selection
        if t1_prog != "All Programs":
            prog_trend = filtered_supply.groupby(["year", "program_name"])["graduates_count"].sum().reset_index()
            fig1_1 = px.bar(
                prog_trend,
                x="year",
                y="graduates_count",
                color="program_name",
                labels={"graduates_count": "จำนวนบัณฑิตที่จบ (คน)", "year": "ปีการศึกษา", "program_name": "ชื่อหลักสูตร"},
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
                labels={"graduates_count": "จำนวนบัณฑิตที่จบ (คน)", "year": "ปีการศึกษา", "program_name": "ชื่อหลักสูตร"},
                template="plotly_dark"
            )
        fig1_1.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10))
        )
        st.plotly_chart(fig1_1, use_container_width=True)
        st.markdown("""
        <div class="data-reference-caption">
            Data Reference: กระทรวงการอุดมศึกษา วิทยาศาสตร์ วิจัยและนวัตกรรม (MHESI Open Data) และทะเบียนมหาวิทยาลัย (Chulalongkorn, Mahidol, KU, KMUTT, TU, CMU, NUS, AIT) 2020-2025.
        </div>
        """, unsafe_allow_html=True)

    with c12:
        st.markdown("#### 1.2 รายวิชาบังคับในแต่ละหลักสูตรที่ตรงกับสายงาน (Core Required Curriculum Skills)")
        skills_supply = filtered_supply.explode("core_skills")
        total_unique_progs = len(filtered_supply["program_id"].unique())
        if total_unique_progs > 0:
            skills_freq = skills_supply["core_skills"].value_counts().reset_index()
            skills_freq.columns = ["รายวิชาบังคับ", "จำนวนหลักสูตร"]
            skills_freq["สัดส่วนหลักสูตรที่เปิดสอน (%)"] = (skills_freq["จำนวนหลักสูตร"] / total_unique_progs * 100).round(1)
        else:
            skills_freq = pd.DataFrame(columns=["รายวิชาบังคับ", "จำนวนหลักสูตร", "สัดส่วนหลักสูตรที่เปิดสอน (%)"])

        fig1_2 = px.bar(
            skills_freq.head(10),
            x="สัดส่วนหลักสูตรที่เปิดสอน (%)",
            y="รายวิชาบังคับ",
            orientation="h",
            labels={"สัดส่วนหลักสูตรที่เปิดสอน (%)": "สัดส่วนหลักสูตรที่บรรจุเป็นวิชาบังคับ (%)", "รายวิชาบังคับ": "รายวิชา / ทักษะ"},
            color="สัดส่วนหลักสูตรที่เปิดสอน (%)",
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
            Data Reference: คู่มือหลักสูตรและรายวิชาบังคับจากสภาวิชาชีพและหลักสูตรระดับอุดมศึกษา (Curriculum Catalogs & Accreditation Records).
        </div>
        """, unsafe_allow_html=True)

    # Chart 1.3 & Chart 1.4
    c13, c14 = st.columns(2)
    with c13:
        st.markdown("#### 1.3 จำนวนบัณฑิตที่ได้งานทำในปีแรก ปีที่สอง และปีที่สาม หลังจบการศึกษา (Employed Headcount)")
        # Show actual headcount of employed graduates across year milestones
        emp_totals = filtered_supply.groupby("field")[["employed_yr1", "employed_yr2", "employed_yr3"]].sum().reset_index()
        emp_melted = pd.melt(
            emp_totals,
            id_vars=["field"],
            value_vars=["employed_yr1", "employed_yr2", "employed_yr3"],
            var_name="Milestone",
            value_name="จำนวนผู้มีงานทำ (คน)"
        )
        emp_melted["Milestone"] = emp_melted["Milestone"].map({
            "employed_yr1": "ปีแรก (Year 1)",
            "employed_yr2": "ปีที่สอง (Year 2)",
            "employed_yr3": "ปีที่สาม (Year 3)"
        })
        fig1_3 = px.bar(
            emp_melted,
            x="Milestone",
            y="จำนวนผู้มีงานทำ (คน)",
            color="field",
            barmode="group",
            text="จำนวนผู้มีงานทำ (คน)",
            labels={"จำนวนผู้มีงานทำ (คน)": "จำนวนบัณฑิตที่ได้งานทำ (คน)", "Milestone": "ช่วงเวลาหลังจบ", "field": "สาขาวิชา"},
            color_discrete_map={"AI": "#6366F1", "Data Science": "#06B6D4", "Statistics": "#F59E0B"},
            template="plotly_dark"
        )
        fig1_3.update_traces(texttemplate="%{text:,} คน", textposition="outside")
        fig1_3.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig1_3, use_container_width=True)
        st.markdown("""
        <div class="data-reference-caption">
            Data Reference: แบบสำรวจภาวะการมีงานทำของบัณฑิต (Graduate Employment Longitudinal Tracer Survey, สกอ./อว. 2020-2025).
        </div>
        """, unsafe_allow_html=True)

    with c14:
        st.markdown("#### 1.4 ค่าเทอมตลอดหลักสูตรเทียบกับอัตราการได้งานทำปีแรก (Tuition Fee vs. Employment Rate)")
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
                tuition_col: f"ค่าเทอมตลอดหลักสูตร ({sal_prefix})",
                "employment_rate_yr1": "อัตราการได้งานทำปีแรก (%)",
                "field": "สาขาวิชา"
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
            Data Reference: ประกาศอัตราค่าธรรมเนียมการศึกษาของมหาวิทยาลัย และฐานข้อมูลการได้งานทำของบัณฑิตจบใหม่.
        </div>
        """, unsafe_allow_html=True)

    with st.expander("ดูตารางข้อมูลรายละเอียดหลักสูตรและการผลิตบัณฑิต (Curriculum Records)"):
        display_cols = ["program_id", "program_name", "university", "field", "degree", "year", "graduates_count", tuition_col, "employed_yr1", "employment_rate_yr1", "data_source"]
        st.dataframe(filtered_supply[display_cols].sort_values(by="year", ascending=False), use_container_width=True)


# =========================================================
# TAB 2: ปริมาณงานที่จ้าง และ Skills ที่ต้องการ
# =========================================================
with tab2:
    st.markdown("### คำถามที่ 2: ปริมาณงานที่จ้าง และ Skills ที่ต้องการ (Market Demand & Industry Requirements)")
    st.caption("วิเคราะห์อุปสงค์ตลาดแรงงาน: ปริมาณตำแหน่งงานว่าง ทักษะที่ต้องการ บริษัทที่เปิดรับ และโครงสร้างค่าตอบแทนในแต่ละระดับการทำงาน")

    # Tab 2 Cross-Filters (เชื่อมโยงทุกกราฟ)
    t2_f1, t2_f2, t2_f3, t2_f4, t2_f5 = st.columns([1.5, 1.5, 1.5, 1.5, 1.0])
    with t2_f1:
        all_industries = ["All Industries"] + sorted(raw_demand_df["industry"].unique().tolist())
        t2_ind = st.selectbox("กลุ่มอุตสาหกรรม (Industry Sector):", options=all_industries, key="t2_ind")
    with t2_f2:
        all_roles = ["All Roles"] + sorted(raw_demand_df["field"].unique().tolist())
        t2_role = st.selectbox("สายงาน (Role / Discipline):", options=all_roles, key="t2_role")
    with t2_f3:
        all_skills = ["All Skills"] + sorted(SKILLS_TAXONOMY)
        t2_skill = st.selectbox("ทักษะที่ต้องการ (Skill Filter):", options=all_skills, key="t2_skill")
    with t2_f4:
        all_exp = ["All Experience Levels", "Entry-Level", "Mid-Level", "Senior", "Executive"]
        t2_exp = st.selectbox("ระดับประสบการณ์ (Experience Level):", options=all_exp, key="t2_exp")
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
        st.markdown("#### 2.1 ปริมาณตำแหน่งที่ว่างในตลาดตามไทม์ไลน์ (Open Job Vacancies Trend)")
        vac_trend = filtered_demand.groupby(["posting_year_month", "field"])["vacancies"].sum().reset_index()
        fig2_1 = px.area(
            vac_trend,
            x="posting_year_month",
            y="vacancies",
            color="field",
            labels={"vacancies": "ปริมาณตำแหน่งงานว่าง (อัตรา)", "posting_year_month": "ช่วงเวลา (เดือน/ปี)", "field": "สายงาน"},
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
            Data Reference: ข้อมูลประกาศรับสมัครงานจริง (Open Job Postings) และ Kaggle AI Job Market Global (CC BY 4.0).
        </div>
        """, unsafe_allow_html=True)

    with c22:
        st.markdown("#### 2.2 Skills ที่ตลาดต้องการมากที่สุด (Top In-Demand Technical & Applied Skills)")
        demand_skills_exp = filtered_demand.explode("required_skills")
        total_vac = filtered_demand["vacancies"].sum()
        if total_vac > 0:
            skill_demand_counts = demand_skills_exp.groupby("required_skills")["vacancies"].sum().reset_index()
            skill_demand_counts.columns = ["ทักษะ", "จำนวนตำแหน่งที่ต้องการ"]
            skill_demand_counts = skill_demand_counts.sort_values(by="จำนวนตำแหน่งที่ต้องการ", ascending=False).head(10)
        else:
            skill_demand_counts = pd.DataFrame(columns=["ทักษะ", "จำนวนตำแหน่งที่ต้องการ"])

        fig2_2 = px.bar(
            skill_demand_counts,
            x="จำนวนตำแหน่งที่ต้องการ",
            y="ทักษะ",
            orientation="h",
            labels={"จำนวนตำแหน่งที่ต้องการ": "จำนวนตำแหน่งงานที่ระบุทักษะนี้ (อัตรา)", "ทักษะ": "ทักษะที่ต้องการ"},
            color="จำนวนตำแหน่งที่ต้องการ",
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
            Data Reference: การจำแนกทักษะจากประกาศรับสมัครงานจริง (Skills Taxonomy Extraction จาก Kaggle Data Science & Open Postings).
        </div>
        """, unsafe_allow_html=True)

    # Chart 2.3 & Chart 2.4
    c23, c24 = st.columns(2)
    with c23:
        st.markdown("#### 2.3 บริษัทที่เปิดรับสมัครงานและส่วนแบ่งตำแหน่งงานว่าง (Top Hiring Companies)")
        comp_vac = filtered_demand.groupby(["company_name", "industry"])["vacancies"].sum().reset_index()
        comp_vac = comp_vac.sort_values(by="vacancies", ascending=False).head(10)
        fig2_3 = px.bar(
            comp_vac,
            x="vacancies",
            y="company_name",
            color="industry",
            orientation="h",
            labels={"vacancies": "จำนวนตำแหน่งงานว่าง (อัตรา)", "company_name": "ชื่อบริษัท", "industry": "กลุ่มอุตสาหกรรม"},
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
            Data Reference: ฐานข้อมูลบริษัทผู้ว่าจ้างจริงจาก Glassdoor / Open Postings (Tech, Finance, Healthcare, Consulting).
        </div>
        """, unsafe_allow_html=True)

    with c24:
        st.markdown(f"#### 2.4 โครงสร้างเงินเดือนในแต่ละระดับการทำงาน (Salary by Career Level in {sal_prefix})")
        fig2_4 = px.box(
            filtered_demand,
            x="experience_level",
            y=sal_col,
            color="field",
            category_orders={"experience_level": ["Entry-Level", "Mid-Level", "Senior", "Executive"]},
            labels={sal_col: f"อัตราเงินเดือน ({sal_prefix})", "experience_level": "ระดับการทำงาน", "field": "สายงาน"},
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
            Data Reference: Kaggle Data Science Job Salaries (CC0 Public Domain) และ U.S. BLS OEWS May Benchmark Statistics.
        </div>
        """, unsafe_allow_html=True)

    with st.expander("ดูตารางข้อมูลประกาศรับสมัครงานจริง (Open Job Postings Ledger)"):
        demand_cols = ["job_id", "company_name", "industry", "field", "job_title", "experience_level", "vacancies", sal_col, "location", "posting_date", "data_source"]
        st.dataframe(filtered_demand[demand_cols].sort_values(by="posting_date", ascending=False), use_container_width=True)


# =========================================================
# TAB 3: วิเคราะห์ Skills Mismatch จาก Tab 1 และ Tab 2
# =========================================================
with tab3:
    st.markdown("### Tab 3: การวิเคราะห์ Skills Mismatch (Supply vs. Demand Equilibrium)")
    st.caption("เปรียบเทียบข้อมูลระหว่าง Tab 1 (อุปทาน/สิ่งที่หลักสูตรสอน) และ Tab 2 (อุปสงค์/สิ่งที่ตลาดต้องการ) เพื่อวิเคราะห์ช่องว่างทักษะและดุลยภาพกำลังคน")

    # Tab 3 Cross-Filter by Field
    t3_c1, t3_c2 = st.columns([2, 1])
    with t3_c1:
        t3_field = st.selectbox(
            "เลือกสายงานที่ต้องการวิเคราะห์ Mismatch เฉพาะด้าน:",
            options=["ทุกสายงาน (All Fields)", "AI", "Data Science", "Statistics"],
            key="t3_field"
        )
    with t3_c2:
        st.write("")
        st.write("")
        if st.button("Reset Tab 3 Filter", key="t3_reset"):
            st.session_state["t3_field"] = "ทุกสายงาน (All Fields)"
            st.rerun()

    # Re-calculate Mismatch metrics based on selected scope
    target_supply = raw_supply_df if t3_field == "ทุกสายงาน (All Fields)" else raw_supply_df[raw_supply_df["field"] == t3_field]
    target_demand = raw_demand_df if t3_field == "ทุกสายงาน (All Fields)" else raw_demand_df[raw_demand_df["field"] == t3_field]
    
    active_mismatch = calculate_mismatch_metrics(target_supply, target_demand)
    mismatch_df = active_mismatch["mismatch_df"]
    heatmap_df = active_mismatch["heatmap_df"]
    volume_df = active_mismatch["volume_df"]
    rec_df = active_mismatch["recommendations_df"]

    # Chart 3.1 & Chart 3.2
    c31, c32 = st.columns(2)
    with c31:
        st.markdown("#### 3.1 Heatmap ช่องว่างทักษะ (รายวิชาในหลักสูตร vs. ทักษะที่ตลาดต้องการ)")
        fig3_1 = px.imshow(
            heatmap_df,
            labels=dict(x="ทักษะที่ตลาดงานต้องการ (Market Demand)", y="รายวิชาบังคับในหลักสูตร (Curriculum Core)", color="ความสอดคล้อง (%)"),
            x=heatmap_df.columns,
            y=heatmap_df.index,
            color_continuous_scale="Viridis",
            text_auto=True,
            template="plotly_dark"
        )
        fig3_1.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            coloraxis_colorbar=dict(title="ความสอดคล้อง %")
        )
        st.plotly_chart(fig3_1, use_container_width=True)
        st.markdown("""
        <div class="data-reference-caption">
            Data Reference: การคำนวณ Co-occurrence Matrix ระหว่างรายวิชาบังคับของ อว. กับความต้องการในประกาศงานจริงของ Kaggle.
        </div>
        """, unsafe_allow_html=True)

    with c32:
        st.markdown("#### 3.2 กราฟจำแนกทักษะส่วนเกิน vs. ขาดแคลน (Skill Surplus vs. Shortage Divergence)")
        st.caption("ด้านขวา (+) = Shortage (ตลาดต้องการสูง แต่หลักสูตรเปิดสอนน้อย) | ด้านซ้าย (-) = Surplus (หลักสูตรสอนเยอะ แต่ตลาดระบุความต้องการน้อย)")
        
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
            labels={"gap_divergence": "ค่าความแตกต่าง (ความต้องการตลาด % - การสอนในหลักสูตร %)", "skill": "ทักษะ"},
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
            Data Reference: ผลต่างสัดส่วนร้อยละ (Divergence Delta) ระหว่างสัดส่วนการสอนจริงในหลักสูตร กับความต้องการในตลาดแรงงาน.
        </div>
        """, unsafe_allow_html=True)

    # Chart 3.3 & Diagnostic Recommendations
    c33, c34 = st.columns([1, 1.2])
    with c33:
        st.markdown("#### 3.3 ดุลยภาพจำนวนคนที่จบต่อปี VS ปริมาณตำแหน่งงานว่าง (Talent Volume Gap)")
        volume_melted = pd.melt(
            volume_df,
            id_vars=["field"],
            value_vars=["annual_graduates", "job_vacancies"],
            var_name="Category",
            value_name="จำนวนคน/อัตรา"
        )
        volume_melted["Category"] = volume_melted["Category"].map({
            "annual_graduates": "จำนวนบัณฑิตที่จบต่อปี (Supply)",
            "job_vacancies": "ปริมาณตำแหน่งงานว่างแรกเข้า (Demand)"
        })
        fig3_3 = px.bar(
            volume_melted,
            x="field",
            y="จำนวนคน/อัตรา",
            color="Category",
            barmode="group",
            labels={"จำนวนคน/อัตรา": "จำนวนคน / ตำแหน่งงาน (อัตรา)", "field": "สาขาวิชา", "Category": "กลุ่มข้อมูล"},
            color_discrete_map={"จำนวนบัณฑิตที่จบต่อปี (Supply)": "#3B82F6", "ปริมาณตำแหน่งงานว่างแรกเข้า (Demand)": "#EC4899"},
            template="plotly_dark"
        )
        fig3_3.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig3_3, use_container_width=True)
        st.markdown("""
        <div class="data-reference-caption">
            Data Reference: ยอดบัณฑิตจบใหม่ประจำปี (อว.) เทียบกับตำแหน่งงานว่างจริงในระบบ (Kaggle & ILOSTAT Indicators).
        </div>
        """, unsafe_allow_html=True)

    with c34:
        st.markdown("#### 3.4 ตารางวินิจฉัยและข้อเสนอแนะเชิงนโยบายเพื่อลด Mismatch (Policy Recommendations)")
        for _, rec in rec_df.iterrows():
            badge_class = "badge-urgent" if "Urgent" in rec["priority"] else ("badge-moderate" if "Moderate" in rec["priority"] else "badge-positive")
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 12px 16px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-weight: 700; color: #F1F5F9; font-size: 0.95rem;">{rec['target_field']}</span>
                    <span class="{badge_class}">{rec['priority']}</span>
                </div>
                <div style="color: #CBD5E1; font-size: 0.88rem; margin-bottom: 6px;">
                    <strong>ช่องว่างทักษะที่พบ:</strong> {rec['skill_gap']}
                </div>
                <div style="color: #94A3B8; font-size: 0.85rem; line-height: 1.4;">
                    <strong>ข้อเสนอแนะเชิงนโยบาย:</strong> {rec['policy_action']}
                </div>
                <div style="color: #38BDF8; font-size: 0.82rem; font-weight: 600; margin-top: 4px;">
                    เป้าหมายการลด Mismatch: {rec['impact_reduction']}
                </div>
                <div style="color: #64748B; font-size: 0.75rem; margin-top: 2px;">
                    แหล่งข้อมูลอ้างอิง: {rec['benchmark_source']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("""
        <div class="data-reference-caption">
            Data Reference: ข้อเสนอแนะเชิงนโยบายคำนวณจากค่าดัชนี Skill Mismatch และมาตรฐานสมรรถนะอาชีพ U.S. BLS / ILOSTAT.
        </div>
        """, unsafe_allow_html=True)

    with st.expander("ดูตารางสรุปค่า Mismatch รายทักษะทั้งหมด (Quantitative Mismatch Ledger)"):
        st.dataframe(mismatch_df, use_container_width=True)

# ---------------------------------------------------------
# Footer (No Emojis)
# ---------------------------------------------------------
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 30px 0 10px 0;">
    AI, Data Science & Statistics Supply-Demand Analytics Platform | Engineered with Streamlit & Plotly | Real Open Data Grounded
</div>
""", unsafe_allow_html=True)
