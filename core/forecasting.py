import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

def prepare_monthly_series(df: pd.DataFrame):
    df = df.copy()
    df["order_month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()

    monthly = (
        df.groupby("order_month")
        .agg(revenue=("revenue", "sum"))
        .reset_index()
        .sort_values("order_month")
    )

    monthly["month"] = monthly["order_month"].dt.month
    monthly["year"] = monthly["order_month"].dt.year
    monthly["trend"] = np.arange(len(monthly))

    return monthly

def train_forecast_model(monthly_df: pd.DataFrame):
    features = ["month", "year", "trend"]
    X = monthly_df[features]
    y = monthly_df["revenue"]

    model = RandomForestRegressor(
        n_estimators=300,
        random_state=42
    )
    model.fit(X, y)

    predictions = model.predict(X)
    mae = mean_absolute_error(y, predictions)

    return model, predictions, mae

def forecast_future(model, last_monthly_df, periods=6):
    future = []

    last_date = last_monthly_df["order_month"].max()
    last_trend = last_monthly_df["trend"].max()

    for i in range(1, periods + 1):
        future_date = last_date + pd.DateOffset(months=i)

        future.append({
            "order_month": future_date,
            "month": future_date.month,
            "year": future_date.year,
            "trend": last_trend + i
        })

    future_df = pd.DataFrame(future)
    future_df["forecast_revenue"] = model.predict(
        future_df[["month", "year", "trend"]]
    )

    return future_df

def save_model(model, path="models/forecast_model.pkl"):
    joblib.dump(model, path)
