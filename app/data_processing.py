import pandas as pd


def load_data(file) -> pd.DataFrame:
    df = pd.read_excel(file)
    return df


def calculate_summary(df: pd.DataFrame) -> dict:
    total_area = df["Area (m²)"].sum()
    total_cost = (df["Area (m²)"] * df["Cost per m²"]).sum()
    return {"total_area": total_area, "total_cost": total_cost}


def aggregate_by_category(df: pd.DataFrame) -> pd.DataFrame:
    agg = df.groupby("Category").agg(
        total_area=("Area (m²)", "sum"),
        avg_cost_per_m2=("Cost per m²", "mean"),
        total_cost=("Area (m²)", lambda x: (x * df.loc[x.index, "Cost per m²"]).sum())
    ).reset_index()
    return agg


