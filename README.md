# FreightOpt – Smart Freight Infrastructure Planning & Budget Optimization

An interactive, data-driven decision support system designed specifically for **Tamil Nadu** government planners and administrators to identify logistics infrastructure gaps, predict freight demand using Machine Learning, prioritize districts, and optimize budget allocation.

## 🚀 Technology Stack
- **Python 3.10+**
- **Streamlit** (Interactive Web UI Framework)
- **Pandas & NumPy** (Data Analytics & Processing)
- **Plotly** (Dynamic Analytical Charts)
- **Folium & Streamlit-Folium** (Spatial GIS & Interactive Maps)
- **SQLite** (Embedded Relational Database)
- **Scikit-learn** (Freight Demand Forecasting ML Pipeline)
- **Joblib** (Model Serialization & Persistence)

## 📁 Architecture Layout

```
FreightOpt/
├── app.py                     # Main Streamlit Application Entry Point
├── requirements.txt           # Python Package Dependencies
├── README.md                  # System Documentation
│
├── data/                      # Persistent Database Storage
│   └── freightopt.db          # SQLite DB (Auto-seeded with 38 TN Districts Data)
│
├── models/                    # Serialized Machine Learning Models (.joblib)
│
├── src/                       # Core Application Package
│   ├── config.py              # Application Constants, Color Palettes & CSS Styling
│   ├── database/              # Data Access Layer & Seed Engine
│   │   ├── db_connection.py   # SQLite Connection Manager
│   │   ├── seed_data.py       # TN 38 Districts Logistics Seeder
│   │   └── repository.py      # Data Access Layer & Analytical Queries
│   ├── logic/                 # Pure Business Logic Modules
│   └── components/            # Reusable Modern UI Components
│       ├── header.py          # Custom Modern App Header Banner
│       └── sidebar.py         # Role-based Sidebar Navigation
│
└── modules/                   # 10 Application Modules (Independently Runnable)
    ├── module_1_project_setup.py  # Module 1: Project Setup & Diagnostics
    ├── module_2_auth.py           # Module 2: Authentication UI
    ├── module_3_dashboard.py      # Module 3: Executive Overview Dashboard
    ├── module_4_project_input.py  # Module 4: Project & Data Input Forms
    ├── module_5_gis_map.py        # Module 5: Tamil Nadu Interactive GIS Map
    ├── module_6_deficit_page.py   # Module 6: Infrastructure Deficit Analysis
    ├── module_7_prediction_page.py# Module 7: Freight ML Prediction Engine
    ├── module_8_budget_opt.py     # Module 8: Constraint Budget Optimization
    ├── module_9_reports.py        # Module 9: Summary & Analytics Reports
    └── module_10_api_integration.py # Module 10: API Connectors & Integrations
```

## 🛠️ How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the main application:
   ```bash
   streamlit run app.py
   ```

3. Or run Module 1 independently:
   ```bash
   streamlit run modules/module_1_project_setup.py
   ```
