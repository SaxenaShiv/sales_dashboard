import pandas as pd

def monthly_kpis(df: pd.DataFrame):
    df = df.copy()
    df["order_month"] = df["order_date"].dt.to_period("M").astype(str)

    monthly = (
        df.groupby("order_month")
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique")
        )
        .reset_index()
    )

    monthly["aov"] = monthly["revenue"] / monthly["orders"]
    return monthly

def revenue_decomposition(monthly_df: pd.DataFrame):
    df = monthly_df.copy()
    df["prev_revenue"] = df["revenue"].shift(1)
    df["prev_orders"] = df["orders"].shift(1)
    df["prev_aov"] = df["aov"].shift(1)

    df["revenue_change"] = df["revenue"] - df["prev_revenue"]

    # Decomposition logic
    df["orders_effect"] = (df["orders"] - df["prev_orders"]) * df["prev_aov"]
    df["aov_effect"] = (df["aov"] - df["prev_aov"]) * df["orders"]

    df = df.dropna()

    return df[
        [
            "order_month",
            "revenue",
            "revenue_change",
            "orders_effect",
            "aov_effect"
        ]
    ]

def interpret_revenue_change(row):
    messages = []

    if row["orders_effect"] > 0:
        messages.append("Increase driven by higher order volume")
    else:
        messages.append("Decrease driven by lower order volume")

    if row["aov_effect"] > 0:
        messages.append("Higher average order value helped")
    else:
        messages.append("Lower average order value impacted revenue")

    return " & ".join(messages)
