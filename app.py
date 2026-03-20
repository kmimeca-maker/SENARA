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

# 2. Studio Minimalist CSS (No Emojis, No Dark Boxes)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    
    /* Clean White Canvas */
    .stApp { background-color: #ffffff; color: #000000; }
    
    /* Sidebar: Fixed & Refined */
    section[data-testid="stSidebar"] { 
        background-color: #fcfcfc !important; 
        border-right: 1px solid #e5e5e5; 
        min-width: 250px !important;
    }
    
    /* Input Fields: Professional Grey Borders */
    textarea, input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 4px !important;
    }

    /* Content Cards */
    .premium-card {
        background: #ffffff;
        padding: 32px;
        border-radius: 4px;
        border: 1px solid #e5e7eb;
        margin-bottom: 24px;
    }

    /* Tab Navigation */
    .stTabs [data-baseweb="tab-list"] { gap: 40px; border-bottom: 1px solid #e5e7eb; }
    .stTabs [data-baseweb="tab"] { 
        height: 60px; 
        font-weight: 500; 
        color: #6b7280; 
        border: none !important;
    }
    .stTabs [data-baseweb="tab--active"] { color: #000000 !important; border-bottom: 2px solid #000000 !important; }

    /* Solid Black Buttons */
    .stButton>button {
        background-color: #000000;
        color: #ffffff;
        border-radius: 4px;
        padding: 12px 32px;
        border: none;
        font-weight: 500;
        letter-spacing: 0.5px;
        transition: opacity 0.2s;
    }
    .stButton>button:hover { opacity: 0.8; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar (Clean Vault)
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
    
    url_input = st.text_input("URL", placeholder="Paste Google Maps link here...")
    
    if st.button("RUN ANALYSIS"):
        if url_input:
            with st.status("Gathering Intelligence...") as status:
                try:
                    data = out_client.google_maps_reviews(url_input, reviews_limit=20, language='en')
                    if data:
                        biz_name = data[0].get('name', 'Business')
                        reviews = [r.get('review_text', '') for r in data[0].get('reviews_data') if r.get('review_text')]
                        ratings = [r.get('rating') for r in data[0].get('reviews_data')]
                        
                        ai_res = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{"role":"user", "content": f"Analyze reviews for {biz_name}. Format with professional headers: Score, Strengths, Weaknesses, and Growth Strategy. { ' '.join(reviews[:10]) }"}]
                        )
                        report = ai_res.choices[0].message.content
                        
                        if biz_name not in st.session_state.history:
                            st.session_state.history.append(biz_name)
                        
                        status.update(label="Complete", state="complete")

                        c1, c2 = st.columns([2, 1], gap="large")
                        with c1:
                            st.markdown(f"<div class='premium-card'><h3>{biz_name} Report</h3>{report}</div>", unsafe_allow_html=True)
                        with c2:
                            st.markdown("<div class='premium-card'><h3>Sentiment Mix</h3>", unsafe_allow_html=True)
                            df = pd.DataFrame(ratings, columns=['Stars'])
                            fig = px.pie(df, names='Stars', hole=.7, color_discrete_sequence=px.colors.sequential.Greys)
                            fig.update_layout(showlegend=False, height=300, paper_bgcolor='rgba(0,0,0,0)')
                            st.plotly_chart(fig, use_container_width=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Analysis failed: {e}")

with tab1:
    st.markdown("## Response Engine")
    st.write("Craft professional, brand-aligned responses to customer feedback.")
    st.text_area("Review Context", height=250, placeholder="Paste customer review here...")
    st.button("GENERATE RESPONSE")

with tab3:
    st.markdown("## Market Versus")
    st.info("Side-by-side analysis mode is currently being optimized for high-volume data.")
