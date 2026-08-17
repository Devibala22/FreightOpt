"""
Tamil Nadu Multi-Year Freight & Infrastructure Dataset Seeder
Populates the SQLite database using the official 2020-2026 Tamil Nadu 38-District dataset.
"""

import os
import sqlite3
import pandas as pd
from src.database.db_connection import get_db_connection, DATA_DIR

CSV_PATH = os.path.join(DATA_DIR, "tn_districts_multiyear.csv")

def initialize_database():
    """
    Initializes the SQLite schema and seeds multi-year district metrics (2020-2026).
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 1. Create Multi-Year District Metrics Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS districts_multiyear (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                district_id TEXT NOT NULL,
                district_name TEXT NOT NULL,
                year INTEGER NOT NULL,
                region TEXT NOT NULL,
                population REAL NOT NULL,
                area_sq_km REAL NOT NULL,
                population_density REAL NOT NULL,
                gddp_cr REAL NOT NULL,
                industrial_output_cr REAL NOT NULL,
                number_of_industries INTEGER NOT NULL,
                road_length_km REAL NOT NULL,
                road_density REAL NOT NULL,
                freight_volume_million_tonnes REAL NOT NULL,
                warehouses INTEGER NOT NULL,
                logistics_parks INTEGER NOT NULL,
                railway_connectivity_score REAL NOT NULL,
                port_connectivity_score REAL NOT NULL,
                congestion_index REAL NOT NULL,
                infrastructure_deficit_score REAL NOT NULL,
                recommended_budget_cr REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 2. Check if seeded
        cursor.execute("SELECT COUNT(*) FROM districts_multiyear;")
        count = cursor.fetchone()[0]

        if count == 0 and os.path.exists(CSV_PATH):
            df_csv = pd.read_csv(CSV_PATH)
            # Drop empty trailing rows if present
            df_csv = df_csv.dropna(subset=["district_id", "district_name", "year"])
            df_csv["year"] = df_csv["year"].astype(int)
            
            df_csv.to_sql("districts_multiyear", conn, if_exists="append", index=False)
            print(f"Successfully loaded {len(df_csv)} records (2020-2026) into 'districts_multiyear' table.")
        else:
            print(f"Database already contains {count} multi-year records.")

if __name__ == "__main__":
    initialize_database()
