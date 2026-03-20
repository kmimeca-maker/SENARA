import streamlit as st
from openai import OpenAI
from outscraper import ApiClient
import plotly.express as px
import pandas as pd

# 1. Core Setup
st.set_page_config(page_title="Senara Elite", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    out_client = ApiClient(api_key=st.secrets["OUTSCRAPER_API_KEY"])
except:
    st.error("Credential Error: Please check your Streamlit Secrets.")

# 2. Studio Minimalist CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #ffffff; color: #000000; }
    
    /* Sidebar Fix */
    section[data-testid="stSidebar"] { 
        background-color: #fcfcfc !important; 
        border-right: 1px solid #e5e5e5; 
    }
    
    /* Input Fields */
    textarea, input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 4px !important;
    }

    /* Cards & Tabs */
    .premium-card {
        background: #ffffff;
        padding: 32px;
        border-radius: 4px;
        border: 1px solid #e5e7eb;
        margin-bottom: 24px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 40px; border-bottom: 1px solid #e5e7eb; }
    .stTabs [data-baseweb="tab"] { height: 60px; font-weight: 500; color: #6b7280; border: none !important; }
    .stTabs [data-baseweb="tab--active"] { color: #000000 !important; border-bottom: 2px solid #000000 !important; }

    /* Button */
    .stButton>button {
        background-color: #000000;
        color: #ffffff;
        border-radius: 4px;
        padding: 12px 32px;
        border: none;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.markdown("### Senara Elite")
    st.markdown("---")
    st.markdown("**Audit Vault**")
    if not st.session_state.history:
        st.caption("No records found.")
    for item in st.session_state.history:
        st.text(f"• {item}")

# 4. Main Application
tab1, tab2, tab3 = st.tabs(["Response Engine", "Strategic Audit", "Market Versus"])

with tab2:
    st.markdown("## Strategic Audit")
    st.write("Extract live market data and generate executive reports.")
    url_input = st.text_input("URL", placeholder="Paste Google Maps link here...", key="single_audit")
    if st.button("RUN ANALYSIS"):
        if url_input:
            with st.status("Gathering Intelligence...") as status:
                data = out_client.google_maps_reviews(url_input, reviews_limit=10, language='en')
                if data:
                    biz_name = data[0].get('name', 'Business')
                    reviews = [r.get('review_text', '') for r in data[0].get('reviews_data') if r.get('review_text')]
                    ai_res = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role":"user", "content": f"Brief audit for {biz_name}: { ' '.join(reviews) }"}]
                    )
                    st.markdown(f"<div class='premium-card'> {ai_res.choices[0].message.content} </div>", unsafe_allow_html=True)
                    if biz_name not in st.session_state.history:
                        st.session_state.history.append(biz_name)
                    status.update(label="Complete", state="complete")

with tab3:
    st.markdown("## Market Versus")
    st.write("Compare two businesses side-by-side to identify competitive advantages.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        url_a = st.text_input("Primary Business URL", placeholder="Paste first Google Maps link...", key="url_a")
    with col_b:
        url_b = st.text_input("Competitor URL", placeholder="Paste second Google Maps link...", key="url_b")
    
    if st.button("EXECUTE COMPETITIVE COMPARISON"):
        if url_a and url_b:
            with st.status("Interrogating Competitor Data...") as status:
                # Scrape both
                data_a = out_client.google_maps_reviews(url_a, reviews_limit=10, language='en')
                data_b = out_client.google_maps_reviews(url_b, reviews_limit=10, language='en')
                
                if data_a and data_b:
                    name_a = data_a[0].get('name', 'Business A')
                    name_b = data_b[0].get('name', 'Business B')
                    
                    revs_a = " ".join([r.get('review_text', '') for r in data_a[0].get('reviews_data') if r.get('review_text')])
                    revs_b = " ".join([r.get('review_text', '') for r in data_b[0].get('reviews_data') if r.get('review_text')])
                    
                    # AI Comparison
                    compare_prompt = f"Compare {name_a} vs {name_b}. Who is winning in service? Who has better value? Give a winner for each category and a final recommendation for {name_a} to beat {name_b}. Data A: {revs_a} | Data B: {revs_b}"
                    
                    res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": compare_prompt}])
                    
                    status.update(label="Intelligence Synced", state="complete")
                    st.markdown(f"<div class='premium-card'><h3>Battle Report: {name_a} vs {name_b}</h3>{res.choices[0].message.content}</div>", unsafe_allow_html
