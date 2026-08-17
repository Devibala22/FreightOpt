"""
Machine Learning Freight Prediction & Demand Forecasting Engine
Trains Scikit-Learn regression models (Random Forest, Gradient Boosting, Linear Regression)
on official 2020-2026 multi-year dataset to forecast 2027-2030 Tamil Nadu freight demand.
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List, Optional
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

from src.database.repository import get_all_districts_df

# Path to saved model file inside models/ directory
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "models"))
MODEL_FILE_PATH = os.path.join(MODEL_DIR, "freight_predictor.joblib")

# Feature Columns used for Machine Learning
FEATURE_COLS = [
    "gddp_cr",
    "industrial_output_cr",
    "number_of_industries",
    "population",
    "road_density",
    "warehouses",
    "logistics_parks",
    "railway_connectivity_score",
    "port_connectivity_score"
]
TARGET_COL = "freight_volume_million_tonnes"

def train_freight_models() -> Dict[str, Any]:
    """
    Fetches full 2020-2026 multi-year dataset, trains Random Forest, Gradient Boosting,
    and Ridge regression models, evaluates performance ($R^2$, MAE, RMSE), and saves best model.
    """
    df = get_all_districts_df(year="All")
    if df.empty:
        raise ValueError("Multi-year dataset is empty. Cannot train ML models.")

    X = df[FEATURE_COLS].copy()
    y = df[TARGET_COL].copy()

    # Train/Test Split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 1. Random Forest Regressor
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_preds = rf_model.predict(X_test)
    rf_metrics = {
        "r2": float(r2_score(y_test, rf_preds)),
        "mae": float(mean_absolute_error(y_test, rf_preds)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, rf_preds)))
    }

    # 2. Gradient Boosting Regressor
    gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    gb_model.fit(X_train, y_train)
    gb_preds = gb_model.predict(X_test)
    gb_metrics = {
        "r2": float(r2_score(y_test, gb_preds)),
        "mae": float(mean_absolute_error(y_test, gb_preds)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, gb_preds)))
    }

    # 3. Ridge Linear Model
    ridge_model = Ridge()
    ridge_model.fit(X_train, y_train)
    ridge_preds = ridge_model.predict(X_test)
    ridge_metrics = {
        "r2": float(r2_score(y_test, ridge_preds)),
        "mae": float(mean_absolute_error(y_test, ridge_preds)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, ridge_preds)))
    }

    # Select Best Model based on R2 Score
    best_model_name = "Random Forest"
    best_model = rf_model
    best_metrics = rf_metrics

    if gb_metrics["r2"] > rf_metrics["r2"]:
        best_model_name = "Gradient Boosting"
        best_model = gb_model
        best_metrics = gb_metrics

    # Feature Importances
    importances = best_model.feature_importances_ if hasattr(best_model, "feature_importances_") else np.zeros(len(FEATURE_COLS))
    feat_imp_df = pd.DataFrame({
        "feature": [f.replace("_", " ").title() for f in FEATURE_COLS],
        "importance": importances
    }).sort_values(by="importance", ascending=True)

    # Save Best Model to Disk
    os.makedirs(MODEL_DIR, exist_ok=True)
    payload = {
        "model": best_model,
        "model_name": best_model_name,
        "feature_cols": FEATURE_COLS,
        "metrics": best_metrics,
        "rf_metrics": rf_metrics,
        "gb_metrics": gb_metrics,
        "ridge_metrics": ridge_metrics
    }
    joblib.dump(payload, MODEL_FILE_PATH)
    print(f"Successfully trained and saved {best_model_name} model to {MODEL_FILE_PATH} with R2 = {best_metrics['r2']:.4f}")

    return {
        "best_model_name": best_model_name,
        "metrics": best_metrics,
        "rf_metrics": rf_metrics,
        "gb_metrics": gb_metrics,
        "ridge_metrics": ridge_metrics,
        "feature_importance_df": feat_imp_df
    }

def load_trained_model_payload() -> Dict[str, Any]:
    """
    Loads trained ML payload from disk. Trains if not present.
    """
    if not os.path.exists(MODEL_FILE_PATH):
        return train_freight_models()
    try:
        payload = joblib.load(MODEL_FILE_PATH)
        best_model = payload["model"]
        importances = best_model.feature_importances_ if hasattr(best_model, "feature_importances_") else np.zeros(len(FEATURE_COLS))
        feat_imp_df = pd.DataFrame({
            "feature": [f.replace("_", " ").title() for f in FEATURE_COLS],
            "importance": importances
        }).sort_values(by="importance", ascending=True)
        payload["feature_importance_df"] = feat_imp_df
        return payload
    except Exception as e:
        print(f"Error loading saved model: {e}. Retraining...")
        return train_freight_models()

def predict_district_freight_scenario(
    district_row: pd.Series,
    target_year: int,
    gddp_growth_pct: float = 6.0,
    industrial_growth_pct: float = 8.0,
    added_road_density: float = 0.0,
    added_warehouses: int = 0
) -> Dict[str, Any]:
    """
    Predicts future freight volume for a specific district under growth scenario multipliers.
    """
    payload = load_trained_model_payload()
    model = payload["model"]

    years_ahead = max(1, target_year - 2026)

    # Apply Compound Growth
    gddp_mult = (1.0 + (gddp_growth_pct / 100.0)) ** years_ahead
    ind_mult = (1.0 + (industrial_growth_pct / 100.0)) ** years_ahead

    base_features = {
        "gddp_cr": float(district_row["gddp_cr"]) * gddp_mult,
        "industrial_output_cr": float(district_row["industrial_output_cr"]) * ind_mult,
        "number_of_industries": int(float(district_row["number_of_industries"]) * (1.0 + (industrial_growth_pct / 200.0) * years_ahead)),
        "population": float(district_row["population"]) * (1.0 + 0.01 * years_ahead),
        "road_density": float(district_row["road_density"]) + added_road_density,
        "warehouses": int(district_row["warehouses"]) + added_warehouses,
        "logistics_parks": int(district_row["logistics_parks"]),
        "railway_connectivity_score": float(district_row["railway_connectivity_score"]),
        "port_connectivity_score": float(district_row["port_connectivity_score"])
    }

    input_df = pd.DataFrame([base_features])[FEATURE_COLS]
    predicted_volume = float(model.predict(input_df)[0])

    current_volume = float(district_row["freight_volume_million_tonnes"])
    delta_volume = predicted_volume - current_volume
    growth_pct = (delta_volume / current_volume) * 100.0 if current_volume > 0 else 0.0

    return {
        "target_year": target_year,
        "current_volume": current_volume,
        "predicted_volume": max(1.0, round(predicted_volume, 2)),
        "delta_volume": round(delta_volume, 2),
        "growth_pct": round(growth_pct, 1),
        "confidence_lower": max(1.0, round(predicted_volume * 0.93, 2)),
        "confidence_upper": round(predicted_volume * 1.07, 2)
    }

def generate_statewide_projections_2027_2030() -> pd.DataFrame:
    """
    Generates multi-year forecast matrix (2027 - 2030) across all 38 TN districts.
    """
    current_2026_df = get_all_districts_df(year=2026)
    records = []

    for _, row in current_2026_df.iterrows():
        for year in [2027, 2028, 2029, 2030]:
            res = predict_district_freight_scenario(
                district_row=row,
                target_year=year,
                gddp_growth_pct=6.5,
                industrial_growth_pct=8.0
            )
            records.append({
                "district_name": row["district_name"],
                "region": row["region"],
                "year": year,
                "predicted_freight_mton": res["predicted_volume"],
                "growth_pct": res["growth_pct"],
                "confidence_lower": res["confidence_lower"],
                "confidence_upper": res["confidence_upper"]
            })

    return pd.DataFrame(records)

if __name__ == "__main__":
    res = train_freight_models()
    print("ML Pipeline verified cleanly:", res["best_model_name"], res["metrics"])
