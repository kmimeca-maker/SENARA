import streamlit as st
from openai import OpenAI
from outscraper import ApiClient

# 1. System Initialization
st.set_page_config(page_title="Senara Elite | Strategic Intelligence", layout="wide")

# Critical Fix: Initialize state before any sidebar or logic execution
if "history" not in st.session_state:
    st.session_state.history = []

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    out_client = ApiClient(api_key=st.secrets["OUTSCRAPER_API_KEY"])
except:
    st.error("Credential Error: Please verify your Streamlit Secrets.")

# 2. Executive UI Styling (High-Contrast / Professional)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #ffffff; color: #1e293b; }

    /* Professional Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }
    section[data-testid="stSidebar"] * { color: #f1f5f9 !important; }

    /* Navigation: Clean & Focused */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background-color: #f8fafc;
        padding: 8px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        font-weight: 600 !important;
        font-size: 14px !important;
        color: #64748b !important;
        border: none !important;
    }
    .stTabs [data-baseweb="tab--active"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border-radius: 6px !important;
    }

    /* Executive Report Cards */
    .report-card {
        background: #ffffff;
        padding: 35px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-top: 25px;
    }

    /* Action Buttons */
    .stButton>button {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border-radius: 6px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        width: 100%;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar: Strategic Archive
with st.sidebar:
    st.markdown("<h2 style='font-weight:700;'>SENARA ELITE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='opacity:0.6; font-size:13px;'>Intelligence Protocol v3.0</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Strategic Archive")
    if not st.session_state.history:
        st.caption("No historical data available.")
    for item in st.session_state.history:
        st.markdown(f"<p style='font-size:13px; color:#94a3b8;'>• {item}</p>", unsafe_allow_html=True)

# 4. Dashboard Header
st.markdown("<h1 style='font-weight:700; letter-spacing:-1.5px; margin-bottom:0;'>Market Intelligence Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#64748b; margin-bottom:35px;'>Quantitative analysis and competitive displacement strategies.</p>", unsafe_allow_html=True)

# 5. Operational Modules
tab1, tab2, tab3 = st.tabs(["Response Management", "Location Diagnostic", "Competitive Benchmarking"])

with tab1:
    st.markdown("### Response Management")
    st.write("Generate brand-aligned executive communications for customer feedback.")
    review_input = st.text_area("Review Context", placeholder="Insert review text...", height=180)
    if st.button("Generate Executive Response"):
        st.info("System is drafting a professional alignment...")

with tab2:
    st.markdown("### Location Diagnostic")
    st.write("Perform a deep-dive audit of specific operational performance data.")
    url_audit = st.text_input("Entity URL (Google Maps)", placeholder="Paste link...")
    if st.button("Execute Diagnostic"):
        st.warning("Extracting market data for analysis...")

with tab3:
    st.markdown("### Competitive Benchmarking")
    st.write("Direct side-by-side performance analysis between Primary Entity and Market Rival.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        url_a = st.text_input("Primary Entity URL", placeholder="Your link...", key="v_a")
    with col_b:
        url_b = st.text_input("Competitor Entity URL", placeholder="Rival link...", key="v_b")
    
    if st.button("Execute Benchmarking Analysis"):
        if url_a and url_b:
            with st.status("Analyzing Market Displacement...") as s:
                try:
                    data_a = out_client.google_maps_reviews(url_a, reviews_limit=15)
                    data_b = out_client.google_maps_reviews(url_b, reviews_limit=15)
                    
                    name_a = data_a[0].get('name', 'Primary')
                    name_b = data_b[0].get('name', 'Competitor')
                    
                    if name_a not in st.session_state.history:
                        st.session_state.history.append(name_a)

                    # Serious, Structured Business Prompt
                    prompt = f"""
                    Perform a professional competitive analysis between {name_a} and {name_b}.
                    Output requirements:
                    1. A Table comparing 'Value Proposition', 'Service Efficiency', and 'Product Quality' (Weighted Score /10).
                    2. Section 'Market Displacement Risk': Identify exactly why customers are migrating to {name_b}.
                    3. Section 'Strategic Recommendations': Provide two high-impact operational changes for {name_a}.
                    """
                    
                    res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                    
                    s.update(label="Analysis Finalized", state="complete")
                    
                    st.markdown(f"#### Comparative Report: {name_a} vs {name_b}")
                    st.markdown('<div class="report-card">', unsafe_allow_html=True)
                    st.markdown(res.choices[0].message.content)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Intelligence Failure: {e}")
