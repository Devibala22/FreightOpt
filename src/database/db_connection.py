"""
SQLite Database Connection Manager
Provides thread-safe connections, automatic database directory setup,
and context management for SQLite execution.
"""

import os
import sqlite3
from contextlib import contextmanager

# Base path relative to project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DB_PATH = os.path.join(DATA_DIR, "freightopt.db")

def ensure_data_directory():
    """Ensures that the data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

@contextmanager
def get_db_connection():
    """
    Context manager for SQLite connections.
    Ensures safe commit and rollback handling.
    """
    ensure_data_directory()
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Enables column access by name
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_db_path() -> str:
    """Returns absolute path to the SQLite database file."""
    ensure_data_directory()
    return DB_PATH
