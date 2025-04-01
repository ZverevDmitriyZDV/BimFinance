from app.finance import generate_cash_flow_advanced, calculate_roi, calculate_npv, find_irr


def calculate_scenario(params, total_area, total_cost):
    rent_area = total_area * params["rent_share"]
    sale_area = total_area * params["sale_share"]

    cash_flow = generate_cash_flow_advanced(
        rent_area=rent_area,
        sale_area=sale_area,
        price_per_m2=params["price_per_m2"],
        cost=total_cost,
        years=params["years"],
        occupancy=params["occupancy"],
        growth_rate=params["growth_rate"],
        start_year=params["start_year"]
    )

    total_income = sum(cf for cf in cash_flow if cf > 0)
    yearly_income = sum(cash_flow[1:params["years"] + 1]) / params["years"]

    roi = calculate_roi(total_income, total_cost)
    npv = calculate_npv(yearly_income, total_cost, params["years"], params.get("discount_rate", 0.1))
    irr = find_irr(yearly_income, total_cost, params["years"])

    return {
        "Scenario": params["name"],
        "ROI": f"{roi * 100:.2f}%",
        "NPV": f"${npv:,.0f}",
        "IRR": f"{irr * 100:.2f}%"
    }
