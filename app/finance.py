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


def npv_sensitivity(
        yearly_income: float,
        cost: float,
        years: int,
        rates: list[float]
) -> dict:
    """Вычисляет NPV при разных ставках дисконтирования"""
    results = {}
    for rate in rates:
        npv = calculate_npv(yearly_income, cost, years, rate)
        results[rate] = npv
    return results


def find_irr(
        yearly_income: float,
        cost: float,
        years: int,
        precision: float = 0.0001,
        max_rate: float = 1.0
) -> float:
    """Находит IRR (ставку, при которой NPV ≈ 0) бинарным поиском"""
    low = 0.0
    high = max_rate
    while high - low > precision:
        mid = (low + high) / 2
        npv = calculate_npv(yearly_income, cost, years, mid)
        if npv > 0:
            low = mid
        else:
            high = mid
    return (low + high) / 2
