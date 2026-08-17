"""
User Authentication Database Repository
Handles SQLite user table creation, seeding demo accounts,
and user CRUD operations.
"""

import sqlite3
import hashlib
from typing import Dict, Any, Optional
from src.database.db_connection import get_db_connection

def hash_password(password: str) -> str:
    """Returns SHA-256 hashed password string."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def initialize_users_table():
    """
    Creates the users table and seeds default demo accounts for Admin and Planner.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL,
                department TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Check if empty, seed default accounts
        cursor.execute("SELECT COUNT(*) FROM users;")
        count = cursor.fetchone()[0]

        if count == 0:
            demo_users = [
                {
                    "email": "admin@tnlogistics.gov.in",
                    "password_hash": hash_password("Admin@123"),
                    "full_name": "Dr. K. Arulmozhi (IAS)",
                    "role": "Administrator",
                    "department": "TN Infrastructure Development Board"
                },
                {
                    "email": "planner@tnlogistics.gov.in",
                    "password_hash": hash_password("Planner@123"),
                    "full_name": "S. Ramachandran",
                    "role": "Decision Maker (Government Planner)",
                    "department": "TN Highways & Minor Ports Department"
                }
            ]
            for u in demo_users:
                cursor.execute("""
                    INSERT INTO users (email, password_hash, full_name, role, department)
                    VALUES (:email, :password_hash, :full_name, :role, :department);
                """, u)
            conn.commit()
            print("Successfully initialized users table with demo accounts.")

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """
    Fetches user record dictionary by email address.
    """
    initialize_users_table()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(?);", (email.strip(),))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

def create_user(email: str, password: str, full_name: str, role: str, department: str) -> Dict[str, Any]:
    """
    Registers a new user into the database.
    """
    initialize_users_table()
    if get_user_by_email(email):
        raise ValueError(f"User with email '{email}' already exists.")
    
    pwd_hash = hash_password(password)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (email, password_hash, full_name, role, department)
            VALUES (?, ?, ?, ?, ?);
        """, (email.strip().lower(), pwd_hash, full_name.strip(), role, department.strip()))
        conn.commit()
    
    return get_user_by_email(email)

if __name__ == "__main__":
    initialize_users_table()
