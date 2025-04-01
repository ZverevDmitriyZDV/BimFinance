import plotly.express as px
import plotly.graph_objects as go


def pie_chart_by_area(agg_df):
    fig = px.pie(agg_df, names="Category", values="total_area", title="Area Distribution by Category")
    return fig


def bar_chart_by_cost(agg_df):
    fig = px.bar(agg_df, x="Category", y="total_cost", title="Total Cost by Category")
    return fig


def cash_flow_chart(cash_flows):
    years = list(range(len(cash_flows)))
    fig = go.Figure([go.Bar(x=years, y=cash_flows)])
    fig.update_layout(title="💸 Cash Flow by Year", xaxis_title="Year", yaxis_title="Cash Flow ($)")
    return fig
