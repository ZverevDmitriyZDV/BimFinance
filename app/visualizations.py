import plotly.express as px
import plotly.graph_objects as go


def pie_chart_by_area(agg_df):
    fig = px.pie(
        agg_df,
        names="Category",
        values="total_area",
        title="Area Distribution by Category")
    return fig


def bar_chart_by_cost(agg_df):
    fig = px.bar(
        agg_df,
        x="Category",
        y="total_cost",
        title="Total Cost by Category")
    return fig


def cash_flow_chart(cash_flows):
    years = list(range(len(cash_flows)))
    fig = go.Figure([go.Bar(x=years, y=cash_flows)])

    fig.update_layout(
        title="💸 Cash Flow by Year",
        xaxis_title="Year",
        yaxis_title="Cash Flow ($)")
    return fig


def npv_sensitivity_chart(npv_results: dict, irr: float = None):
    rates = list(npv_results.keys())
    values = list(npv_results.values())

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=rates, y=values, mode='lines+markers', name="NPV vs Discount Rate"))

    if irr:
        fig.add_vline(x=irr, line_dash="dash", line_color="red", annotation_text=f"IRR ≈ {irr:.2%}",
                      annotation_position="top right")

    fig.update_layout(
        title="📉 NPV Sensitivity Analysis",
        xaxis_title="Discount Rate",
        yaxis_title="NPV ($)",
        hovermode="x unified"
    )
    return fig
