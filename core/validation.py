import pandas as pd
import numpy as np

REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "product_name",
    "category",
    "region",
    "quantity",
    "unit_price",
    "revenue"
]

def validate_schema(df: pd.DataFrame):
    missing_cols = set(REQUIRED_COLUMNS) - set(df.columns)
    return list(missing_cols)

def validate_business_rules(df: pd.DataFrame):
    issues = {}

    issues["invalid_quantity"] = df[df["quantity"] <= 0]
    issues["invalid_price"] = df[df["unit_price"] <= 0]

    # Revenue mismatch (allow small rounding error)
    calculated_revenue = df["quantity"] * df["unit_price"]
    mismatch = np.abs(df["revenue"] - calculated_revenue) > 1.0

    issues["revenue_mismatch"] = df[mismatch]

    return issues

def detect_revenue_outliers(df: pd.DataFrame):
    q1 = df["revenue"].quantile(0.25)
    q3 = df["revenue"].quantile(0.75)
    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    return df[(df["revenue"] < lower) | (df["revenue"] > upper)]

def run_full_validation(df: pd.DataFrame):
    report = {}

    report["missing_columns"] = validate_schema(df)
    report["business_rule_issues"] = validate_business_rules(df)
    report["outliers"] = detect_revenue_outliers(df)

    return report
