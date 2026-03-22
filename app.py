import streamlit as st
from openai import OpenAI
from outscraper import ApiClient
import pandas as pd

# 1. System Setup
st.set_page_config(page_title="Senara Elite", layout="wide")

# Initialize Session State
if "history" not in st.session_state:
    st.session_state.history = []
if "found_rivals" not in st.session_state:
    st.session_state.found_rivals = {}

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    out_client = ApiClient(api_key=st.secrets["OUTSCRAPER_API_KEY"])
except:
    st.error("Credential Error: Please check your Streamlit Secrets.")

# 2. Executive UI Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #ffffff; color: #1f2937; }
    section[data-testid="stSidebar"] { background-color: #111827 !important; }
    section[data-testid="stSidebar"] * { color: #f9fafb !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: #f3f4f6; padding: 8px; border-radius: 10px; }
    .stTabs [data-baseweb="tab--active"] { background-color: #ffffff !important; border-radius: 6px !important; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .result-card { background: #ffffff; padding: 24px; border-radius: 8px; border: 1px solid #e5e7eb; margin-top: 15px; }
    .stButton>button { background-color: #111827 !important; color: #ffffff !important; border-radius: 6px !important; font-weight: 600 !important; width: 100%; border: none !important; height: 45px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.title("Senara Elite")
    st.markdown("---")
    st.subheader("Analysis Vault")
    for item in st.session_state.history:
        st.markdown(f"• {item}")

# 4. Main Dashboard Header
st.title("Business Intelligence Center")
st.markdown("Automated competitive scouting and performance auditing.")

# Define Tabs FIRST to avoid NameErrors
t1, t2, t3 = st.tabs(["Review Helper", "Location Audit", "Competitor Radar"])

with t1:
    st.subheader("Review Helper")
    st.text_area("Paste Review:", height=150)
    st.button("Draft Response")

with t2:
    st.subheader("Location Audit")
    url_audit = st.text_input("Enter Google Maps URL:", key="audit_main")
    if st.button("Run Diagnostic"):
        st.info("Gathering data...")

with t3:
    st.subheader("Competitor Radar")
    
    st.markdown("""
    **Instruction:** Paste your business link below to scan for rivals within a 1km radius.
    """)
    
    u1 = st.text_input("Your Business Link", placeholder="Paste your Google Maps URL...", key="primary_url")
    
    col_scan, col_clear = st.columns([2, 1])
    with col_scan:
        if st.button("📡 Scan 1km Radius"):
            if u1:
                with st.status("Scanning local market...") as status:
                    try:
                        # Get Primary Biz Details
                        my_biz = out_client.google_maps_reviews(u1, reviews_limit=1)
                        lat, lon = my_biz[0].get('latitude'), my_biz[0].get('longitude')
                        category = my_biz[0].get('type', 'Business')
                        
                        # Search nearby
                        search_query = f"{category} near {lat}, {lon}"
                        rivals = out_client.google_maps_search([search_query], limit=10)
                        
                        # Filter to top 3 unique rivals
                        rival_data = []
                        for r in rivals[0]:
                            if r.get('google_id') != my_biz[0].get('google_id') and len(rival_data) < 3:
                                rival_data.append(r)
                        
                        st.session_state.found_rivals = {r['name']: r for r in rival_data}
                        status.update(label="Rivals Identified", state="complete")
                    except Exception as e:
                        st.error(f"Scan Error: {e}")
            else:
                st.warning("Please provide your link first.")

    # Show map and selection if rivals found
    if st.session_state.found_rivals:
        st.markdown("---")
        
        # Map Visual
        map_data = pd.DataFrame([
            {"lat": r['latitude'], "lon": r['longitude'], "name": r['name']}
            for r in st.session_state.found_rivals.values()
        ])
        st.map(map_data)
        
        selected_name = st.selectbox("Select a rival for deep-dive comparison:", list(st.session_state.found_rivals.keys()))
        
        if st.button("Execute Comparison Report"):
            rival = st.session_state.found_rivals[selected_name]
            rival_link = f"https://www.google.com/maps/search/?api=1&query=Google&query_place_id={rival['google_id']}"
            
            with st.status(f"Benchmarking against {selected_name}...") as status:
                d_a = out_client.google_maps_reviews(u1, reviews_limit=15)
                d_b = out_client.google_maps_reviews(rival_link, reviews_limit=15)
                
                n1 = d_a[0]['name']
                if n1 not in st.session_state.history:
                    st.session_state.history.append(n1)

                prompt = f"Compare {n1} vs {selected_name}. 1. Score table for Price, Service, Quality. 2. Revenue Leak analysis (why choose them over you?). 3. 3-step action plan."
                res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                
                status.update(label="Analysis Ready", state="complete")
                st.markdown(f"### Strategy Report: {n1} vs {selected_name}")
                st.markdown(f'<div class="result-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
