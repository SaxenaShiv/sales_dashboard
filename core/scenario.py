import pandas as pd

def baseline_metrics(df: pd.DataFrame):
    return {
        "total_revenue": df["revenue"].sum(),
        "total_quantity": df["quantity"].sum(),
        "avg_price": df["unit_price"].mean()
    }

def simulate_scenario(
    baseline_revenue: float,
    price_change_pct: float = 0.0,
    volume_change_pct: float = 0.0,
    discount_pct: float = 0.0
):
    """
    All percentage values are given as:
    +10 = +10%
    -5 = -5%
    """

    price_factor = 1 + price_change_pct / 100
    volume_factor = 1 + volume_change_pct / 100
    discount_factor = 1 - discount_pct / 100

    simulated_revenue = (
        baseline_revenue
        * price_factor
        * volume_factor
        * discount_factor
    )

    delta = simulated_revenue - baseline_revenue
    delta_pct = (delta / baseline_revenue) * 100

    return {
        "simulated_revenue": simulated_revenue,
        "absolute_change": delta,
        "percentage_change": delta_pct
    }

def batch_simulation(baseline_revenue, scenarios):
    results = []

    for s in scenarios:
        outcome = simulate_scenario(
            baseline_revenue,
            s.get("price_change", 0),
            s.get("volume_change", 0),
            s.get("discount", 0)
        )

        outcome.update(s)
        results.append(outcome)

    return pd.DataFrame(results)
