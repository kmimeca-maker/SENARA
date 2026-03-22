import streamlit as st
from openai import OpenAI
from outscraper import ApiClient
import pandas as pd

# 1. Core System Setup
st.set_page_config(page_title="Senara Elite", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    out_client = ApiClient(api_key=st.secrets["OUTSCRAPER_API_KEY"])
except:
    st.error("Credential Error: Please check your Streamlit Secrets.")

# 2. Studio Minimalist CSS (Strictly Professional)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #ffffff; color: #111827; }
    
    section[data-testid="stSidebar"] { 
        background-color: #f9fafb !important; 
        border-right: 1px solid #e5e7eb; 
    }
    
    textarea, input {
        background-color: #ffffff !important;
        color: #111827 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 4px !important;
    }

    .premium-card {
        background: #ffffff;
        padding: 32px;
        border-radius: 4px;
        border: 1px solid #e5e7eb;
        margin-bottom: 24px;
        color: #111827;
    }
    
    /* Table Styling for AI Output */
    table { width: 100%; border-collapse: collapse; margin-top: 10px; margin-bottom: 20px; }
    th { text-align: left; padding: 12px; border-bottom: 2px solid #e5e7eb; color: #4b5563; }
    td { padding: 12px; border-bottom: 1px solid #e5e7eb; }

    .stTabs [data-baseweb="tab-list"] { gap: 40px; border-bottom: 1px solid #e5e7eb; }
    .stTabs [data-baseweb="tab"] { height: 60px; font-weight: 500; color: #6b7280; border: none !important; }
    .stTabs [data-baseweb="tab--active"] { color: #111827 !important; border-bottom: 2px solid #111827 !important; }

    .stButton>button {
        background-color: #111827;
        color: #ffffff;
        border-radius: 4px;
        padding: 12px 32px;
        border: none;
        width: 100%;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Vault
with st.sidebar:
    st.markdown("### Senara Elite")
    st.markdown("---")
    st.markdown("**Audit Vault**")
    if not st.session_state.history:
        st.caption("No intelligence gathered yet.")
    for item in st.session_state.history:
        st.text(item)

# 4. Main Application Modules
tab1, tab2, tab3 = st.tabs(["Response Engine", "Strategic Audit", "Market Versus"])

with tab2:
    st.markdown("## Strategic Audit")
    st.write("Extract live market data and generate single-business executive reports.")
    url_input = st.text_input("Location URL", placeholder="Paste Google Maps link...", key="single_audit")
    
    if st.button("RUN DIAGNOSTIC", key="btn_audit"):
        if url_input:
            with st.status("Gathering Intelligence...") as status:
                try:
                    data = out_client.google_maps_reviews(url_input, reviews_limit=10, language='en')
                    if data:
                        biz_name = data[0].get('name', 'Business')
                        reviews = [r.get('review_text', '') for r in data[0].get('reviews_data') if r.get('review_text')]
                        
                        ai_res = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{"role":"user", "content": f"Provide a strict, professional audit for {biz_name} based on these reviews: { ' '.join(reviews) }"}]
                        )
                        st.markdown(f"<div class='premium-card'><h3>{biz_name} Report</h3>{ai_res.choices[0].message.content}</div>", unsafe_allow_html=True)
                        if biz_name not in st.session_state.history:
                            st.session_state.history.append(biz_name)
                        status.update(label="Complete", state="complete")
                except Exception as e:
                    st.error(f"Error: {e}")

with tab3:
    st.markdown("## Market Versus")
    st.write("Compare your business directly against a local rival to identify competitive gaps.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        url_a = st.text_input("Primary Business URL", placeholder="https://www.google.com/maps/search/KFC+Morden+London+Road", key="url_a")
    with col_b:
        url_b = st.text_input("Competitor URL", placeholder="
