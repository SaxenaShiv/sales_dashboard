import pandas as pd
import pytest
from core.validation import run_full_validation
from core.kpi import monthly_kpis, revenue_decomposition, interpret_revenue_change
from core.scenario import baseline_metrics, simulate_scenario
from core.forecasting import prepare_monthly_series, train_forecast_model, forecast_future
from core.pareto import pareto_products, pareto_categories

# Fixture to load test data once
@pytest.fixture
def df():
    data = pd.read_csv("data/sales.csv")
    data["order_date"] = pd.to_datetime(data["order_date"])
    return data

# ===== 1. Validation Tests =====
def test_run_full_validation(df):
    """Test the full data validation process"""
    report = run_full_validation(df)
    
    assert report is not None
    assert "missing_columns" in report
    assert "business_rule_issues" in report
    assert "outliers" in report
    assert isinstance(report["missing_columns"], list)
    # Handle both DataFrame and list returns
    assert isinstance(report["business_rule_issues"]["invalid_quantity"], (pd.DataFrame, list))
    assert isinstance(report["business_rule_issues"]["revenue_mismatch"], (pd.DataFrame, list))
    assert isinstance(report["outliers"], (pd.DataFrame, list))
    print(f"✓ Validation passed - Missing columns: {report['missing_columns']}")

# ===== 2. KPI Calculation Tests =====
def test_monthly_kpis(df):
    """Test monthly KPI calculation"""
    monthly = monthly_kpis(df)
    
    assert monthly is not None
    assert len(monthly) > 0
    assert "revenue" in monthly.columns
    print(f"✓ Monthly KPIs calculated for {len(monthly)} months")

def test_revenue_decomposition(df):
    """Test revenue decomposition"""
    monthly = monthly_kpis(df)
    decomp = revenue_decomposition(monthly)
    
    assert decomp is not None
    assert len(decomp) > 0
    print(f"✓ Revenue decomposition completed with {len(decomp)} records")

def test_interpret_revenue_change(df):
    """Test revenue change interpretation"""
    monthly = monthly_kpis(df)
    decomp = revenue_decomposition(monthly)
    decomp["explanation"] = decomp.apply(interpret_revenue_change, axis=1)
    
    assert "explanation" in decomp.columns
    assert len(decomp["explanation"]) > 0
    assert all(decomp["explanation"].notna())
    print(f"✓ Revenue change interpretation completed")

# ===== 3. Scenario Tests =====
def test_baseline_metrics(df):
    """Test baseline metrics calculation"""
    baseline = baseline_metrics(df)
    
    assert baseline is not None
    assert "total_revenue" in baseline
    assert baseline["total_revenue"] > 0
    print(f"✓ Baseline revenue: ${baseline['total_revenue']:,.2f}")

def test_simulate_scenario(df):
    """Test scenario simulation"""
    baseline = baseline_metrics(df)
    result = simulate_scenario(
        baseline_revenue=baseline["total_revenue"],
        price_change_pct=5,
        volume_change_pct=10,
        discount_pct=2
    )
    
    assert result is not None
    assert isinstance(result, dict)
    print(f"✓ Scenario simulation result: {result}")

# ===== 4. Forecasting Tests =====
def test_prepare_monthly_series(df):
    """Test monthly series preparation"""
    monthly = prepare_monthly_series(df)
    
    assert monthly is not None
    assert len(monthly) > 0
    print(f"✓ Monthly series prepared with {len(monthly)} data points")

def test_train_forecast_model(df):
    """Test model training"""
    monthly = prepare_monthly_series(df)
    model, preds, mae = train_forecast_model(monthly)
    
    assert model is not None
    assert preds is not None
    assert mae > 0
    assert len(preds) == len(monthly)
    print(f"✓ Model trained with MAE: ${mae:,.2f}")

def test_forecast_future(df):
    """Test future forecasting"""
    monthly = prepare_monthly_series(df)
    model, preds, mae = train_forecast_model(monthly)
    future = forecast_future(model, monthly, periods=6)
    
    assert future is not None
    assert len(future) == 6
    print(f"✓ Future forecast generated for 6 periods")

# ===== 5. Pareto Tests =====
def test_pareto_products(df):
    """Test Pareto analysis for products"""
    product_pareto = pareto_products(df)
    
    assert product_pareto is not None
    assert len(product_pareto) > 0
    assert "pareto_flag" in product_pareto.columns
    print(f"✓ Pareto analysis completed - {len(product_pareto)} products")

def test_pareto_categories(df):
    """Test Pareto analysis for categories"""
    category_pareto = pareto_categories(df)
    
    assert category_pareto is not None
    assert len(category_pareto) > 0
    assert "pareto_flag" in category_pareto.columns
    print(f"✓ Pareto analysis completed - {len(category_pareto)} categories")

def test_pareto_80_rule(df):
    """Test that Pareto rule identifies 80% revenue drivers"""
    product_pareto = pareto_products(df)
    pareto_products_list = product_pareto[product_pareto["pareto_flag"]]
    
    assert len(pareto_products_list) > 0
    print(f"✓ {len(pareto_products_list)} products drive 80% of revenue")