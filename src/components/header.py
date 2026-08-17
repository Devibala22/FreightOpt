"""
Custom App Header Banner Component
Renders a modern, visually striking header for the application.
"""

import streamlit as st
from src.config import APP_TITLE, APP_SUBTITLE

def render_header(module_title: str = "Project Setup", role: str = "Administrator"):
    """
    Renders the custom styled header banner.
    """
    st.markdown(f"""
    <div class="app-header">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <h1>🚛 {APP_TITLE}</h1>
                <p>{APP_SUBTITLE}</p>
            </div>
            <div style="text-align: right;">
                <span class="status-pill status-ok">Module: {module_title}</span>
                <div style="font-size: 0.8rem; color: #93C5FD; margin-top: 6px;">
                    Active Role: <strong>{role}</strong>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
