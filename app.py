import streamlit as st
import pandas as pd
import plotly.express as px

from core.validation import run_full_validation
from core.kpi import monthly_kpis, revenue_decomposition
from core.pareto import pareto_products
from core.forecasting import (
    prepare_monthly_series,
    train_forecast_model,
    forecast_future
)
from core.scenario import baseline_metrics, simulate_scenario

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="E-commerce Revenue Intelligence & Forecasting System",
    layout="wide"
)

st.title("📊 E-commerce Revenue Intelligence & Forecasting System")

# ---------------- DATA LOAD ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/sales.csv")
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df

df = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.header("Controls")
show_raw = st.sidebar.checkbox("Show raw data")

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Data Quality",
    "Revenue Drivers",
    "Forecast",
    "Scenario Simulator"
])

# ==================================================
# TAB 1 — OVERVIEW
# ==================================================
with tab1:
    st.subheader("Business Overview")

    total_rev = df["revenue"].sum()
    total_orders = df["order_id"].nunique()
    aov = total_rev / total_orders
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Revenue", f"${total_rev:,.0f}")
    c2.metric("Total Orders", total_orders)
    c3.metric("Avg Order Value", f"${aov:,.0f}")

    monthly = monthly_kpis(df)
    fig = px.line(
        monthly,
        x="order_month",
        y="revenue",
        title="Monthly Revenue Trend"
    )
    fig.update_traces(hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>")
    st.plotly_chart(fig, width='stretch')

    if show_raw:
        st.dataframe(
            df.head(100).style.format({
                'unit_price': '${:,.2f}',
                'revenue': '${:,.2f}'
            })
        )

# ==================================================
# TAB 2 — DATA QUALITY
# ==================================================
with tab2:
    st.subheader("Data Validation & Anomalies")

    report = run_full_validation(df)

    st.write("**Missing Columns:**", report["missing_columns"])

    st.metric(
        "Revenue Outliers",
        len(report["outliers"])
    )

    if len(report["outliers"]) > 0:
        st.dataframe(
            report["outliers"].head(50).style.format({
                'unit_price': '${:,.2f}',
                'revenue': '${:,.2f}'
            }, na_rep="-")
        )

# ==================================================
# TAB 3 — REVENUE DRIVERS
# ==================================================
with tab3:
    st.subheader("Revenue Driver Decomposition")

    monthly = monthly_kpis(df)
    decomp = revenue_decomposition(monthly)

    fig = px.bar(
        decomp,
        x="order_month",
        y=["orders_effect", "aov_effect"],
        title="Revenue Change Attribution",
        barmode="relative"
    )
    fig.update_traces(hovertemplate="<b>%{x}</b><br>%{fullData.name}: $%{y:,.2f}<extra></extra>")
    st.plotly_chart(fig, width='stretch')

    st.dataframe(
        decomp.style.format({
            'revenue': '${:,.2f}',
            'revenue_change': '${:,.2f}',
            'orders_effect': '${:,.2f}',
            'aov_effect': '${:,.2f}'
        }, na_rep="-")
    )

    st.subheader("Pareto (80/20) Products")
    pareto_df = pareto_products(df)

    fig2 = px.line(
        pareto_df,
        x=pareto_df.index,
        y="cumulative_share",
        title="Cumulative Revenue Contribution"
    )
    fig2.update_traces(hovertemplate="<b>%{x}</b><br>Share: %{y:.2f}%<extra></extra>")
    st.plotly_chart(fig2, width='stretch')

    st.dataframe(
        pareto_df.style.format({
            'revenue': '${:,.2f}',
            'cumulative_share': '{:.2f}%'
        }, na_rep="-")
    )

# ==================================================
# TAB 4 — FORECAST
# ==================================================
with tab4:
    st.subheader("Sales Forecasting (ML)")

    monthly_series = prepare_monthly_series(df)
    model, preds, mae = train_forecast_model(monthly_series)

    monthly_series["prediction"] = preds

    fig = px.line(
        monthly_series,
        x="order_month",
        y=["revenue", "prediction"],
        title=f"Actual vs Predicted (MAE = {mae:,.0f})"
    )
    fig.update_traces(hovertemplate="<b>%{x}</b><br>%{fullData.name}: $%{y:,.2f}<extra></extra>")
    st.plotly_chart(fig, width='stretch')

    future = forecast_future(model, monthly_series, periods=6)
    st.subheader("Next 6-Month Forecast")
    st.dataframe(
        future.style.format({
            'forecast_revenue': '${:,.2f}',
            'prediction': '${:,.2f}'
        }, na_rep="-")
    )

# ==================================================
# TAB 5 — SCENARIO SIMULATOR
# ==================================================
with tab5:
    st.subheader("What-If Revenue Simulator")

    baseline = baseline_metrics(df)

    price_change = st.slider("Price Change (%)", -20, 20, 0)
    volume_change = st.slider("Volume Change (%)", -30, 30, 0)
    discount = st.slider("Discount (%)", 0, 30, 0)

    result = simulate_scenario(
        baseline["total_revenue"],
        price_change,
        volume_change,
        discount
    )

    c1, c2, c3 = st.columns(3)
    c1.metric(
        "Simulated Revenue",
        f"${result['simulated_revenue']:,.0f}"
    )
    c2.metric(
        "Absolute Change",
        f"${result['absolute_change']:,.0f}"
    )
    c3.metric(
        "% Change",
        f"{result['percentage_change']:.2f}%"
    )
