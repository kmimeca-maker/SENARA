import streamlit as st
from openai import OpenAI
from outscraper import ApiClient
import pandas as pd

# 1. High-Level Configuration
st.set_page_config(page_title="Senara Elite | BI", layout="wide", initial_sidebar_state="expanded")

# Initialize Session States to prevent KeyErrors
if "history" not in st.session_state:
    st.session_state.history = []
if "found_rivals" not in st.session_state:
    st.session_state.found_rivals = {}

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    out_client = ApiClient(api_key=st.secrets["OUTSCRAPER_API_KEY"])
except Exception as e:
    st.error("Configuration Error: Ensure API keys are set in Streamlit Secrets.")

# 2. Deep Visual Overhaul (Professional SaaS Aesthetic)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #fcfcfd; color: #101828; }

    /* Modern Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }
    section[data-testid="stSidebar"] * { color: #f8fafc !important; }

    /* Tab Navigation - Bold & Visible */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f2f4f7;
        padding: 6px;
        border-radius: 10px;
        border: 1px solid #eaecf0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        font-weight: 600 !important;
        color: #667085 !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 0 20px !important;
    }
    .stTabs [data-baseweb="tab--active"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
        box-shadow: 0 1px 3px rgba(16, 24, 40, 0.1);
    }

    /* Professional Content Cards */
    .report-card {
        background: #ffffff;
        padding: 32px;
        border-radius: 12px;
        border: 1px solid #eaecf0;
        box-shadow: 0 4px 6px -1px rgba(16, 24, 40, 0.03);
        margin-top: 20px;
    }

    /* Buttons - Clean High Contrast */
    .stButton>button {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        width: 100%;
        border: none !important;
        height: 48px;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #1e293b !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
    }
    
    /* Input Styling */
    input, textarea {
        border: 1px solid #d0d5dd !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar: Strategic Archive
with st.sidebar:
    st.markdown("<h2 style='font-weight:700;'>SENARA ELITE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='opacity:0.6; font-size:12px;'>Intelligence Protocol v4.0</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("Saved Diagnostics")
    if not st.session_state.history:
        st.caption("No historical data recorded.")
    for item in st.session_state.history:
        st.markdown(f"<code style='color:#94a3b8;'>• {item}</code>", unsafe_allow_html=True)

# 4. Main UI Layout
st.markdown("<h1 style='letter-spacing:-1.5px; font-weight:700;'>Market Intelligence Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#667085; font-size:18px;'>Analyze performance, monitor rivals, and capture market share.</p>", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["💬 Review Helper", "📊 Strategic Audit", "⚔️ Competitive Intelligence"])

with t1:
    st.subheader("Review Response Engine")
    st.write("Generate brand-aligned, professional responses to customer feedback.")
    rev_in = st.text_area("Paste Review Text", placeholder="Input customer feedback here...", height=200)
    if st.button("Generate Professional Draft", key="btn_rev"):
        st.info("AI is analyzing sentiment and drafting response...")

with t2:
    st.subheader("Location Diagnostic")
    st.write("Perform a deep-dive audit of a specific business location's reputation.")
    u_audit = st.text_input("Entity URL (Google Maps)", placeholder="Paste link here...", key="audit_in")
    if st.button("Execute Strategic Audit", key="btn_audit"):
        st.warning("Extracting live market data...")

with t3:
    st.subheader("Competitive Intelligence Suite")
    
    # Combined Mode: Scanner + Manual
    st.markdown("""
    **Intelligence Options:**
    * **Automated Radar:** Paste your link and we will scout rivals within 1km.
    * **Direct Comparison:** Manually input a specific competitor URL.
    """)
    
    primary_url = st.text_input("Your Business URL", placeholder="Paste your Google Maps link...", key="pri_url")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📡 Scan 1km Radius"):
            if primary_url:
                with st.status("Deploying local radar...") as s:
                    try:
                        # Get Primary Data
                        me = out_client.google_maps_reviews(primary_url, reviews_limit=1)
                        lat, lon = me[0]['latitude'], me[0]['longitude']
                        cat = me[0].get('type', 'Business')
                        
                        # Find Rivals
                        query = f"{cat} near {lat}, {lon}"
                        found = out_client.google_maps_search([query], limit=10)
                        
                        # Filter top 3
                        rivals = [r for r in found[0] if r.get('google_id') != me[0].get('google_id')][:3]
                        st.session_state.found_rivals = {r['name']: r for r in rivals}
                        s.update(label="Rivals Detected", state="complete")
                    except Exception as e:
                        st.error(f"Scan Failure: {e}")
            else:
                st.warning("Please provide your link to begin scanning.")

    with c2:
        manual_url = st.text_input("Or Paste Competitor URL Manually", placeholder="Optional rival link...")

    # Display Results Logic
    if st.session_state.found_rivals or manual_url:
        st.markdown("---")
        
        # Determine which rival to compare
        target_name = ""
        target_link = ""
        
        if manual_url:
            target_name = "Manual Competitor"
            target_link = manual_url
        elif st.session_state.found_rivals:
            # Map View for Scouts
            m_data = pd.DataFrame([{"lat": r['latitude'], "lon": r['longitude'], "name": r['name']} for r in st.session_state.found_rivals.values()])
            st.map(m_data)
            
            sel = st.selectbox("Select scouted rival to compare:", list(st.session_state.found_rivals.keys()))
            target_name = sel
            target_link = f"http://googleusercontent.com/maps.google.com/9{st.session_state.found_rivals[sel]['google_id']}"

        if st.button("Generate Comparative Strategy Report"):
            with st.status(f"Benchmarking against {target_name}...") as s:
                try:
                    d_a = out_client.google_maps_reviews(primary_url, reviews_limit=15)
                    d_b = out_client.google_maps_reviews(target_link, reviews_limit=15)
                    
                    n_a = d_a[0]['name']
                    n_b = d_b[0].get('name', target_name)
                    
                    if n_a not in st.session_state.history:
                        st.session_state.history.append(n_a)

                    prompt = f"""
                    Compare {n_a} vs {n_b}.
                    1. Create a table comparing 'Service', 'Price', and 'Quality' (Score 1-10).
                    2. Revenue Impact: Why might customers choose {n_b} over {n_a}?
                    3. Action Plan: 3 immediate steps for {n_a} to improve market position.
                    """
                    
                    res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                    s.update(label="Intelligence Finalized", state="complete")
                    
                    st.markdown(f"### Strategy Report: {n_a} vs {n_b}")
                    st.markdown(f'<div class="report-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Analysis Error: {e}")
