import streamlit as st
from openai import OpenAI
from outscraper import ApiClient
import plotly.express as px
import pandas as pd

# 1. Setup & High-End Minimalist Theme
st.set_page_config(page_title="Senara Elite", page_icon="✨", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    out_client = ApiClient(api_key=st.secrets["OUTSCRAPER_API_KEY"])
except Exception as e:
    st.error("API Keys missing in Secrets. Please check Streamlit settings.")

# 2. Modern UI Styling (Soft Greys & Professional Type)
st.markdown("""
    <style>
    .stApp { background-color: #f9fafb; color: #111827; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 8px;
        padding: 10px 20px;
        border: 1px solid #e5e7eb;
    }
    .report-card {
        background: white;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #f3f4f6;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #111827;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.title("💎 Senara")
    st.markdown("### Analysis Vault")
    for item in st.session_state.history:
        st.info(f"📍 {item}")

# 4. Main App Logic
tab1, tab2, tab3 = st.tabs(["🚀 Response Engine", "📊 Strategic Audit", "⚔️ Market Versus"])

with tab1:
    st.subheader("AI Response Agent")
    rev_text = st.text_area("Customer Review", placeholder="Paste here...", height=150)
    if st.button("Generate Elite Response"):
        if rev_text:
            res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": f"Write a professional response: {rev_text}"}])
            st.markdown(f"<div class='report-card'>{res.choices[0].message.content}</div>", unsafe_allow_html=True)

with tab2:
    st.subheader("Automated Intelligence")
    url_input = st.text_input("Google Maps URL", placeholder="Paste link here...")
    
    if st.button("EXECUTE AUDIT"):
        if url_input:
            with st.status("📡 Intercepting Data...") as status:
                try:
                    data = out_client.google_maps_reviews(url_input, reviews_limit=20, language='en')
                    if data:
                        biz_name = data[0].get('name', 'Business')
                        reviews = [r.get('review_text', '') for r in data[0].get('reviews_data') if r.get('review_text')]
                        ratings = [r.get('rating') for r in data[0].get('reviews_data')]
                        
                        # AI Report
                        ai_res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":f"Audit this: {' '.join(reviews[:10])}"}])
                        report = ai_res.choices[0].message.content
                        
                        if biz_name not in st.session_state.history:
                            st.session_state.history.append(biz_name)

                        status.update(label="✅ Success", state="complete")
                        
                        c1, c2 = st.columns([2, 1])
                        with c1:
                            st.markdown(f"<div class='report-card'><h3>{biz_name} Report</h3>{report}</div>", unsafe_allow_html=True)
                        with c2:
                            st.markdown("<div class='report-card'>", unsafe_allow_html=True)
                            df = pd.DataFrame(ratings, columns=['Stars'])
                            fig = px.pie(df, names='Stars', hole=.4, title="Sentiment Mix", color_discrete_sequence=px.colors.sequential.RdBu)
                            fig.update_layout(showlegend=False, height=300)
                            st.plotly_chart(fig, use_container_width=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.error("No reviews found for this link.")
                except Exception as e:
                    st.error(f"Error: {e}")

with tab3:
    st.subheader("Competitive Analysis")
    st.write("Compare two businesses side by side.")
    col_a, col_b = st.columns(2)
    with col_a:
        st.text_area("Your Business Reviews", height=200)
    with col_b:
        st.text_area("Rival Business Reviews", height=200)
    st.button("Compare Competitors")
