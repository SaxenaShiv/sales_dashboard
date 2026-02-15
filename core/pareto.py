import pandas as pd

def pareto_products(df: pd.DataFrame, threshold: float = 0.8):
    """
    Returns product-level revenue contribution and Pareto flag.
    """
    product_rev = (
        df.groupby("product_name")
        .agg(revenue=("revenue", "sum"))
        .sort_values("revenue", ascending=False)
        .reset_index()
    )

    total_revenue = product_rev["revenue"].sum()
    product_rev["revenue_share"] = product_rev["revenue"] / total_revenue
    product_rev["cumulative_share"] = product_rev["revenue_share"].cumsum()

    product_rev["pareto_flag"] = product_rev["cumulative_share"] <= threshold

    return product_rev

def pareto_categories(df: pd.DataFrame, threshold: float = 0.8):
    category_rev = (
        df.groupby("category")
        .agg(revenue=("revenue", "sum"))
        .sort_values("revenue", ascending=False)
        .reset_index()
    )

    total_revenue = category_rev["revenue"].sum()
    category_rev["revenue_share"] = category_rev["revenue"] / total_revenue
    category_rev["cumulative_share"] = category_rev["revenue_share"].cumsum()

    category_rev["pareto_flag"] = category_rev["cumulative_share"] <= threshold

    return category_rev
