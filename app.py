import streamlit as st
from openai import OpenAI
from outscraper import ApiClient
import plotly.express as px
import pandas as pd

# 1. Page Config & Brand Identity
st.set_page_config(page_title="Senara Elite", page_icon="💎", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    out_client = ApiClient(api_key=st.secrets["OUTSCRAPER_API_KEY"])
except:
    st.error("Credential Error. Please check your Streamlit Secrets.")

# 2. Premium "Zinc & Slate" Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* Background & Container */
    .stApp { background-color: #fcfcfc; color: #18181b; }
    
    /* Elegant Sidebar */
    section[data-testid="stSidebar"] { 
        background-color: #ffffff !important; 
        border-right: 1px solid #f0f0f0; 
    }
    
    /* Unifying Input Boxes (Fixes the "Ugly" Dark Boxes) */
    textarea, input {
        background-color: #ffffff !important;
        color: #18181b !important;
        border: 1px solid #e4e4e7 !important;
        border-radius: 10px !important;
    }

    /* Soft-UI Card Design */
    .premium-card {
        background: #ffffff;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #f0f0f0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
    }

    /* Professional Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; border-bottom: 1px solid #f0f0f0; }
    .stTabs [data-baseweb="tab"] { 
        height: 50px; 
        font-weight: 600; 
        color: #71717a; 
        border: none !important;
    }
    .stTabs [data-baseweb="tab--active"] { color: #18181b !important; }

    /* Action Buttons */
    .stButton>button {
        background-color: #18181b;
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        border: none;
        font-weight: 600;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #3f3f46; transform: translateY(-1px); }
    </style>
    """, unsafe_allow_html=True)

# 3. Structural Layout
with st.sidebar:
    st.markdown("## 💎 Senara Elite")
    st.caption("Intelligence Protocol v3.0")
    st.markdown("---")
    st.subheader("Audit Archive")
    if not st.session_state.history:
        st.caption("Analysis vault is empty.")
    for item in st.session_state.history:
        st.success(f"📍 {item}")

# 4. Main Tabs
t1, t2, t3 = st.tabs(["🚀 Response Engine", "📊 Strategic Audit", "⚔️ Market Versus"])

with t2:
    st.markdown("## Strategic Business Audit")
    url_input = st.text_input("Enter Google Maps URL", placeholder="https://www.google.com/maps/...")
    
    if st.button("RUN DIAGNOSTIC"):
        if url_input:
            with st.status("📡 Gathering Intelligence...") as status:
                data = out_client.google_maps_reviews(url_input, reviews_limit=20, language='en')
                if data:
                    biz_name = data[0].get('name', 'Business')
                    revs = [r.get('review_text', '') for r in data[0].get('reviews_data') if r.get('review_text')]
                    ratings = [r.get('rating') for r in data[0].get('reviews_data')]
                    
                    # AI Report Logic
                    ai_res = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role":"user", "content": f"Analyze reviews for {biz_name}. Use clean Markdown headers. { ' '.join(revs[:10]) }"}]
                    )
                    report = ai_res.choices[0].message.content
                    
                    if biz_name not in st.session_state.history:
                        st.session_state.history.append(biz_name)
                    
                    status.update(label="✅ Success", state="complete")

                    col1, col2 = st.columns([2, 1], gap="large")
                    with col1:
                        st.markdown(f"<div class='premium-card'><h3>{biz_name} Report</h3>{report}</div>", unsafe_allow_html=True)
                    with col2:
                        st.markdown("<div class='premium-card'><h3>Sentiment Mix</h3>", unsafe_allow_html=True)
                        # Fixed Graph Style
                        df = pd.DataFrame(ratings, columns=['Stars'])
                        fig = px.pie(df, names='Stars', hole=.6, color_discrete_sequence=px.colors.sequential.Greys_r)
                        fig.update_layout(
                            showlegend=False, height=280, margin=dict(t=0, b=0, l=0, r=0),
                            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error("No reviews found for this location.")

with t1:
    st.markdown("## Response Engine")
    st.text_area("Paste Customer Review", height=200, placeholder="Review text goes here...")
    st.button("DRAFT ELITE RESPONSE")

with t3:
    st.markdown("## Market Versus")
    st.info("Side-by-side analysis mode is currently being optimized for high-volume data.")
