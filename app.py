import streamlit as st
from openai import OpenAI
from outscraper import ApiClient

# 1. Core Setup & Session Initialization
st.set_page_config(page_title="Senara Elite", layout="wide")

# This MUST come before any sidebar logic to prevent the KeyError
if "history" not in st.session_state:
    st.session_state.history = []

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    out_client = ApiClient(api_key=st.secrets["OUTSCRAPER_API_KEY"])
except:
    st.error("Credential Error: Please verify your Streamlit Secrets.")

# 2. Advanced SaaS Styling (The "Anti-Rookie" Fix)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #ffffff; color: #0f172a; }

    /* Deep Slate Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }
    section[data-testid="stSidebar"] * { color: #f8fafc !important; }

    /* Tactile Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background-color: #f1f5f9;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        font-weight: 700 !important;
        font-size: 14px !important;
        color: #64748b !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0 20px !important;
    }
    .stTabs [data-baseweb="tab--active"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* Premium Analysis Cards */
    .premium-card {
        background: #ffffff;
        padding: 30px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.04);
        margin-top: 20px;
    }

    /* High-Contrast Action Buttons */
    .stButton>button {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        width: 100%;
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background-color: #1e293b !important;
        transform: translateY(-1px);
    }

    /* Clean Input Fields */
    input, textarea {
        border: 2px solid #f1f5f9 !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar (Command Center)
with st.sidebar:
    st.markdown("<h2 style='letter-spacing:-1px;'>SENARA ELITE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='opacity:0.5; font-size:12px;'>Intelligence Protocol v3.0</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Analysis Vault")
    if not st.session_state.history:
        st.caption("No records found.")
    for item in st.session_state.history:
        st.markdown(f"<code style='color:#94a3b8;'>• {item}</code>", unsafe_allow_html=True)

# 4. Main Application
st.markdown("<h1 style='font-weight:800; letter-spacing:-2px; margin-bottom:0px;'>Market Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#64748b; margin-bottom:30px;'>Strategic data-driven competitive analysis.</p>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Response Engine", "Strategic Audit", "Market Versus"])

with tab1:
    st.markdown("### Response Engine")
    st.write("Draft professional, high-retention responses to customer reviews.")
    review_input = st.text_area("Review Context", placeholder="Paste the customer's review here...", height=200)
    if st.button("Generate Elite Response"):
        st.info("AI is drafting a professional response...")

with tab2:
    st.markdown("### Strategic Audit")
    st.write("Full diagnostic report for a single business location.")
    url_audit = st.text_input("Google Maps URL", placeholder="Paste location link here...")
    if st.button("Execute Diagnostic"):
        st.warning("Fetching live market data...")

with tab3:
    st.markdown("### Market Versus")
    st.write("Side-by-side battle report against your top local competitor.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        url_a = st.text_input("Your Business URL", placeholder="Paste your link...", key="v_a")
    with col_b:
        url_b = st.text_input("Competitor URL", placeholder="Paste rival link...", key="v_b")
    
    if st.button("Run Battle Analysis"):
        if url_a and url_b:
            with st.status("Analyzing Market Position...") as s:
                try:
                    data_a = out_client.google_maps_reviews(url_a, reviews_limit=10)
                    data_b = out_client.google_maps_reviews(url_b, reviews_limit=10)
                    
                    name_a = data_a[0].get('name', 'Business A')
                    name_b = data_b[0].get('name', 'Business B')
                    
                    # Store in history
                    if name_a not in st.session_state.history:
                        st.session_state.history.append(name_a)

                    prompt = f"Compare {name_a} vs {name_b}. 1. Create a markdown table for Service, Price, and Quality scores (/10). 2. Add 'Revenue Leakage' section explaining why customers choose B over A. 3. Add 'Executive Summary'."
                    res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                    
                    s.update(label="Intelligence Ready", state="complete")
                    
                    st.markdown(f"#### {name_a} vs {name_b}")
                    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
                    st.markdown(res.choices[0].message.content)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
