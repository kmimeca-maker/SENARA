import streamlit as st
from openai import OpenAI
from outscraper import ApiClient

# 1. System Setup
st.set_page_config(page_title="Senara Elite", layout="wide")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    out_client = ApiClient(api_key=st.secrets["OUTSCRAPER_API_KEY"])
except:
    st.error("Credential Error: Please verify your Streamlit Secrets.")

# 2. Advanced "SaaS" UI Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* Typography & Background */
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #ffffff; color: #111827; }

    /* The Sidebar: Dark Professional Slate */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        color: #f8fafc !important;
        border-right: 1px solid #1e293b;
    }
    section[data-testid="stSidebar"] * { color: #f8fafc !important; }

    /* The Tabs: Making them Bold & Visible */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: #f8fafc;
        padding: 10px 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        font-weight: 800 !important; /* Extra Bold */
        font-size: 16px !important;
        color: #64748b !important;
        border: none !important;
        transition: all 0.3s;
    }
    .stTabs [data-baseweb="tab--active"] {
        color: #0f172a !important;
        border-bottom: 3px solid #0f172a !important;
    }

    /* Premium Content Cards */
    .premium-card {
        background: #ffffff;
        padding: 40px;
        border-radius: 16px;
        border: 1px solid #f1f5f9;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        margin-top: 25px;
    }

    /* Action Buttons: High Contrast Black */
    .stButton>button {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        padding: 14px 28px !important;
        font-weight: 600 !important;
        border: none !important;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stButton>button:hover {
        background-color: #1e293b !important;
        transform: translateY(-1px);
    }

    /* Inputs */
    input, textarea {
        border: 2px solid #f1f5f9 !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }
    input:focus { border-color: #0f172a !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.markdown("<h1 style='font-weight:800; font-size: 24px;'>SENARA ELITE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='opacity:0.6;'>Strategic Intelligence v3.0</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Analysis Vault")
    if not st.session_state.history:
        st.caption("No intelligence gathered yet.")

# 4. Main App
st.markdown("<h1 style='font-weight:800; letter-spacing:-1px;'>Intelligence Center</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🚀 Response Engine", "📊 Strategic Audit", "⚔️ Market Versus"])

# ... rest of your tab logic (copy from previous version) ...
