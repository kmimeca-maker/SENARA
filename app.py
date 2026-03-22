import streamlit as st
from openai import OpenAI
from outscraper import ApiClient
import pandas as pd

# 1. Page Configuration & Safety Setup
st.set_page_config(page_title="Senara Elite", layout="wide")

# Initialize State immediately to prevent AttributeErrors
for key in ["history", "found_rivals"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key == "history" else {}

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    out_client = ApiClient(api_key=st.secrets["OUTSCRAPER_API_KEY"])
except:
    st.error("Credential Error: Check your Streamlit Secrets.")

# 2. Clean UI Styling (Fixes hover bugs & rendering)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    
    .stApp { background-color: #f8fafc; color: #0f172a; }
    
    /* Tooltip/Hover Fix */
    [title] { pointer-events: none !important; } 
    button [title] { pointer-events: auto !important; }

    /* Clean Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px; background-color: #f1f5f9; padding: 8px; border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px; font-weight: 700 !important; color: #64748b !important; border: none !important;
    }
    .stTabs [data-baseweb="tab--active"] {
        background-color: #ffffff !important; color: #0f172a !important; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* Result Card */
    .report-card {
        background: #ffffff; padding: 25px; border-radius: 12px; border: 1px solid #e2e8f0; margin-top: 15px;
    }

    .stButton>button {
        background-color: #0f172a !important; color: #ffffff !important; border-radius: 8px !important;
        font-weight: 600 !important; width: 100%; height: 48px; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.markdown("<h2 style='font-weight:700;'>SENARA ELITE</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("Audit History")
    for item in st.session_state.history:
        st.markdown(f"• {item}")

# 4. Main UI
st.title("Business Intelligence Dashboard")

tab1, tab2, tab3 = st.tabs(["Review Helper", "Location Audit", "Competitive Intelligence"])

with tab1:
    st.subheader("Review Helper")
    st.text_area("Paste Review:", placeholder="Paste text...", height=150, key="rev_area")
    st.button("Draft Response", key="btn_reply")

with tab2:
    st.subheader("Location Audit")
    u_audit = st.text_input("Google Maps Link:", placeholder="Paste link...", key="aud_url")
    if st.button("Run Audit"):
        st.info("Fetching data...")

with tab3:
    st.subheader("Competitive Intelligence")
    
    p_url = st.text_input("Your Business Link", placeholder="Paste your Google Maps URL...", key="primary_url")
    st.markdown("---")

    mode = st.radio("Comparison Mode:", ["Radar (Auto-Scout)", "Market Versus (Manual)"], horizontal=True)

    if mode == "Radar (Auto-Scout)":
        if st.button("📡 Start Local Radar"):
            if p_url:
                with st.status("Scanning market...") as s:
                    try:
                        # 1. Get Primary Biz Details with better error handling
                        me = out_client.google_maps_reviews(p_url, reviews_limit=1)
                        if not me or 'latitude' not in me[0]:
                            # Try to get data via search if direct link fails to provide lat/lon
                            me = out_client.google_maps_search([p_url], limit=1)[0]
                        
                        lat = me[0].get('latitude')
                        lon = me[0].get('longitude')
                        cat = me[0].get('type', 'Restaurant')

                        if lat and lon:
                            search_q = f"{cat} near {lat}, {lon}"
                            rivals = out_client.google_maps_search([search_q], limit=5)
                            top_3 = [r for r in rivals[0] if r.get('google_id') != me[0].get('google_id')][:3]
                            st.session_state.found_rivals = {r['name']: r for r in top_3}
                            s.update(label="Rivals Detected", state="complete")
                        else:
                            st.error("Could not determine location coordinates. Try a full Google Maps link.")
                    except Exception as e:
                        st.error(f"Scan Error: {e}")

        if st.session_state.found_rivals:
            m_df = pd.DataFrame([{"lat": r['latitude'], "lon": r['longitude'], "name": r['name']} for r in st.session_state.found_rivals.values()])
            st.map(m_df)
            
            sel = st.selectbox("Select scouted rival:", list(st.session_state.found_rivals.keys()))
            if st.button("Compare with Selected Rival"):
                r_id = st.session_state.found_rivals[sel]['google_id']
                r_link = f"https://www.google.com/maps/search/McDonalds+Morden0:{r_id}"
                
                with st.status(f"Comparing with {sel}...") as s:
                    d_a = out_client.google_maps_reviews(p_url, reviews_limit=15)
                    d_b = out_client.google_maps_reviews(r_link, reviews_limit=15)
                    n_a = d_a[0]['name']
                    if n_a not in st.session_state.history: st.session_state.history.append(n_a)
                    
                    prompt = f"Compare {n_a} vs {sel}. Give 1. Score Table, 2. Revenue Leak analysis, 3. 3-step plan."
                    res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                    st.markdown(f'<div class="report-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)

    else: # Manual Mode
        m_url = st.text_input("Competitor Google Maps Link", placeholder="Paste competitor link...")
        if st.button("Run Manual Comparison"):
            if p_url and m_url:
                with st.status("Analyzing...") as s:
                    try:
                        d_a = out_client.google_maps_reviews(p_url, reviews_limit=15)
                        d_b = out_client.google_maps_reviews(m_url, reviews_limit=15)
                        n_a, n_b = d_a[0]['name'], d_b[0]['name']
                        if n_a not in st.session_state.history: st.session_state.history.append(n_a)
                        
                        prompt = f"Compare {n_a} vs {n_b}. Give 1. Score Table, 2. Revenue Leak, 3. 3-step plan."
                        res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                        st.markdown(f'<div class="report-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Failed: {e}")
