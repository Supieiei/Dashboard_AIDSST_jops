"""
Unit and smoke tests for AI, Data Science & Statistics Dashboard.
Verifies data generation schema integrity, mismatch calculations, and Plotly chart generation.
"""

import unittest
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.data_engine import (
    generate_supply_dataset,
    generate_demand_dataset,
    calculate_mismatch_metrics,
    SKILLS_TAXONOMY
)


class TestDashboardDataAndCharts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.supply_df = generate_supply_dataset()
        cls.demand_df = generate_demand_dataset()
        cls.mismatch_data = calculate_mismatch_metrics(cls.supply_df, cls.demand_df)

    def test_supply_schema_and_values(self):
        df = self.supply_df
        required_cols = [
            "program_id", "program_name", "university", "field", "degree",
            "year", "graduates_count", "tuition_fee_thb", "tuition_fee_usd",
            "core_skills", "employed_yr1", "employed_yr2", "employed_yr3",
            "employment_rate_yr1", "employment_rate_yr2", "employment_rate_yr3"
        ]
        for col in required_cols:
            self.assertIn(col, df.columns, f"Missing supply column: {col}")

        self.assertGreater(len(df), 400)
        self.assertEqual(set(df["field"].unique()), {"AI", "Data Science", "Statistics"})
        self.assertEqual(set(df["degree"].unique()), {"Bachelor's", "Master's", "Doctorate"})
        self.assertEqual(set(df["year"].unique()), {2020, 2021, 2022, 2023, 2024, 2025})
        self.assertTrue((df["employment_rate_yr1"] <= 100).all())
        self.assertTrue((df["employment_rate_yr1"] >= 0).all())

    def test_demand_schema_and_values(self):
        df = self.demand_df
        required_cols = [
            "job_id", "company_name", "industry", "field", "job_title",
            "experience_level", "company_size", "location", "vacancies",
            "required_skills", "min_salary_usd", "max_salary_usd", "avg_salary_usd",
            "avg_salary_thb", "posting_date"
        ]
        for col in required_cols:
            self.assertIn(col, df.columns, f"Missing demand column: {col}")

        self.assertGreater(len(df), 500)
        self.assertEqual(set(df["field"].unique()), {"AI", "Data Science", "Statistics"})
        self.assertIn("Entry-Level", df["experience_level"].unique())
        self.assertIn("Senior", df["experience_level"].unique())
        self.assertTrue((df["vacancies"] >= 1).all())
        self.assertTrue((df["avg_salary_usd"] > 0).all())

    def test_mismatch_metrics_calculation(self):
        m = self.mismatch_data
        self.assertIn("mismatch_df", m)
        self.assertIn("heatmap_df", m)
        self.assertIn("volume_df", m)
        self.assertIn("recommendations_df", m)
        self.assertIn("overall_match_index", m)

        mismatch_df = m["mismatch_df"]
        self.assertIn("gap_divergence", mismatch_df.columns)
        self.assertIn("curriculum_supply_pct", mismatch_df.columns)
        self.assertIn("market_demand_pct", mismatch_df.columns)

        # Overall match index should be realistic percentage
        self.assertGreaterEqual(m["overall_match_index"], 50)
        self.assertLessEqual(m["overall_match_index"], 100)

        # Volume balance
        volume_df = m["volume_df"]
        self.assertEqual(len(volume_df), 3)
        self.assertTrue((volume_df["annual_graduates"] > 0).all())
        self.assertTrue((volume_df["job_vacancies"] > 0).all())

    def test_plotly_charts_smoke_test(self):
        # 1.1 Bar chart
        grad_trend = self.supply_df.groupby(["year", "field"])["graduates_count"].sum().reset_index()
        fig1_1 = px.bar(grad_trend, x="year", y="graduates_count", color="field")
        self.assertIsNotNone(fig1_1)

        # 1.2 Skills bar
        skills_supply = self.supply_df.explode("core_skills")
        counts = skills_supply["core_skills"].value_counts().reset_index()
        fig1_2 = px.bar(counts.head(10), x="count", y="core_skills", orientation="h")
        self.assertIsNotNone(fig1_2)

        # 1.3 Employment bar
        emp_rates = self.supply_df.groupby("field")[["employment_rate_yr1", "employment_rate_yr2"]].mean().reset_index()
        emp_melted = pd.melt(emp_rates, id_vars=["field"], value_vars=["employment_rate_yr1", "employment_rate_yr2"])
        fig1_3 = px.bar(emp_melted, x="variable", y="value", color="field", barmode="group")
        self.assertIsNotNone(fig1_3)

        # 1.4 Scatter plot
        fig1_4 = px.scatter(self.supply_df, x="tuition_fee_usd", y="employment_rate_yr1", size="graduates_count", color="field")
        self.assertIsNotNone(fig1_4)

        # 2.1 Area chart
        vac_trend = self.demand_df.groupby(["posting_year_month", "field"])["vacancies"].sum().reset_index()
        fig2_1 = px.area(vac_trend, x="posting_year_month", y="vacancies", color="field")
        self.assertIsNotNone(fig2_1)

        # 2.4 Box plot
        fig2_4 = px.box(self.demand_df, x="experience_level", y="avg_salary_usd", color="field")
        self.assertIsNotNone(fig2_4)

        # 3.1 Heatmap
        heatmap_df = self.mismatch_data["heatmap_df"]
        fig3_1 = px.imshow(heatmap_df, text_auto=True)
        self.assertIsNotNone(fig3_1)

        # 3.2 Diverging bar
        mismatch_df = self.mismatch_data["mismatch_df"]
        fig3_2 = px.bar(mismatch_df, x="gap_divergence", y="skill", orientation="h")
        self.assertIsNotNone(fig3_2)


if __name__ == "__main__":
    unittest.main()
