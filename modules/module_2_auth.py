"""
Module 2: Authentication UI
Independently runnable module for user authentication, role-based login,
new user registration with auto-session activation, and active profile management.
"""

import sys
import os
import streamlit as st

# Ensure parent root is in Python path for standalone execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.config import apply_custom_css
from src.components.header import render_header
from src.logic.auth import (
    init_auth_session, is_authenticated, get_current_user,
    authenticate, login_user, logout_user
)
from src.database.auth_repository import create_user

def run_module_2(role: str = "Administrator"):
    """
    Executes Module 2 Authentication UI workflows.
    """
    apply_custom_css()
    init_auth_session()
    
    current_user = get_current_user()
    active_role = current_user["role"] if current_user else role
    
    render_header(module_title="Module 2: Authentication UI", role=active_role)

    st.markdown("### 🔐 Identity & Role-Based Access Control")
    
    # -------------------------------------------------------------
    # VIEW 1: AUTHENTICATED USER PROFILE CARD (ACTIVE SESSION)
    # -------------------------------------------------------------
    if is_authenticated() and current_user:
        st.balloons()
        st.success(f"🎉 **Active Session**: Welcome, **{current_user['full_name']}** ({current_user['role']})")
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border: 2px solid #3B82F6; border-radius: 16px; padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.4); margin-bottom: 25px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                <div>
                    <span class="badge-green" style="font-size: 0.85rem; padding: 5px 14px;">🟢 SESSION ACTIVE & LOGGED IN</span>
                    <h2 style="color: #FFFFFF !important; margin: 12px 0 4px 0;">👤 {current_user['full_name']}</h2>
                    <p style="color: #93C5FD !important; margin: 0; font-size: 0.98rem;">📧 Email: <strong>{current_user['email']}</strong> &nbsp;|&nbsp; 🏛️ Dept: <strong>{current_user['department']}</strong></p>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.85rem; color: #94A3B8;">AUTHORIZED ROLE</div>
                    <div style="font-size: 1.3rem; font-weight: 700; color: #34D399;">{current_user['role']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_actions1, col_actions2 = st.columns([3, 1])
        with col_actions1:
            st.info(f"💡 **Logged in as {current_user['role']}**: You can now navigate to **Module 3: Dashboard**, **Module 4: Project Input**, or **Module 5: GIS Map**.")
        with col_actions2:
            if st.button("🚪 Logout of Account", use_container_width=True, type="primary"):
                logout_user()
                st.toast("Logged out successfully.", icon="ℹ️")
                st.rerun()

    # -------------------------------------------------------------
    # VIEW 2: LOGIN / REGISTER FORMS
    # -------------------------------------------------------------
    else:
        # Credentials Reference Banner
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.9); border: 1px solid #3B82F6; border-radius: 12px; padding: 16px 20px; margin-bottom: 20px;">
            <div style="color: #60A5FA; font-weight: 700; font-size: 0.95rem; margin-bottom: 8px;">🔑 Official Demo Credentials Reference</div>
            <div style="display: flex; gap: 20px; flex-wrap: wrap; font-size: 0.88rem; color: #E2E8F0;">
                <div style="background: #0F172A; padding: 10px 14px; border-radius: 8px; border: 1px solid #334155; flex: 1; min-width: 250px;">
                    <strong style="color: #34D399;">👑 Administrator Role:</strong><br>
                    • Email: <code style="color: #60A5FA;">admin@tnlogistics.gov.in</code><br>
                    • Password: <code style="color: #FBBF24;">Admin@123</code>
                </div>
                <div style="background: #0F172A; padding: 10px 14px; border-radius: 8px; border: 1px solid #334155; flex: 1; min-width: 250px;">
                    <strong style="color: #60A5FA;">📐 Decision Maker (Planner) Role:</strong><br>
                    • Email: <code style="color: #60A5FA;">planner@tnlogistics.gov.in</code><br>
                    • Password: <code style="color: #FBBF24;">Planner@123</code>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Tab Navigation (High Contrast Styled)
        tab_login, tab_register = st.tabs([
            "🔒 Tab 1: Secure User Login", 
            "📝 Tab 2: Register New Government Account"
        ])

        # TAB 1: LOGIN FORM
        with tab_login:
            st.subheader("Login to Your FreightOpt Account")
            
            with st.form("login_form"):
                email_input = st.text_input(
                    "Official Email Address", 
                    value="", 
                    placeholder="Enter email (e.g. devi@tn.gov.in or planner@tnlogistics.gov.in)"
                )
                password_input = st.text_input(
                    "Password", 
                    value="", 
                    type="password", 
                    placeholder="Enter password"
                )
                submit_login = st.form_submit_button("Sign In to Account", type="primary", use_container_width=True)

                if submit_login:
                    if not email_input or not password_input:
                        st.error("Please enter both email and password.")
                    else:
                        user = authenticate(email_input, password_input)
                        if user:
                            login_user(user)
                            st.success(f"Authentication successful! Welcome, {user['full_name']}.")
                            st.rerun()
                        else:
                            st.error("Invalid email or password. Please check credentials or register under Tab 2.")

        # TAB 2: REGISTER FORM
        with tab_register:
            st.subheader("Register a New Government Account")
            st.caption("Once registered, your session will automatically log you in.")

            with st.form("register_form"):
                reg_name = st.text_input("Full Name", placeholder="e.g. Devi")
                reg_email = st.text_input("Official Email Address", placeholder="devi@tn.gov.in")
                reg_pwd = st.text_input("Account Password", type="password", placeholder="devi@123")
                reg_dept = st.text_input("Department / Board", placeholder="e.g. Supply Chain & Logistics Board")
                reg_role = st.selectbox(
                    "Select Account Role:",
                    options=["Decision Maker (Government Planner)", "Administrator"]
                )
                submit_reg = st.form_submit_button("Create Account & Auto-Login", type="primary", use_container_width=True)

                if submit_reg:
                    if not reg_name or not reg_email or not reg_pwd or not reg_dept:
                        st.error("All registration fields are required.")
                    else:
                        try:
                            new_user = create_user(
                                email=reg_email,
                                password=reg_pwd,
                                full_name=reg_name,
                                role=reg_role,
                                department=reg_dept
                            )
                            # Auto-login newly registered user!
                            login_user(new_user)
                            st.toast(f"Account for {reg_name} created successfully!", icon="🎉")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Registration failed: {str(e)}")

    st.success("✅ **Module 2 Authentication UI Operational**: Multi-tab login, registration, and active session manager ready.")

if __name__ == "__main__":
    st.set_page_config(
        page_title="FreightOpt - Module 2 Authentication UI",
        page_icon="🔐",
        layout="wide"
    )
    run_module_2()
