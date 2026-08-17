# 🚛 FreightOpt: Smart Freight Infrastructure Planning & Budget Optimization System

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.41%2B-FF4B4B.svg)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.7%2B-F7931E.svg)](https://scikit-learn.org/)
[![Scipy](https://img.shields.io/badge/Scipy-Linear%20Programming-8CA0D7.svg)](https://scipy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An end-to-end, data-driven AI decision-support platform designed for government planners, transport authorities, and state administrators in **Tamil Nadu, India**. **FreightOpt** integrates multi-year socio-economic datasets (2020–2026) across all 38 districts of Tamil Nadu, interactive GIS spatial heatmaps, Machine Learning demand forecasting ($R^2 = 98.72\%$), Scipy Linear Programming capital budget optimization, and automated executive policy briefing suites.

---

## 🌟 Executive Key Features

- **🌐 100% Comprehensive Coverage**: Covers all **38 Tamil Nadu districts** with 266 historical multi-year records (2020–2026) spanning 20+ logistics, economic, spatial, and infrastructure indicators.
- **🤖 High-Precision ML Demand Forecasting**: Scikit-Learn **Gradient Boosting Regressor** ($R^2 = 98.72\%$, $\text{MAE} = 0.89\text{ M Tonnes}$) predicting cargo growth through 2030 with $95\%$ confidence prediction intervals.
- **💰 Scipy Linear Programming Budget Optimizer**: Integer Knapsack & LP solver (`scipy.optimize.linprog`) maximizing state-wide deficit reduction & ROI under state capital budget constraints (e.g. ₹ 500 Cr to ₹ 5,000 Cr).
- **🗺️ Interactive Folium GIS Spatial Map**: Multi-layer spatial mapping with **Freight Density Heatmaps**, **Congestion Chokepoint Alerts**, and **District Infrastructure Deficit Circle Markers**.
- **⚠️ Multi-Pillar Infrastructure Deficit Scoring**: Calculates 0–100 deficit vulnerability index across Road Density Gaps, Congestion Severity, Storage Capacity, and Rail/Port Connectivity.
- **🏗️ Infrastructure Proposals Registry**: Interactive workflow for proposing capital projects (*MMLPs, Freight Bypass Roads, Cold Storage Hubs, Industrial Rail Spurs*) with Administrator status approval controls (*Approved, Under Review, Rejected*).
- **📜 Executive Briefing Reports & Suite**: Auto-compiles formal Markdown (`.md`) and official plain-text government memorandums (`.txt`) with ASCII tables and letterheads.
- **🔌 FastAPI REST API & Integration Suite**: Complete REST API with OpenAPI `/docs` endpoints, interactive API explorer, bearer token security manager, and ULIP National Logistics Portal connectors.

---

## 🏛️ 10-Module System Architecture

FreightOpt is built using a clean, modular architecture separating data repositories, business logic engines, UI components, and API routes:

| Module | Module Name | Primary Function & Capabilities |
| :--- | :--- | :--- |
| **Module 1** | **Project Setup** | Modular architecture, native Streamlit dark theme tokens, thread-safe SQLite connection manager (`src/database/db_connection.py`). |
| **Module 2** | **Authentication UI** | SQLite `users` table with SHA-256 password hashing, active session manager (`src/logic/auth.py`), role-based views (Administrator / Planner), instant registration auto-login. |
| **Module 3** | **Executive Dashboard** | High-level KPI metric cards, multi-year dataset slider (2020–2026), regional filters, search ranking, and 4 Plotly visual analytics charts (`src/components/charts.py`). |
| **Module 4** | **Project Input** | Infrastructure proposal submission forms for all 38 TN districts, Proposals Registry with Administrator approval controls, District Master Data Editor. |
| **Module 5** | **Tamil Nadu GIS Map** | Interactive Folium map (`src/components/gis_map.py`) with CartoDB dark tiles, Freight Density Heatmap layer (`folium.plugins.HeatMap`), Congestion Alerts, and HTML popup cards. |
| **Module 6** | **Infrastructure Deficit Page** | Multi-pillar deficit index algorithm (0–100), Top 5 Vulnerable District Alert Cards, Plotly Radar / Spider Chart, and Interactive Deficit Reduction Simulator. |
| **Module 7** | **Freight Prediction Page** | ML regression models (Gradient Boosting $R^2 = 98.72\%$, Random Forest, Ridge), saved to `models/freight_predictor.joblib`. 2027–2030 scenario forecast simulator & feature importance drivers. |
| **Module 8** | **Budget Optimization** | Scipy LP Knapsack solver (`scipy.optimize.linprog`) maximizing state-wide deficit reduction & ROI under budget constraints. Regional/category distribution charts & optimal roadmap export. |
| **Module 9** | **Reports** | Automated Executive Policy Briefing compiler (`src/logic/reports_engine.py`). Generates Markdown (`.md`) and formal Government Memorandum (`.txt`) with ASCII box tables & multi-format CSV export suite. |
| **Module 10** | **API Integration** | FastAPI REST server (`src/api/main.py`) with JSON endpoints, OpenAPI Swagger UI (`/docs`), interactive API tester, Bearer token security manager, and ULIP/GIS feeds. |

---

## 📂 Project Directory Structure

```text
FreightOpt/
├── data/
│   ├── freightopt.db               # Primary SQLite Database (Districts, Users, Projects)
│   └── tn_districts_multiyear.csv  # Official 2020-2026 38-District Tamil Nadu Dataset
├── models/
│   └── freight_predictor.joblib    # Serialized Scikit-Learn Machine Learning Model
├── modules/
│   ├── module_1_project_setup.py   # Module 1 UI Page
│   ├── module_2_auth.py            # Module 2 Auth Page
│   ├── module_3_dashboard.py       # Module 3 Executive Dashboard Page
│   ├── module_4_project_input.py   # Module 4 Project Input Page
│   ├── module_5_gis_map.py         # Module 5 GIS Map Page
│   ├── module_6_deficit.py         # Module 6 Deficit Page
│   ├── module_7_prediction.py      # Module 7 Freight Prediction Page
│   ├── module_8_budget.py          # Module 8 Budget Optimization Page
│   ├── module_9_reports.py         # Module 9 Executive Reports Page
│   └── module_10_api.py            # Module 10 API Integration Page
├── src/
│   ├── api/
│   │   └── main.py                 # FastAPI REST Application Server & Endpoints
│   ├── components/
│   │   ├── charts.py               # Plotly Visualizations Engine
│   │   ├── gis_map.py              # Folium GIS Map Component
│   │   ├── header.py               # Header Banner Component
│   │   └── sidebar.py              # Sidebar Navigation Widget
│   ├── database/
│   │   ├── auth_repository.py      # User Auth Queries & SHA-256 Hashing
│   │   ├── db_connection.py        # SQLite Thread-Safe Context Manager
│   │   ├── projects_repository.py  # Projects Table CRUD & Schema Migration
│   │   ├── repository.py           # District Metrics Queries & Aggregations
│   │   └── seed_data.py            # Multi-Year SQLite Seeder
│   ├── logic/
│   │   ├── api_client.py           # API Token Manager & ULIP Feed Simulation
│   │   ├── auth.py                 # Authentication Business Logic & Session Manager
│   │   ├── budget_optimizer.py     # Scipy Linear Programming Knapsack Solver
│   │   ├── deficit_engine.py       # Multi-Pillar Deficit Index & Simulator
│   │   ├── metrics.py              # KPI Calculations & Regional Aggregations
│   │   ├── ml_prediction_engine.py # Scikit-Learn Model Training & Demand Forecast
│   │   └── reports_engine.py       # Executive Briefing & Plaintext Memorandum Compiler
│   └── config.py                   # High-Contrast CSS Tokens & Region Metadata
├── .gitignore                      # Git Ignore Rules
├── app.py                          # Main Streamlit Application Entry Point & Router
├── README.md                       # Comprehensive Project Documentation
└── requirements.txt                # Python Dependencies
```

---

## 📊 Dataset & Indicator Schema

The dataset covers all **38 districts of Tamil Nadu** from **2020 through 2026** (266 total records) with the following primary features:

| Column Name | Description | Unit / Scale |
| :--- | :--- | :--- |
| `district_name` | Name of Tamil Nadu District | Text (38 Districts) |
| `year` | Data Record Year | 2020 – 2026 |
| `region` | Geographic Region | North TN, South TN, Western TN, Central TN, Delta TN |
| `population` | Total District Population | Persons |
| `gddp_cr` | Gross District Domestic Product | ₹ Crore |
| `industrial_output_cr` | Annual Industrial Output | ₹ Crore |
| `number_of_industries` | Total Registered Manufacturing Units | Count |
| `road_length_km` | Total Road Network Length | Kilometers (km) |
| `road_density` | Road Network Density | km / 100 sq km |
| `freight_volume_million_tonnes` | **Target Freight Cargo Volume** | Million Tonnes (M Tonnes) |
| `warehouses` | Storage Warehouse Count | Count |
| `logistics_parks` | Multi-Modal Logistics Facilities | Count |
| `railway_connectivity_score` | Rail Connectivity Access Index | Score (1 – 10) |
| `port_connectivity_score` | Maritime Port Access Index | Score (1 – 10) |
| `congestion_index` | Traffic Bottleneck Index | Score (1 – 100) |
| `infrastructure_deficit_score` | Composite Vulnerability Index | Score (0 – 100) |
| `recommended_budget_cr` | Target Capital Infrastructure Outlay | ₹ Crore |

---

## ⚡ Installation & Local Setup

### Prerequisites
- Python 3.10+ installed
- Git installed

### 1. Clone the Repository
```bash
git clone https://github.com/Devibala22/FreightOpt.git
cd FreightOpt
```

### 2. Create and Activate Virtual Environment
```bash
# On Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# On Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Platform

### 1. Launch Main Streamlit Web Application
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.

### 2. Launch FastAPI REST Server (Optional)
```bash
uvicorn src.api.main:app --reload --port 8000
```
- **Base API Endpoint**: `http://localhost:8000/api/v1`
- **Interactive OpenAPI Documentation (Swagger UI)**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

---

## 🔑 Demo Access Credentials

| Role | Username / Email | Default Password |
| :--- | :--- | :--- |
| 👑 **Administrator** | `admin@tnlogistics.gov.in` | `Admin@123` |
| 📐 **Government Planner** | `planner@tnlogistics.gov.in` | `Planner@123` |

---

## 🤖 Machine Learning Model Benchmarks

Machine learning models were trained on the multi-year Tamil Nadu logistics dataset to forecast annual freight cargo volumes ($Y = \text{freight\_volume\_million\_tonnes}$):

| Model Algorithm | $R^2$ Score (Accuracy) | Mean Absolute Error (MAE) | Root Mean Squared Error (RMSE) | Status |
| :--- | :---: | :---: | :---: | :---: |
| 🥇 **Gradient Boosting Regressor** | **98.72%** | **0.896 M Tonnes** | **1.116 M Tonnes** | **Selected & Saved** |
| 🥈 **Random Forest Regressor** | 98.41% | 0.942 M Tonnes | 1.230 M Tonnes | Benchmark |
| 🥉 **Ridge Linear Regression** | 89.15% | 2.450 M Tonnes | 3.120 M Tonnes | Baseline |

---

## 📄 License & Attribution

Distributed under the MIT License. See `LICENSE` for more information.

Developed for **Tamil Nadu State Freight & Logistics Infrastructure Optimization**.
