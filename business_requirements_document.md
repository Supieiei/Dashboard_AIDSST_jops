# Business Requirements Document (BRD)

## Project Title
**AI, Data Science & Statistics Talent Supply & Demand Dashboard**

---

## 1. Executive Summary & Objective
โครงการนี้มีวัตถุประสงค์เพื่อพัฒนา Interactive Analytical Dashboard โดยใช้ **Python** และ **Plotly** สำหรับวิเคราะห์ดุลยภาพระหว่าง **อุปทาน (Graduates Supply)** และ **อุปสงค์ (Market Job Demand)** ในสายงาน Artificial Intelligence (AI), Data Science (DS) และ Statistics (Stat) 

ระบบจะต้องเปรียบเทียบทักษะที่สถาบันการศึกษาผลิตเข้าสู่ตลาดแรงงาน กับทักษะที่ภาคอุตสาหกรรมต้องการจริง เพื่อนำไปสู่การวิเคราะห์ **Skill Mismatch** สำหรับใช้วางแผนยุทธศาสตร์การผลิตกำลังคนและการพัฒนาหลักสูตร

---

## 2. Technical Stack & Architectural Constraints
1. **Backend & Framework:** Python 3.10+ (ใช้ **Dash by Plotly** หรือ **Streamlit** พร้อม Plotly Express/Objects)
2. **Data Visualization:** Plotly Library (Interactive Charts, Cross-filtering, Hover Tooltips)
3. **Interactivity Requirements (Cross-Filtering):**
   * กราฟและฟิลเตอร์ทุกตัวภายใน Tab เดียวกันต้องมี **Cross-filtering State Synchronization** (เมื่อคลิกเลือกจุดข้อมูล/แท่งกราฟ หรือเปลี่ยน Dropdown ในกราฟหนึ่ง กราฟอื่นใน Tab เดียวกันต้องอัปเดต Filter ตามทันที)
4. **Data Management:** Pandas DataFrame / DuckDB (ฝัง Mock/Processed Open Data Set ภายในโครงสร้างโครงการ)
5. **Deployment Target:** Single-file หรือ Clean Python Project Structure ที่สามารถรันผ่าน Agent/Container ได้ทันที

---

## 3. Functional Requirements & Dashboard Architecture

Dashboard แบ่งออกเป็น **3 Tabs หลัก** ดังรายละเอียดต่อไปนี้:

```
[ Dashboard Main View ]
 │
 ├── 🎓 Tab 1: Graduate Supply & Curriculum Skills
 ├── 💼 Tab 2: Labor Market Demand & Industry Requirements
 └── ⚖️ Tab 3: Skill Mismatch Analysis (Supply vs. Demand)
```

---

### 🎓 Tab 1: ปริมาณคนที่จบ และ Skills ที่เรียนมา (Graduate Supply & Education)

#### **Goal:** 
วิเคราะห์ศักยภาพการผลิตกำลังคนของสถาบันการศึกษา คุณภาพหลักสูตร ทักษะบังคับ และอัตราการได้งานทำของบัณฑิตจบใหม่

#### **Component Breakdown & Visualizations:**

1. **Global Filters (Header Bar):**
   * `Field Filter`: [All, AI, Data Science, Statistics]
   * `Degree Level`: [Bachelor's, Master's, Doctorate]
   * `Year Range`: [2020 - 2025]

2. **Graph 1.1: Production Capacity by Program & Year (Bar/Line Combo Chart)**
   * **x-axis:** ปีการศึกษา (Year)
   * **y-axis:** จำนวนบัณฑิตที่จบการศึกษา (Graduates Count)
   * **Color/Legend:** ชื่อหลักสูตร/มหาวิทยาลัย (Program/University Name)
   * **Interactive Action:** คลิกที่แท่ง/เส้นเพื่อเลือกหลักสูตรเฉพาะ ส่งผลกระทบต่อ Graph 1.2, 1.3, 1.4

3. **Graph 1.2: Core Required Skills in Curriculum (Horizontal Stacked Bar / Sunburst Chart)**
   * **Content:** รายวิชาบังคับในหลักสูตรที่ตรงกับทักษะสายงาน (เช่น Core Math, Machine Learning, Python/R, Data Modeling, MLOps, SQL)
   * **x-axis:** สัดส่วน/จำนวนหลักสูตรที่เปิดบรรจุเป็นวิชาบังคับ (%)
   * **Interactive Action:** คลิกเลือกทักษะวิชาบังคับเพื่อ Filter บัณฑิตและหลักสูตรที่เกี่ยวข้อง

4. **Graph 1.3: Post-Graduation Employment Rate (Grouped Bar Chart)**
   * **x-axis:** ช่วงเวลาหลังจบ (`Year 1`, `Year 2`, `Year 3`)
   * **y-axis:** จำนวน / เปอร์เซ็นต์บัณฑิตที่ได้งานตรงสาย (Employed Graduates)
   * **Breakdown:** จำแนกตามสาขา (AI vs DS vs Stat)

