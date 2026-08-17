"""
Authentication Business & Session Logic
Manages user authentication, password verification,
and Streamlit session_state state machine.
"""

import streamlit as st
from typing import Dict, Any, Optional
from src.database.auth_repository import get_user_by_email, create_user, hash_password

def init_auth_session():
    """
    Initializes session_state variables for authentication if not present.
    """
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "current_user" not in st.session_state:
        st.session_state["current_user"] = None
    if "active_role" not in st.session_state:
        st.session_state["active_role"] = "Administrator"

def authenticate(email: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Verifies user credentials. Returns user dict on success, None on failure.
    """
    user = get_user_by_email(email)
    if not user:
        return None
    
    input_hash = hash_password(password)
    if user["password_hash"] == input_hash:
        return user
    return None

def login_user(user: Dict[str, Any]):
    """
    Sets session state to logged in with active user metadata.
    """
    init_auth_session()
    st.session_state["authenticated"] = True
    st.session_state["current_user"] = user
    st.session_state["active_role"] = user["role"]

def logout_user():
    """
    Logs out the user and clears session state.
    """
    init_auth_session()
    st.session_state["authenticated"] = False
    st.session_state["current_user"] = None

def quick_demo_login(role: str = "Administrator"):
    """
    Performs quick demo login for Admin or Planner.
    """
    if role == "Administrator":
        email = "admin@tnlogistics.gov.in"
    else:
        email = "planner@tnlogistics.gov.in"
    
    user = get_user_by_email(email)
    if user:
        login_user(user)
        return True
    return False

def get_current_user() -> Optional[Dict[str, Any]]:
    """
    Returns current authenticated user dictionary or None.
    """
    init_auth_session()
    return st.session_state.get("current_user", None)

def is_authenticated() -> bool:
    """
    Returns True if a user is actively authenticated.
    """
    init_auth_session()
    return st.session_state.get("authenticated", False)
