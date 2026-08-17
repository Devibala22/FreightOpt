"""
FreightOpt Configuration & Design System Constants
Centralized settings, color palettes, Tamil Nadu regional metadata, and custom CSS styling.
"""

import streamlit as st

# Application Info
APP_TITLE = "FreightOpt – Smart Freight Infrastructure Planning & Budget Optimization"
APP_SUBTITLE = "Tamil Nadu Logistics Infrastructure & Analytics Portal"
APP_VERSION = "v1.0.0"

# Color Palette (Modern Dark / Glassmorphism Palette)
COLORS = {
    "primary": "#1A56DB",        # Deep Royal Blue
    "primary_light": "#3B82F6",  # Vibrant Indigo-Blue
    "secondary": "#0E9F6E",      # Emerald Green
    "warning": "#F59E0B",        # Amber Warning
    "danger": "#EF4444",         # Coral Red
    "background": "#0F172A",     # Slate 900
    "card_bg": "#1E293B",        # Slate 800
    "text": "#F8FAFC",           # Slate 50
    "text_muted": "#94A3B8",     # Slate 400
    "border": "#334155"          # Slate 700
}

# Tamil Nadu 38 Districts categorized by Economic / Administrative Regions
TN_REGIONS = {
    "North": [
        "Chennai", "Chengalpattu", "Kanchipuram", "Tiruvallur", 
        "Vellore", "Ranipet", "Tirupathur", "Tiruvannamalai"
    ],
    "South": [
        "Madurai", "Dindigul", "Theni", "Ramanathapuram", 
        "Sivaganga", "Virudhunagar", "Tirunelveli", "Tenkasi", 
        "Thoothukudi", "Kanniyakumari"
    ],
    "West": [
        "Coimbatore", "Tiruppur", "Erode", "The Nilgiris", 
        "Salem", "Namakkal", "Dharmapuri", "Krishnagiri"
    ],
    "Central": [
        "Tiruchirappalli", "Karur", "Perambalur", "Ariyalur", 
        "Thanjavur", "Tiruvarur", "Nagapattinam", "Mayiladuthurai", "Pudukkottai"
    ],
    "Coastal": [
        "Cuddalore", "Villupuram", "Kallakurichi"
    ]
}

def apply_custom_css():
    """
    Applies custom CSS for modern typography, high contrast sidebar readability,
    sleek stat cards, and responsive, polished Streamlit components.
    """
    custom_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700&display=swap');

        /* Global Font Setup */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #F8FAFC;
        }

        h1, h2, h3, h4, .title-font {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            color: #F8FAFC;
        }

        /* ------------------------------------------------------------- */
        /* HIGH CONTRAST SIDEBAR STYLING FIX                             */
        /* ------------------------------------------------------------- */
        section[data-testid="stSidebar"] {
            background-color: #0F172A !important;
            border-right: 1px solid #1E293B !important;
        }

        /* Sidebar Headers & Titles */
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3 {
            color: #FFFFFF !important;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
        }

        /* Sidebar Captions & Helper Labels */
        section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
        section[data-testid="stSidebar"] .stMarkdown p {
            color: #CBD5E1 !important;
            font-size: 0.9rem !important;
        }

        /* Widget Labels (User Role & Select Module Labels) */
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
            color: #60A5FA !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            letter-spacing: 0.02em;
        }

        /* Radio Options Items (Module Names) */
        section[data-testid="stSidebar"] div[role="radiogroup"] label {
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(51, 65, 85, 0.5);
            border-radius: 8px;
            padding: 8px 12px !important;
            margin-bottom: 6px !important;
            transition: all 0.2s ease-in-out;
            cursor: pointer;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
            background: rgba(37, 99, 235, 0.2);
            border-color: #3B82F6;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label p {
            color: #F8FAFC !important;
            font-weight: 500 !important;
            font-size: 0.95rem !important;
        }

        /* Selected Radio Highlight */
        section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
            background: linear-gradient(90deg, rgba(37, 99, 235, 0.4) 0%, rgba(30, 41, 59, 0.8) 100%) !important;
            border: 1px solid #3B82F6 !important;
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
        }
        
        section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] p {
            color: #60A5FA !important;
            font-weight: 700 !important;
        }

        /* Select Box Styling */
        section[data-testid="stSidebar"] div[data-baseweb="select"] {
            background-color: #1E293B !important;
            border-radius: 8px !important;
            border: 1px solid #334155 !important;
        }

        section[data-testid="stSidebar"] div[data-baseweb="select"] * {
            color: #F8FAFC !important;
        }

        /* High Contrast Tabs Styling */
        button[data-baseweb="tab"] {
            background-color: rgba(30, 41, 59, 0.6) !important;
            border: 1px solid #334155 !important;
            border-radius: 8px 8px 0 0 !important;
            padding: 10px 20px !important;
            margin-right: 4px !important;
        }

        button[data-baseweb="tab"] div[data-testid="stMarkdownContainer"] p {
            color: #CBD5E1 !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            background-color: #1E3A8A !important;
            border: 1px solid #3B82F6 !important;
            border-bottom: none !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] div[data-testid="stMarkdownContainer"] p {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }

        /* ------------------------------------------------------------- */
        /* MAIN BODY & CARDS STYLING                                     */
        /* ------------------------------------------------------------- */
        
        /* Gradient Stat Cards */
        .metric-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
            border: 1px solid rgba(51, 65, 85, 0.8);
            border-radius: 14px;
            padding: 20px 24px;
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.25);
            backdrop-filter: blur(12px);
            margin-bottom: 15px;
            transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-3px);
            border-color: #3B82F6;
            box-shadow: 0 8px 30px rgba(59, 130, 246, 0.25);
        }

        .metric-label {
            font-size: 0.85rem;
            color: #94A3B8;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 6px;
        }

        .metric-value {
            font-size: 2rem;
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            color: #F8FAFC;
        }

        .metric-badge {
            display: inline-block;
            padding: 4px 10px;
            font-size: 0.78rem;
            font-weight: 600;
            border-radius: 6px;
            margin-top: 8px;
        }

        .badge-green { background-color: rgba(14, 159, 110, 0.25); color: #34D399; border: 1px solid rgba(14, 159, 110, 0.4); }
        .badge-amber { background-color: rgba(245, 158, 11, 0.25); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.4); }
        .badge-red { background-color: rgba(239, 68, 68, 0.25); color: #FCA5A5; border: 1px solid rgba(239, 68, 68, 0.4); }
        .badge-blue { background-color: rgba(59, 130, 246, 0.25); color: #60A5FA; border: 1px solid rgba(59, 130, 246, 0.4); }

        /* Custom Header Styling */
        .app-header {
            background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%);
            padding: 26px 32px;
            border-radius: 16px;
            border: 1px solid #2563EB;
            color: white;
            margin-bottom: 25px;
            box-shadow: 0 12px 30px -5px rgba(30, 58, 138, 0.5);
        }

        .app-header h1 {
            color: #FFFFFF !important;
            margin: 0;
            font-size: 2.1rem;
            letter-spacing: -0.02em;
        }

        .app-header p {
            color: #93C5FD !important;
            margin: 6px 0 0 0;
            font-size: 1.05rem;
        }

        /* Status Pills */
        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .status-ok { background: rgba(14, 159, 110, 0.2); color: #34D399; border: 1px solid rgba(14, 159, 110, 0.5); }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
