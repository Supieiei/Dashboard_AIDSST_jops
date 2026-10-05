# AI, Data Science & Statistics Talent Supply & Demand Dashboard

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75.svg)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An interactive analytical dashboard designed to evaluate the equilibrium between Higher Education Graduate Supply and Industry Job Demand across Artificial Intelligence (AI), Data Science (DS), and Statistics (Stat). The platform quantitatively diagnoses Skill Mismatch to guide academic curriculum planning, policy interventions, and workforce development strategies.

---

## Project Objectives & Problem Statement

As AI, Data Science, and Machine Learning rapidly transform the global economy, significant discrepancies emerge between university curricula and labor market expectations:
1. Curriculum Lag: Traditional academic curricula often focus on foundational theory while industry demand surges for applied tools, MLOps, LLM fine-tuning, and cloud-native architecture.
2. Talent Volume vs. Job Openings: Imbalances between annual graduate production rates and first-year industry openings.
3. Information Asymmetry: Students and educational administrators lack granular, cross-filtered visibility into how academic skill sets directly translate into employment rates and starting compensation.

This dashboard provides executive-level, interactive visibility across three core analytical pillars to bridge this gap.

---

## Verified Open Data Sources & Integration

The analytical models and embedded datasets synthesize open labor and educational data benchmarks:

| Source | Scope | Key Features & Metrics | Citation / Portal |
| :--- | :--- | :--- | :--- |
| **AI Job Market Global** | Global Postings | `job_title`, `salary`, `company_location`, `experience_level`, 24+ tracked technical skills (Python, PyTorch, LangChain, etc.) | [Kaggle Dataset (CC BY 4.0)](https://www.kaggle.com/datasets/atharvasoundankar/ai-job-market-global-2026) |
| **Global Data Science Salaries** | Global Multi-year | `work_year`, `experience_level`, `salary_in_usd`, `employment_type`, `company_size` | [Kaggle Dataset (CC0)](https://www.kaggle.com/datasets/ruchi798/data-science-job-salaries) |
| **U.S. BLS OEWS** | Official US Labor Statistics | `tot_emp` (Total Employment), percentiles (`pct_10`, `pct_25`, `pct_median`, `pct_75`, `pct_90`) for Data Scientists & Statisticians | [U.S. Bureau of Labor Statistics](https://www.bls.gov/oes/) |
| **ILOSTAT Labor Statistics** | Global Cross-sector | Employment-to-population ratios, sectoral profiles, and macroeconomic labor trends | [ILOSTAT Data Portal](https://ilostat.ilo.org/data/) |
| **University Curriculum Data** | Higher Education | Program capacity, core compulsory courses, tuition fees, and 1-3 year longitudinal employment rates | Processed Higher Education Open Benchmarks |

---

## System Architecture & Dashboard Features

The dashboard is structured into an Executive KPI Summary and Three Analytical Tabs, featuring real-time Cross-Filtering State Synchronization:

```
[ Dashboard Main View ]
 │
 ├── Executive KPI Summary (Global Salary, Active Openings, Annual Graduates, Top Skills, Match Index)
 ├── Tab 1: Graduate Supply & Curriculum Skills
 ├── Tab 2: Labor Market Demand & Industry Requirements
 └── Tab 3: Skill Mismatch Analysis (Supply vs. Demand)
```

### 1. Executive KPI Summary Cards
* Global Median / Average Salary (USD / THB equivalent): Comprehensive baseline compensation.
* Total Active Job Openings: Live vacancy volume across all tracked domains.
* Annual Graduate Supply: Total annual student output from relevant academic programs.
* Top 3 Most In-Demand Skills: High-frequency industry requirements (e.g., Python, SQL, Cloud / PyTorch).
* Overall Skill Alignment Index: Aggregate compatibility score between curricula and market needs.

---

### 2. Tab 1: Graduate Supply & Curriculum Skills
* Graph 1.1: Production Capacity by Program & Year (Bar/Line Combo)
  * Tracks graduate output over time (2020-2025) categorized by field (`AI`, `Data Science`, `Statistics`) and degree level (`Bachelor's`, `Master's`, `Doctorate`).
* Graph 1.2: Core Required Skills in Curriculum (Horizontal Stacked Bar / Sunburst)
  * Quantifies the proportion of academic programs that mandate key technical disciplines (Machine Learning, Core Math, Cloud, MLOps, SQL, Data Modeling).
* Graph 1.3: Post-Graduation Employment Rate (Grouped Bar Chart)
  * Longitudinal career placement tracking across `Year 1`, `Year 2`, and `Year 3` after graduation.
* Graph 1.4: Tuition Fee vs. Employment Success (Interactive Scatter Plot)
  * Correlates total program tuition costs against 1st-year employment rates, sized by graduating class volume.
* Filters: Field filter, Degree Level, Year Range, and Clear Filter reset.

---

### 3. Tab 2: Labor Market Demand & Industry Requirements
* Graph 2.1: Open Job Vacancies Trend (Area / Line Chart)
  * Temporal hiring dynamics across key job profiles: AI Engineer, Data Scientist, Statistician, and Data Engineer.
* Graph 2.2: Top In-Demand Technical & Soft Skills (Sorted Frequency Bar Chart)
  * Frequency metrics extracted from job specifications (Python, PyTorch, SQL, Cloud Platforms, LLMs, Docker, Communication).
* Graph 2.3: Top Hiring Companies & Market Share (Horizontal Bar Chart)
  * Active hiring volume by leading employers and industry sectors (Tech, Finance & Banking, Healthcare, Retail, Consulting).
* Graph 2.4: Salary Distribution by Career Level (Box / Violin Plot)
  * Detailed compensation breakdown across `Entry-Level`, `Mid-Level`, `Senior`, and `Executive` tiers and company sizes (`Small`, `Medium`, `Large`).
* Filters: Industry Sector, Experience Level, Regional Location, and Clear Filter reset.

---

### 4. Tab 3: Skill Mismatch Analysis (Supply vs. Demand)
* Graph 3.1: Skill Gap Heatmap (Supply vs. Demand Matrix)
  * Bi-directional matrix mapping skills taught in academic curricula against skills requested in industry job descriptions. Highlighted zones pinpoint Over-demanded / Under-taught skills (e.g., MLOps, LLM Engineering, Cloud Deployment).
* Graph 3.2: Skill Surplus vs. Shortage Diverging Bar Chart
  * Diverging analysis showing surplus skills (taught intensely but lower market demand) vs. shortage skills (high industry demand with low curriculum coverage).
* Graph 3.3: Talent Volume vs. Job Vacancies Gap (Butterfly / Grouped Bar Chart)
  * Side-by-side volume comparison between annual graduates and first-year job vacancies per discipline.
* Diagnostic Table & Policy Recommendations:
  * Actionable curriculum adjustments and policy directives with estimated mismatch reduction percentages.

---

## Interactivity & Cross-Filtering Architecture

* State Synchronization: Integrated state management (`st.session_state`) updates downstream charts and tables dynamically when selections or filter controls are toggled.
* Reset Capabilities: Every tab contains a dedicated Clear All Filters button to restore global perspectives.
* Responsive Layout: Adaptive styling optimized for both widescreen executive boardroom displays and mobile/tablet inspection.

---

## Technology Stack

* Language: Python 3.10+
* Application Framework: Streamlit
* Interactive Charting: Plotly Express & Plotly Graph Objects
* Data Processing: Pandas & NumPy
* Styling: Custom CSS theme with executive dark/light support

---

## Quickstart & Installation

### Prerequisites
- Python 3.10 or higher
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/Supieiei/Dashboard_AIDSST_jops.git
cd Dashboard_AIDSST_jops
```

### 2. Set Up Virtual Environment (Recommended)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Dashboard
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.

---

## Repository Structure

```
Dashboard_AIDSST_jops/
├── .streamlit/
│   └── config.toml               # Streamlit UI theme and server configuration
├── data/
│   ├── __init__.py
│   └── data_engine.py            # Data loading, open data synthesis, & mismatch engine
├── tests/
│   └── test_data_and_charts.py   # Automated data validation and chart smoke tests
├── app.py                        # Main Streamlit dashboard application
├── business_requirements_document.md # Original Business Requirements Document (BRD)
├── antigravity_dashboard_handoff.md  # Agent handoff protocol & data specs
├── PROJECT_STATUS.md             # Implementation milestone & progress tracker
├── requirements.txt              # Python package dependencies
└── README.md                     # Project documentation & user guide
```

---

## License
This project is open-source under the [MIT License](LICENSE).
Open datasets utilized remain subject to their respective licenses (CC BY 4.0, CC0 Public Domain, and US Government Open Data).