5. **Graph 1.4: Tuition Fee vs. Employment Success Scatter Plot (Scatter Plot)**
   * **x-axis:** ค่าเทอมตลอดหลักสูตร (Total Tuition Fee - THB/USD)
   * **y-axis:** อัตราการได้งานทำปีแรก (%)
   * **Size:** จำนวนบัณฑิตที่จบต่อปี
   * **Color:** สาขาวิชา

---

### 💼 Tab 2: ปริมาณงานที่จ้าง และ Skills ที่ต้องการ (Market Job Demand)

#### **Goal:** 
วิเคราะห์ความต้องการในตลาดแรงงาน ตำแหน่งงานว่าง บริษัทที่เปิดรับ และโครงสร้างค่าตอบแทนในแต่ละระดับประสบการณ์

#### **Component Breakdown & Visualizations:**

1. **Global Filters (Header Bar):**
   * `Industry Sector`: [Tech, Finance & Banking, Healthcare, Retail, Manufacturing, Consulting]
   * `Experience Level`: [Entry-Level (0-2 yrs), Mid-Level (3-5 yrs), Senior/Lead (5+ yrs)]
   * `Location/Region`: [Local/Thailand, Global/Remote]

2. **Graph 2.1: Open Job Vacancies Trend (Area / Line Chart)**
   * **x-axis:** เดือน/ปี (Timeline)
   * **y-axis:** จำนวนตำแหน่งงานที่เปิดรับสมัคร (Open Vacancies Count)
   * **Breakdown:** AI Engineer, Data Scientist, Statistician, Data Engineer

3. **Graph 2.2: Top In-Demand Technical & Soft Skills (Word Cloud / Sorted Bar Chart)**
   * **Content:** รายชื่อ ทักษะที่ถูกระบุไว้ในประกาศรับสมัครงาน (Job Descriptions) เช่น Python, SQL, PyTorch, Cloud (AWS/GCP), LLMs, Communication
   * **x-axis:** จำนวนครั้งที่ถูกระบุในใบสมัคร (Skill Frequency Count)
   * **Interactive Action:** คลิกที่ทักษะเพื่อ Filter บริษัทที่ต้องการทักษะนั้นๆ และระดับเงินเดือน

4. **Graph 2.3: Top Hiring Companies & Market Share (Horizontal Bar Chart)**
   * **y-axis:** ชื่อบริษัท/กลุ่มอุตสาหกรรม (Company Name / Sector)
   * **x-axis:** จำนวนประกาศรับสมัคร (Active Job Postings)
   * **Interactive Action:** คลิกชื่อบริษัทเพื่อแสดงทักษะเฉพาะที่บริษัทนั้นเปิดรับ

5. **Graph 2.4: Salary Distribution by Career Level (Box Plot / Violin Plot)**
   * **x-axis:** ระดับการทำงาน (`Entry-Level`, `Mid-Level`, `Senior`, `Executive`)
   * **y-axis:** ช่วงเงินเดือน (Starting Salary Range - USD/THB)
   * **Color:** สายงาน (AI vs Data Science vs Statistics)

---

### ⚖️ Tab 3: วิเคราะห์ Skill Mismatch (Supply vs. Demand Analysis)

#### **Goal:** 
เปรียบเทียบข้อมูลจาก Tab 1 (อุปทาน/สิ่งที่สอน) และ Tab 2 (อุปสงค์/สิ่งที่ตลาดต้องการ) เพื่อค้นหาช่องว่างทางทักษะ (Skill Gap) และส่วนเกิน/ขาดแคลนของกำลังคน

#### **Component Breakdown & Visualizations:**

1. **Graph 3.1: Skill Gap Heatmap (Supply vs. Demand Matrix)**
   * **x-axis:** Skills ที่ตลาดต้องการ (from Tab 2)
   * **y-axis:** Skills วิชาบังคับในหลักสูตร (from Tab 1)
   * **Color Density:** ความสอดคล้อง (Match Index Rate 0-100%)
   * **Insight Highlight:** ระบุทักษะที่มีความต้องการสูงในตลาด แต่หลักสูตรยังไม่สอนเป็นวิชาบังคับ (Over-demanded / Under-taught Skills) เช่น MLOps, LLM Fine-Tuning, GenAI

2. **Graph 3.2: Skill Surplus vs. Shortage Bar Chart (Diverging Bar Chart)**
   * **y-axis:** รายชื่อทักษะ (Skills)
   * **x-axis Left (-):** Skill Surplus (สอนเยอะ ตลาดต้องการน้อย)
   * **x-axis Right (+):** Skill Shortage (ตลาดต้องการเยอะ สอนน้อย)

