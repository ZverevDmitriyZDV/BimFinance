import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.data_processing import load_data, calculate_summary, aggregate_by_category
from app.finance import calculate_roi, calculate_npv, generate_cash_flow_advanced, npv_sensitivity, find_irr
from app.visualizations import pie_chart_by_area, bar_chart_by_cost, cash_flow_chart, npv_sensitivity_chart
import streamlit as st

st.set_page_config(page_title="BIM Finance Analyzer", layout="wide")

st.title("🏗️ BIM Finance Analyzer")

uploaded_file = st.file_uploader("Upload your BIM Excel data", type=["xlsx"])


def markdown_with_tab(text_line: str, pixels_dist: int = 50):
    return st.markdown(
        f"<span style='margin-left: {pixels_dist}px'>{text_line}</span>",
        unsafe_allow_html=True
    )


if uploaded_file:
    df = load_data(uploaded_file)
    st.subheader("📋 Raw Data")
    st.dataframe(df)

    summary = calculate_summary(df)
    agg_df = aggregate_by_category(df)

    st.subheader("📊 Summary")
    markdown_with_tab(f"**Total Area:** {summary['total_area']:.2f} m²")
    markdown_with_tab(f"**Total Cost:** ${summary['total_cost']:,.2f}")

    st.subheader("📌 Aggregated by Category")
    st.dataframe(agg_df)
    st.plotly_chart(pie_chart_by_area(agg_df))
    st.plotly_chart(bar_chart_by_cost(agg_df))

    # Strategy by category
    st.subheader("🏢 Category Strategy")

    category_options = {}
    for category in agg_df["Category"]:
        option = st.selectbox(f"{category}:", ["Rent", "Sale", "Exclude"], key=category)
        category_options[category] = option

    st.subheader("📈 Financial Scenario")

    price_per_m2 = st.number_input("💰 Price per m² (rent per year or sale)", min_value=0.0, value=2500.0)
    years = st.number_input("📆 Project Duration (years)", min_value=1, value=5)
    discount_rate = st.number_input("📉 Discount Rate (for NPV)", min_value=0.0, max_value=1.0, value=0.1)

    occupancy = st.slider("🔳 Occupancy Rate", min_value=0.0, max_value=1.0, value=0.9, step=0.05)
    growth_rate = st.slider("📈 Annual Rent Growth Rate", min_value=0.0, max_value=0.2, value=0.05, step=0.01)
    start_year = st.slider("🕒 Start Year for Rent Income", min_value=1, max_value=years, value=1)

    # 🧮 Filter and calculate by strategy
    df["Strategy"] = df["Category"].map(category_options)
    selected_df = df[df["Strategy"] != "Exclude"]

    total_cost = (selected_df["Area (m²)"] * selected_df["Cost per m²"]).sum()
    rent_area = selected_df[selected_df["Strategy"] == "Rent"]["Area (m²)"].sum()
    sale_area = selected_df[selected_df["Strategy"] == "Sale"]["Area (m²)"].sum()

    total_sale = sale_area * price_per_m2

    cash_flow = generate_cash_flow_advanced(
        rent_area=rent_area,
        sale_area=sale_area,
        price_per_m2=price_per_m2,
        cost=total_cost,
        years=years,
        occupancy=occupancy,
        growth_rate=growth_rate,
        start_year=start_year
    )

    total_income = sum([cf for cf in cash_flow if cf > 0])
    yearly_income_equivalent = sum(cash_flow[1:years + 1]) / years if years > 0 else 0

    roi = calculate_roi(total_income, total_cost)
    npv = calculate_npv(yearly_income_equivalent, total_cost, years, discount_rate)

    if st.checkbox("📊 Show NPV Sensitivity Analysis"):
        rates = [i / 100 for i in range(1, 31)]  # 1% to 30%
        sensitivity = npv_sensitivity(yearly_income_equivalent, total_cost, years, rates)
        irr = find_irr(yearly_income_equivalent, total_cost, years)

        st.markdown(f"**Estimated IRR:** {irr:.2%}")
        st.plotly_chart(npv_sensitivity_chart(sensitivity, irr))

    st.subheader("📈 Results")

    markdown_with_tab(f"**Total Income:** ${total_income:,.2f}")
    markdown_with_tab(f"**ROI:** {roi * 100:.2f}%")
    markdown_with_tab(f"**NPV:** ${npv:,.2f}")

    st.plotly_chart(cash_flow_chart(cash_flow))
