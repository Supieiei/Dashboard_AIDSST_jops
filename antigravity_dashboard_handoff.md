# AI Agent Handoff Protocol: Dashboard Generation

**Target Agent:** Antigravity (Data Visualization & Dashboard Generation Agent)
**Project:** AI, Data Science, and Statistics Job Market Dashboard

## 🛠️ 

$$
SYSTEM_INSTRUCTION
$$

You are an expert Frontend Developer and Data Visualization Engineer. Your primary task is to consume the provided open-source job market datasets and generate an interactive, responsive dashboard. You must handle data aggregation, filtering, and rendering beautiful UI components.

## 📊 

$$
VERIFIED OPEN DATA SOURCES
$$

Please ingest the following Open Data sources for the dashboard:

1. **AI Job Market Global (Kaggle - CC BY 4.0 Open Data):**

   * `Description:` Real-time and snapshot global job postings tracking salary, experience levels, and required skills.

   * `URL/Reference:` [Kaggle - AI Job Market Global](https://www.kaggle.com/datasets/atharvasoundankar/ai-job-market-global-2026)

   * `Features:` `job_title`, `salary`, `company_location`, `experience_level`, `required_skills` (24 tracked tech skills including Python, PyTorch, LangChain, etc.)

2. **Global Data Science Salaries (Kaggle - CC0 Public Domain):**

   * `Description:` Historical compensation and labor trends across multiple countries.

   * `URL/Reference:` [Kaggle - Data Science Job Salaries](https://www.kaggle.com/datasets/ruchi798/data-science-job-salaries)

   * `Features:` `work_year`, `experience_level`, `salary_in_usd`, `employment_type`, `company_size`

3. **U.S. BLS Occupational Employment and Wage Statistics (U.S. Government Open Data):**

   * `Description:` Official employment volume, median salary, and percentile distributions for Statisticians and Data Scientists.

   * `URL/Reference:` [U.S. BLS - Data Scientists & Statisticians OEWS](https://www.bls.gov/oes/)

   * `Features:` `tot_emp` (Total Employment), `pct_10`, `pct_25`, `pct_median`, `pct_75`, `pct_90`

4. **ILOSTAT - International Labour Organization (Global Open Labor Data):**

   * `Description:` Global labor market statistics, employment-to-population ratios, and sector profiles.

   * `URL/Reference:` [ILOSTAT Data Portal](https://ilostat.ilo.org/data/)

   * `Features:` Global employment trends by sector and economic indicators.

## 🎯 

$$
DASHBOARD_REQUIREMENTS
$$

The dashboard must include the following interactive sections:

### 1. Executive Summary (KPI Cards)

* Average / Median Salary (USD) globally.

* Total Job Openings / Employment Volume.

* Top 3 Most In-Demand Skills.

### 2. Salary Analysis (Charts)

* **Bar Chart:** Median Salary by Experience Level (`Entry`, `Mid`, `Senior`, `Executive`).

* **Distribution Chart:** Salary breakdown across different company sizes and regions.

### 3. Skills & Education (Interactive)

* **Skill Frequency Bar / Radar Chart:** Frequency of required technical skills (Python, SQL, R, PyTorch, Cloud platforms, etc.).

* **Education Requirement Breakdown:** Proportion of Bachelor's, Master's, and Ph.D. prerequisites.

### 4. Filters & Controls

* Dropdown to filter by **Experience Level**.

* Dropdown to filter by **Job Role / Title** (e.g., Data Scientist, ML Engineer, Statistician).

* Country / Region selector.

## 📦 

$$
DELIVERABLES
$$

* **Single-file Application:** Combine HTML, Tailwind CSS, and JavaScript into a single functional `.html` file (or a single Python Streamlit app file if applicable).

* **Mock Data Fallback:** Include an embedded sample JSON dataset based on the schemas above to ensure the dashboard renders successfully even if live fetch fails.

$$
END OF HANDOFF
$$