3. **Graph 3.3: Talent Volume vs. Job Vacancies Gap (Grouped Bar / Butterfly Chart)**
   * **x-axis:** สาขาวิชา (AI, Data Science, Statistics)
   * **y-axis:** จำนวนบัณฑิตจบใหม่ต่อปี VS จำนวนตำแหน่งงานว่างปีแรก

4. **Interactive Mismatch Diagnostic Table (DataTable)**
   * แสดงตารางสรุปข้อเสนอแนะเชิงนโยบาย (Recommendations) เช่น "หลักสูตร Data Science ควรเพิ่มรายวิชา MLOps และ Cloud Deployment เพื่อลด Mismatch 35%"

---

## 4. Cross-Filtering & State Management Requirements

เพื่อให้สอดคล้องกับข้อกำหนดข้อ 3 **ทุกกราฟใน Tab เดียวกันต้องเชื่อมโยงกัน (Cross-filtering)**:

1. **Callback Architecture (Plotly Dash / Streamlit):**
   * กำหนด `selectedData` หรือ `clickData` event handler ให้กับทุกรูปกราฟ
   * เมื่อ User คลิกที่หมวดหมู่ใดก็ตาม (เช่น คลิกสาขา "Statistics" ใน Graph 1.1):
     * State ของ Dashboard จะถูกอัปเดตเป็น `filtered_df = df[df['field'] == 'Statistics']`
     * Graph 1.2 (Skills), Graph 1.3 (Employment Rate), และ Graph 1.4 (Tuition) ต้อง **Re-render** ทันทีโดยใช้ข้อมูลที่ถูก Filter แล้ว
2. **Reset Filter Button:**
   * มีปุ่ม `Clear All Filters` ในทุก Tab เพื่อรีเซ็ตมุมมองกลับสู่ค่าเริ่มต้น

---

## 5. Sample Data Structure Schema (for Python Backend Integration)

```python
# Sample Pandas DataFrame Schema Structure for Antigravity Implementation

# Tab 1: Supply Data (Graduates & Curriculum)
graduates_df = pd.DataFrame([
    {
        "program_id": "P001",
        "program_name": "B.Sc. Data Science & AI",
        "field": "Data Science",
        "degree": "Bachelor's",
        "year": 2024,
        "graduates_count": 120,
        "tuition_fee_thb": 240000,
        "core_skills": ["Python", "SQL", "Machine Learning", "Statistics"],
        "employed_yr1": 105,
        "employed_yr2": 112,
        "employed_yr3": 118
    }
])

# Tab 2: Demand Data (Job Market & Requirements)
jobs_df = pd.DataFrame([
    {
        "job_id": "J001",
        "company_name": "Tech Corp",
        "industry": "Tech",
        "field": "AI",
        "job_title": "AI Engineer",
        "experience_level": "Entry-Level",
        "vacancies": 5,
        "required_skills": ["Python", "PyTorch", "Docker", "MLOps"],
        "min_salary": 45000,
        "max_salary": 70000,
        "posting_date": "2024-05-15"
    }
])
```

---

## 6. Acceptance Criteria for Antigravity Agent

1. **Functional Completeness:** มีแท็บเมนูแยก 3 Tabs ชัดเจน ตรงตามข้อกำหนดของ BRD
2. **Python Native:** พัฒนาด้วย Python 100% โดยใช้ **Plotly** ร่วมกับ **Dash** หรือ **Streamlit**
3. **Cross-Filtering:** คลิกองค์ประกอบในกราฟใดๆ แล้วกราฟอื่นๆ ใน Tab เดียวกันต้องปรับเปลี่ยนข้อมูลตามทันที
4. **Data Coverage:** แสดงผลข้อมูลครอบคลุมหลักสูตร, จำนวนจบ, วิชาบังคับ, บัณฑิตได้งาน, ค่าเทอม, ตำแหน่งว่าง, ทักษะที่ต้องการ, บริษัท, เงินเดือน และการวิเคราะห์ Mismatch
5. **UI/UX:** ออกแบบในสไตล์ Modern Executive Dashboard รองรับ Dark/Light Mode อ่านง่าย และมี Tooltip อธิบายชัดเจน

---

## 🤖 Direct Prompt for Antigravity Developer Agent

> **Instruction for Antigravity:**  
> "Please read the attached `brd_ai_ds_stat_dashboard.md` specifications carefully. Build a complete, production-ready interactive Python Dashboard using **Plotly** and **Streamlit** (or **Plotly Dash**). Implement all 3 main tabs (`Tab 1: Supply & Curriculum`, `Tab 2: Market Demand`, `Tab 3: Skill Mismatch Analysis`) complete with cross-filtering interactions, dynamic charts, embedded mock datasets based on open data, and clean responsive UI styling."