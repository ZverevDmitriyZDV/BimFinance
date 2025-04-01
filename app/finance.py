def calculate_roi(revenue: float, cost: float) -> float:
    if cost == 0:
        return 0
    return (revenue - cost) / cost


def calculate_npv(revenue: float, cost: float, years: int, discount_rate: float) -> float:
    npv = -cost
    for t in range(1, years + 1):
        npv += revenue / ((1 + discount_rate) ** t)
    return npv


def generate_cash_flow(revenue_per_year: float, cost: float, years: int) -> list:
    flows = [-cost] + [revenue_per_year] * years
    return flows


def generate_cash_flow_advanced(
        rent_area: float,
        sale_area: float,
        price_per_m2: float,
        cost: float,
        years: int,
        occupancy: float,
        growth_rate: float,
        start_year: int
) -> list:
    """
    Возвращает список денежных потоков с учётом:
    - задержки старта аренды
    - ежегодного роста стоимости аренды
    - коэффициента заполняемости
    - дохода от продажи в последний год
    """
    cash_flows = [-cost]
    for t in range(1, years + 1):
        if t < start_year:
            rent_income = 0
        else:
            rent_income = rent_area * price_per_m2 * occupancy * ((1 + growth_rate) ** (t - start_year))
        cash_flows.append(rent_income)

    # доход от продажи
    sale_income = sale_area * price_per_m2
    cash_flows[-1] += sale_income

    return cash_flows


