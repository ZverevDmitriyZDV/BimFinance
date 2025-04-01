import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.data_processing import load_data, calculate_summary, aggregate_by_category
from app.visualizations import pie_chart_by_area, bar_chart_by_cost, cash_flow_chart
from app.finance import calculate_roi, calculate_npv, generate_cash_flow


st.title("🏗️ BIM Finance Analyzer")

uploaded_file = st.file_uploader("Upload your BIM Excel data", type=["xlsx"])

if uploaded_file:
    df = load_data(uploaded_file)
    st.subheader("📋 Raw Data")
    st.dataframe(df)

    summary = calculate_summary(df)
    st.subheader("📊 Summary")
    st.markdown(f"**Total Area:** {summary['total_area']:.2f} m²")
    st.markdown(f"**Total Cost:** ${summary['total_cost']:,.2f}")

    agg_df = aggregate_by_category(df)
    st.subheader("📌 Aggregated by Category")
    st.dataframe(agg_df)

    st.plotly_chart(pie_chart_by_area(agg_df))
    st.plotly_chart(bar_chart_by_cost(agg_df))

    st.subheader("📈 Financial Scenario")

    scenario = st.selectbox("Choose Scenario", ["Rent", "Sale"])

    price_per_m2 = st.number_input("Price per m² (rent per year or sale)", min_value=0.0, value=2500.0)
    years = st.number_input("Project Duration (years)", min_value=1, value=5)
    discount_rate = st.number_input("Discount Rate (for NPV)", min_value=0.0, max_value=1.0, value=0.1)

    total_area = summary["total_area"]
    total_cost = summary["total_cost"]

    if scenario == "Rent":
        yearly_income = total_area * price_per_m2
        total_income = yearly_income * years
    else:
        total_income = total_area * price_per_m2
        yearly_income = 0  # For NPV calc

    roi = calculate_roi(total_income, total_cost)
    npv = calculate_npv(total_income if scenario == "Sale" else yearly_income, total_cost, years, discount_rate)

    st.markdown(f"**Total Revenue:** ${total_income:,.2f}")
    st.markdown(f"**ROI:** {roi * 100:.2f}%")
    st.markdown(f"**NPV:** ${npv:,.2f}")

    if scenario == "Rent":
        cash_flow = generate_cash_flow(yearly_income, total_cost, years)
    else:
        cash_flow = [-total_cost] + [0] * (years - 1) + [total_income]

    st.plotly_chart(cash_flow_chart(cash_flow))
