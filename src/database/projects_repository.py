"""
Infrastructure Projects Database Repository
Handles SQLite table creation, project proposals CRUD, project status approval,
and district metric updates. Includes auto-migration for table schemas.
"""

import sqlite3
import pandas as pd
from typing import Dict, Any, List, Optional
from src.database.db_connection import get_db_connection

def initialize_projects_table():
    """
    Creates the infrastructure_projects table and seeds initial sample project proposals.
    Handles automatic migration if legacy schema is detected.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Check if table exists and inspect columns
        cursor.execute("PRAGMA table_info(infrastructure_projects);")
        columns = [row["name"] for row in cursor.fetchall()]

        # If table exists but lacks 'district_name', drop legacy schema
        if columns and "district_name" not in columns:
            cursor.execute("DROP TABLE IF EXISTS infrastructure_projects;")
            print("Dropped legacy 'infrastructure_projects' table to apply updated schema.")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS infrastructure_projects (
                project_id INTEGER PRIMARY KEY AUTOINCREMENT,
                district_name TEXT NOT NULL,
                project_name TEXT NOT NULL,
                project_type TEXT NOT NULL,
                cost_estimate_cr REAL NOT NULL,
                expected_roi_multiplier REAL NOT NULL,
                implementation_year INTEGER NOT NULL,
                priority_level TEXT NOT NULL,
                description TEXT,
                submitted_by TEXT NOT NULL,
                status TEXT DEFAULT 'Proposed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Check if empty, seed sample proposals for TN
        cursor.execute("SELECT COUNT(*) FROM infrastructure_projects;")
        count = cursor.fetchone()[0]

        if count == 0:
            sample_projects = [
                {
                    "district_name": "Coimbatore",
                    "project_name": "Coimbatore Multi-Modal Logistics Park (MMLP) Phase-1",
                    "project_type": "Multi-Modal Logistics Park (MMLP)",
                    "cost_estimate_cr": 450.0,
                    "expected_roi_multiplier": 2.4,
                    "implementation_year": 2025,
                    "priority_level": "High",
                    "description": "Integrated warehousing, rail spur, and container handling terminal in Coimbatore industrial corridor.",
                    "submitted_by": "planner@tnlogistics.gov.in",
                    "status": "Approved"
                },
                {
                    "district_name": "Chengalpattu",
                    "project_name": "Sriperumbudur Freight Bypass Highway Link",
                    "project_type": "Freight Bypass Road",
                    "cost_estimate_cr": 320.0,
                    "expected_roi_multiplier": 2.1,
                    "implementation_year": 2024,
                    "priority_level": "High",
                    "description": "6-lane heavy cargo bypass connecting industrial parks directly to NH48.",
                    "submitted_by": "admin@tnlogistics.gov.in",
                    "status": "Approved"
                },
                {
                    "district_name": "Thoothukudi",
                    "project_name": "VO Chidambaranar Port Rail Connectivity Expansion",
                    "project_type": "Industrial Rail Spur",
                    "cost_estimate_cr": 280.0,
                    "expected_roi_multiplier": 2.8,
                    "implementation_year": 2025,
                    "priority_level": "High",
                    "description": "Heavy haul cargo rail link from port terminal to inland container depots.",
                    "submitted_by": "planner@tnlogistics.gov.in",
                    "status": "Under Review"
                },
                {
                    "district_name": "Madurai",
                    "project_name": "Southern Agro Cold Storage Hub",
                    "project_type": "Cold Storage Hub",
                    "cost_estimate_cr": 150.0,
                    "expected_roi_multiplier": 1.9,
                    "implementation_year": 2026,
                    "priority_level": "Medium",
                    "description": "50,000 MT temperature-controlled storage facility for agricultural exports.",
                    "submitted_by": "devi@tn.gov.in",
                    "status": "Proposed"
                }
            ]

            for p in sample_projects:
                cursor.execute("""
                    INSERT INTO infrastructure_projects (
                        district_name, project_name, project_type, cost_estimate_cr,
                        expected_roi_multiplier, implementation_year, priority_level,
                        description, submitted_by, status
                    ) VALUES (
                        :district_name, :project_name, :project_type, :cost_estimate_cr,
                        :expected_roi_multiplier, :implementation_year, :priority_level,
                        :description, :submitted_by, :status
                    );
                """, p)
            conn.commit()
            print("Successfully seeded infrastructure_projects table.")

def add_infrastructure_project(project_data: Dict[str, Any]) -> int:
    """
    Submits a new project proposal into SQLite. Returns new project ID.
    """
    initialize_projects_table()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO infrastructure_projects (
                district_name, project_name, project_type, cost_estimate_cr,
                expected_roi_multiplier, implementation_year, priority_level,
                description, submitted_by, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            project_data["district_name"],
            project_data["project_name"],
            project_data["project_type"],
            float(project_data["cost_estimate_cr"]),
            float(project_data["expected_roi_multiplier"]),
            int(project_data["implementation_year"]),
            project_data["priority_level"],
            project_data.get("description", ""),
            project_data.get("submitted_by", "system"),
            project_data.get("status", "Proposed")
        ))
        conn.commit()
        return cursor.lastrowid

def get_all_projects_df(status_filter: Optional[str] = None) -> pd.DataFrame:
    """
    Fetches all submitted infrastructure project records as a Pandas DataFrame.
    """
    initialize_projects_table()
    with get_db_connection() as conn:
        if status_filter and status_filter != "All Statuses":
            df = pd.read_sql_query(
                "SELECT * FROM infrastructure_projects WHERE status = ? ORDER BY created_at DESC;",
                conn, params=(status_filter,)
            )
        else:
            df = pd.read_sql_query(
                "SELECT * FROM infrastructure_projects ORDER BY created_at DESC;",
                conn
            )
    return df

def update_project_status(project_id: int, new_status: str) -> bool:
    """
    Updates the approval status of a project proposal.
    """
    initialize_projects_table()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE infrastructure_projects SET status = ? WHERE project_id = ?;",
            (new_status, int(project_id))
        )
        conn.commit()
        return cursor.rowcount > 0

def update_district_logistics_metrics(district_name: str, year: int, metrics: Dict[str, Any]) -> bool:
    """
    Updates specific district parameters in the districts_multiyear table.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE districts_multiyear
            SET road_density = ?,
                warehouses = ?,
                logistics_parks = ?,
                congestion_index = ?,
                infrastructure_deficit_score = ?
            WHERE LOWER(district_name) = LOWER(?) AND year = ?;
        """, (
            float(metrics["road_density"]),
            int(metrics["warehouses"]),
            int(metrics["logistics_parks"]),
            float(metrics["congestion_index"]),
            float(metrics["infrastructure_deficit_score"]),
            district_name.strip(),
            int(year)
        ))
        conn.commit()
        return cursor.rowcount > 0

if __name__ == "__main__":
    initialize_projects_table()
