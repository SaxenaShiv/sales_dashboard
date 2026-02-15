# 📊 Sales Intelligence & Decision Platform

A comprehensive business intelligence system for sales analytics, forecasting, and scenario planning. This platform provides real-time insights into revenue drivers, data quality validation, and AI-powered sales forecasting using machine learning.

---

## 🎯 Features

### 1. **Business Overview**
   - Total revenue, order count, and average order value (AOV) metrics
   - Monthly revenue trend analysis with interactive visualizations
   - High-level KPI dashboard

### 2. **Data Quality & Validation**
   - Schema validation (required column checks)
   - Business rule validation (quantity, unit price, revenue integrity)
   - Automated outlier detection using IQR (Interquartile Range) method
   - Detailed anomaly reporting

### 3. **Revenue Driver Analysis**
   - **Decomposition**: Attribute revenue changes to order volume vs. average order value
   - **Pareto Analysis (80/20 Rule)**: Identify which products drive 80% of revenue
   - Category-level revenue contributions
   - Interactive cumulative share visualizations

### 4. **ML-Powered Sales Forecasting**
   - Random Forest regression model for 6-month ahead predictions
   - Captures trends, seasonality, and historical patterns
   - Model accuracy metrics (MAE - Mean Absolute Error)
   - Past vs. predicted visualization

### 5. **Scenario Simulator**
   - What-if analysis for pricing changes (-20% to +20%)
   - Volume impact modeling (-30% to +30%)
   - Discount scenario testing (0% to 30%)
   - Real-time revenue impact calculations

---

## 🛠️ Technology Stack

- **Framework**: [Streamlit](https://streamlit.io/) - Interactive web application
- **Data Processing**: [Pandas](https://pandas.pydata.org/) - Data manipulation
- **ML**: [Scikit-learn](https://scikit-learn.org/) - Random Forest forecasting
- **Visualization**: [Plotly](https://plotly.com/) - Interactive charts
- **Math**: [NumPy](https://numpy.org/) & [SciPy](https://scipy.org/) - Numerical computing
- **File Handling**: [PyYAML](https://pyyaml.org/) - Configuration management

---

## 📁 Project Structure

```
sales_dashboard/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── data/
│   └── sales.csv              # Sales transaction data (input)
├── config/
│   └── thresholds.yaml        # Configuration parameters
├── core/                       # Core business logic modules
│   ├── __init__.py
│   ├── validation.py          # Data quality checks
│   ├── kpi.py                 # KPI calculations & decomposition
│   ├── pareto.py              # Pareto analysis (80/20 rule)
│   ├── forecasting.py         # ML forecasting models
│   └── scenario.py            # Scenario simulation engine
├── test/                       # Unit tests
│   ├── test_validation.py
│   ├── test_kpi.py
│   ├── test_pareto.py
│   ├── test_forecasting.py
│   └── test_scenario.py
├── tests/                      # Additional test suite
├── utils/                      # Utility functions
└── venv/                       # Virtual environment (if applicable)
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Install Dependencies

```bash
# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### Required Data

Place your sales data in `data/sales.csv` with the following columns:
- `order_id` - Unique order identifier
- `order_date` - Date of order (YYYY-MM-DD format)
- `product_name` - Name of the product
- `category` - Product category
- `region` - Geographic region
- `quantity` - Number of units ordered
- `unit_price` - Price per unit ($)
- `revenue` - Total revenue for the order (quantity × unit_price)

---

## 💻 Running the Application

```bash
# Navigate to project directory
cd sales_dashboard

# Run Streamlit app
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

---

## 📖 Module Documentation

### `core/validation.py`
Validates data quality and integrity:
- **`validate_schema()`** - Ensures all required columns exist
- **`validate_business_rules()`** - Checks for invalid quantities, prices, and revenue mismatches
- **`detect_revenue_outliers()`** - Identifies statistical anomalies using IQR method
- **`run_full_validation()`** - Comprehensive validation report

### `core/kpi.py`
Calculates key performance indicators:
- **`monthly_kpis()`** - Aggregates revenue, order count, and AOV by month
- **`revenue_decomposition()`** - Separates volume impact from AOV impact on revenue changes
- **`interpret_revenue_change()`** - Human-readable explanation of revenue drivers

### `core/pareto.py`
80/20 analysis tools:
- **`pareto_products()`** - Identifies top products driving 80% of revenue
- **`pareto_categories()`** - Category-level Pareto analysis

### `core/forecasting.py`
Machine learning forecasting:
- **`prepare_monthly_series()`** - Feature engineering (month, year, trend)
- **`train_forecast_model()`** - Trains Random Forest regressor on historical data
- **`forecast_future()`** - Generates 6-month ahead predictions
- **`save_model()`** - Persists trained model for production use

### `core/scenario.py`
Scenario simulation engine:
- **`baseline_metrics()`** - Calculates current baseline KPIs
- **`simulate_scenario()`** - Models revenue impact of pricing, volume, and discount changes
- **`batch_simulation()`** - Runs multiple scenarios and returns comparison DataFrame

---

## 📊 Key Insights from the Dashboard

### Overview Tab
- View aggregate sales metrics and trends
- Monitor monthly revenue progression
- Quick business health check

### Data Quality Tab
- Identify and review data anomalies
- Validate data integrity
- Flag potential data entry errors

### Revenue Drivers Tab
- Understand what's driving revenue changes
  - **Volume Effect**: Impact of more/fewer orders
  - **AOV Effect**: Impact of higher/lower average order values
- Identify top-performing products
- Spot concentration risk (dependency on few products)

### Forecast Tab
- Predict next 6 months of revenue
- Model accuracy displayed (MAE)
- Plan inventory, staffing, and marketing based on projections

### Scenario Simulator
- Answer "what-if" questions
- Model impact of:
  - Pricing strategies
  - Volume growth initiatives
  - Promotional discounts
- Make data-driven business decisions

---

## 🧪 Testing

Run unit tests to validate module functionality:

```bash
# Run all tests
python -m pytest test/

# Run specific test file
python -m pytest test/test_all.py::test_monthly_kpis -v
```

---

## 📊 Data Format Example

**sales.csv**
```
order_id,order_date,product_name,category,region,quantity,unit_price,revenue
1001,2025-01-15,Widget A,Standard,North,5,29.99,149.95
1002,2025-01-15,Widget B,Premium,South,2,99.99,199.98
1003,2025-01-16,Gadget X,Standard,East,10,19.99,199.90
```

---

## ⚙️ Configuration

Edit `config/thresholds.yaml` to customize:
- Revenue outlier sensitivity
- Pareto threshold (default: 80% for 80/20 rule)
- Forecasting parameters
- Scenario defaults

---

## 🔍 Typical Use Cases

1. **Sales Manager**: Monitor monthly performance and identify trends
2. **Product Manager**: Understand which products drive revenue
3. **Finance Team**: Validate data integrity before reporting
4. **Strategy Team**: Run scenarios for pricing or promotion planning
5. **Operations**: Forecast demand for resource planning

---

## 📈 Performance Notes

- Data loading is cached for faster performance
- Forecasting model trains on historical data (typical training time: <1 second)
- UI updates in real-time as sliders are adjusted
- Supports datasets up to 100K+ transactions

---

## 🤝 Contributing

To extend functionality:

1. Add new analysis functions to appropriate `core/` modules
2. Write unit tests in `test/` directory
3. Add new tabs/sections to `app.py` for UI integration
4. Update this README with new features

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**MIT License Summary:**
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ⚠️ Requires attribution

---

**Last Updated**: February 2026
