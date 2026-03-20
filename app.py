import streamlit as st
from openai import OpenAI
from outscraper import ApiClient
import plotly.express as px
import pandas as pd

# 1. Page Identity
st.set_page_config(page_title="Senara Elite", page_icon="💎", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    out_client = ApiClient(api_key=st.secrets["OUTSCRAPER_API_KEY"])
except:
    st.error("Credential Error. Please check your Streamlit Secrets.")

# 2. Professional "Zinc" Styling (The "Expensive" Look)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* Soft Zinc Background */
    .stApp { background-color: #fafafa; color: #18181b; }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e4e4e7; }
    
    /* Modern Content Cards */
    .premium-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #e4e4e7;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; border-bottom: 1px solid #e4e4e7; }
    .stTabs [data-baseweb="tab"] { font-weight: 600; color: #71717a; }
    .stTabs [data-baseweb="tab--active"] { color: #18181b !important; border-bottom-color: #18181b !important; }

    /* Buttons */
    .stButton>button {
        background-color: #18181b;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1rem;
        transition: 0.2s ease;
    }
    .stButton>button:hover { background-color: #3f3f46; transform: translateY(-1px); }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Intelligence Vault
with st.sidebar:
    st.markdown("## 💎 Senara Elite")
    st.caption("Strategic Intelligence Protocol")
    st.markdown("---")
    st.subheader("Audit Archive")
    if not st.session_state.history:
        st.caption("No intelligence gathered yet.")
    for item in st.session_state.history:
        st.info(f"📍 {item}")

# 4. Interface Logic
t1, t2, t3 = st.tabs(["🚀 Response Engine", "📊 Strategic Audit", "⚔️ Market Versus"])

with t2:
    st.markdown("### 📊 Automated Business Intelligence")
    st.write("Input a Google Maps URL to generate a comprehensive market audit.")
    
    url_input = st.text_input("Location URL", placeholder="Paste Google Maps link here...", label_visibility="collapsed")
    
    if st.button("RUN FULL DIAGNOSTIC"):
        if url_input:
            with st.status("📡 Extracting Data Points...", expanded=True) as status:
                try:
                    data = out_client.google_maps_reviews(url_input, reviews_limit=20, language='en')
                    if data:
                        biz_name = data[0].get('name', 'The Business')
                        reviews_data = data[0].get('reviews_data', [])
                        ratings = [r.get('rating') for r in reviews_data]
                        
                        # AI Synthesis
                        text_for_ai = " ".join([r.get('review_text', '') for r in reviews_data[:12]])
                        ai_res = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{"role": "user", "content": f"You are a professional business consultant. Provide a strategic audit for {biz_name} including a Score/10, Top 3 Strengths, Top 3 Weaknesses, and a 30-day Growth Plan. Input: {text_for_ai}"}]
                        )
                        report = ai_res.choices[0].message.content
                        
                        if biz_name not in st.session_state.history:
                            st.session_state.history.append(biz_name)

                        status.update(label="✅ Analysis Complete", state="complete")

                        # UI Presentation
                        col_left, col_right = st.columns([2, 1], gap="medium")
                        
                        with col_left:
                            st.markdown(f"<div class='premium-card'><h3>🛡️ Executive Report: {biz_name}</h3>{report}</div>", unsafe_allow_html=True)
                        
                        with col_right:
                            st.markdown("<div class='premium-card'><h3>📈 Sentiment Mix</h3>", unsafe_allow_html=True)
                            df = pd.DataFrame(ratings, columns=['Stars'])
                            fig = px.pie(df, names='Stars', hole=.5, color_discrete_sequence=px.colors.sequential.Greys_r)
                            fig.update_layout(showlegend=False, height=250, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)')
                            st.plotly_chart(fig, use_container_width=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                            st.button("📥 EXPORT TO PDF (BETA)")
                    else:
                        st.error("No reviews found. Try a busier location.")
                except Exception as e:
                    st.error(f"System Error: {e}")

with t1:
    st.markdown("### 🚀 Response Engine")
    st.write("Craft professional, brand-aligned responses to customer feedback.")
    st.text_area("Review Context", placeholder="Paste a review here...", height=200)
    st.button("DRAFT ELITE RESPONSE")

with t3:
    st.markdown("### ⚔️ Market Versus")
    st.info("Side-by-side competitive analysis mode is currently being optimized.")
