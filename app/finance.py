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
