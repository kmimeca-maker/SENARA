import streamlit as st
from openai import OpenAI
from outscraper import ApiClient
import pandas as pd

# 1. Page Configuration & Initialization
st.set_page_config(page_title="Senara Elite", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []
if "found_rivals" not in st.session_state:
    st.session_state.found_rivals = {}

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    out_client = ApiClient(api_key=st.secrets["OUTSCRAPER_API_KEY"])
except:
    st.error("Credential Error: Please check your Streamlit Secrets.")

# 2. Deep Visual Scan - Professional SaaS Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    
    .stApp { background-color: #f8fafc; color: #0f172a; }

    /* Sidebar Navigation */
    section[data-testid="stSidebar"] { background-color: #0f172a !important; }
    section[data-testid="stSidebar"] * { color: #f8fafc !important; }

    /* Modern Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: #f1f5f9;
        padding: 8px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        font-weight: 700 !important;
        color: #64748b !important;
        border-radius: 8px !important;
        border: none !important;
    }
    .stTabs [data-baseweb="tab--active"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* Result Cards */
    .report-card {
        background: #ffffff;
        padding: 30px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.04);
        margin-top: 20px;
    }

    /* High-Contrast Buttons */
    .stButton>button {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        width: 100%;
        border: none !important;
        height: 48px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.markdown("<h2 style='font-weight:700;'>SENARA ELITE</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("Analysis History")
    for item in st.session_state.history:
        st.markdown(f"• {item}")

# 4. Main UI
st.title("Business Intelligence Dashboard")
st.markdown("Professional market analysis and competitive intelligence.")

tab1, tab2, tab3 = st.tabs(["Review Helper", "Location Audit", "Competitive Intelligence"])

with tab1:
    st.subheader("Review Helper")
    st.text_area("Customer Review:", placeholder="Paste text...", height=150)
    st.button("Draft Response", key="btn_r")

with tab2:
    st.subheader("Location Audit")
    st.text_input("Google Maps Link:", placeholder="Paste link...", key="audit_link")
    st.button("Run Diagnostic", key="btn_d")

with tab3:
    st.subheader("Competitive Intelligence")
    
    # Primary Business Input
    primary_url = st.text_input("Your Business Link", placeholder="Paste your Google Maps link here...", key="p_url")
    st.markdown("---")

    # TWO DISTINCT MODES
    mode = st.radio("Choose Comparison Mode:", ["Radar (Auto-Scout Rivals)", "Market Versus (Manual Link)"], horizontal=True)

    if mode == "Radar (Auto-Scout Rivals)":
        st.write("Automatically find and compare against the top 3 rivals within 1km.")
        if st.button("📡 Start Local Radar"):
            if primary_url:
                with st.status("Scanning market...") as s:
                    try:
                        me = out_client.google_maps_reviews(primary_url, reviews_limit=1)
                        lat, lon = me[0]['latitude'], me[0]['longitude']
                        cat = me[0].get('type', 'Business')
                        rivals = out_client.google_maps_search([f"{cat} near {lat}, {lon}"], limit=5)
                        top_3 = [r for r in rivals[0] if r.get('google_id') != me[0].get('google_id')][:3]
                        st.session_state.found_rivals = {r['name']: r for r in top_3}
                        s.update(label="Rivals Found", state="complete")
                    except Exception as e:
                        st.error(f"Scan Error: {e}")
            else:
                st.warning("Please enter your business link first.")

        if st.session_state.found_rivals:
            # Map View
            m_df = pd.DataFrame([{"lat": r['latitude'], "lon": r['longitude'], "name": r['name']} for r in st.session_state.found_rivals.values()])
            st.map(m_df)
            
            selected_rival = st.selectbox("Select scouted rival:", list(st.session_state.found_rivals.keys()))
            if st.button("Compare with Scouted Rival"):
                rival_id = st.session_state.found_rivals[selected_rival]['google_id']
                rival_link = f"https://www.google.com/maps/search/McDonalds+Morden0:{rival_id}"
                
                with st.status(f"Comparing with {selected_rival}...") as s:
                    d_a = out_client.google_maps_reviews(primary_url, reviews_limit=15)
                    d_b = out_client.google_maps_reviews(rival_link, reviews_limit=15)
                    n_a = d_a[0]['name']
                    if n_a not in st.session_state.history: st.session_state.history.append(n_a)

                    prompt = f"Compare {n_a} vs {selected_rival}. 1. Score table. 2. Revenue leakage (why pick them?). 3. 3-step win plan."
                    res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                    st.markdown(f'<div class="report-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)

    else: # Manual Market Versus Mode
        st.write("Directly compare your business against a specific competitor link.")
        manual_url = st.text_input("Competitor Google Maps Link", placeholder="Paste competitor link here...")
        
        if st.button("Run Market Versus Analysis"):
            if primary_url and manual_url:
                with st.status("Analyzing manual comparison...") as s:
                    try:
                        d_a = out_client.google_maps_reviews(primary_url, reviews_limit=15)
                        d_b = out_client.google_maps_reviews(manual_url, reviews_limit=15)
                        n_a, n_b = d_a[0]['name'], d_b[0]['name']
                        if n_a not in st.session_state.history: st.session_state.history.append(n_a)

                        prompt = f"Compare {n_a} vs {n_b}. 1. Score table. 2. Revenue leakage. 3. 3-step win plan."
                        res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                        st.markdown(f'<div class="report-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")
