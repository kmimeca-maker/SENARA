import streamlit as st
from openai import OpenAI
import re

# 1. Page Config
st.set_page_config(page_title="Senara Intelligence", page_icon="💎", layout="wide")

# --- UNIFIED BRAND COLOR SCHEME ---
# Primary Color: #3498db (Cobalt Blue)
# Background: #0a192f (Deep Navy)
# Sidebar: #112240 (Slate Navy)

st.markdown("""
    <style>
    /* Main App Background */
    .stApp {
        background-color: #0a192f;
        color: #ccd6f6;
    }
    
    /* Headers & Text */
    h1, h2, h3, p {
        color: #e6f1ff !important;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar Background & Borders */
    [data-testid="stSidebar"] {
        background-color: #112240;
        border-right: 1px solid #233554;
    }

    /* Buttons - The 'Action Blue' */
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 4px;
        border: none;
        width: 100%;
        padding: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #2980b9;
        box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
        transform: translateY(-1px);
    }

    /* Progress Bar Color */
    .stProgress > div > div > div > div {
        background-color: #3498db;
    }

    /* Custom Cards for results */
    .result-card {
        background-color: #112240;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #233554;
        margin-bottom: 20px;
    }
    
    /* Tabs Selection */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        color: #8892b0;
    }
    .stTabs [aria-selected="true"] {
        color: #3498db !important;
        border-bottom-color: #3498db !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Connection
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 3. Sidebar (Branding)
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #3498db !important;'>💎 SENARA</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.8em;'>Elite Reputation Intelligence</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.write("Current Session: **Active**")
    st.write("Model: **GPT-4o Mini**")

# 4. Tabs
tab1, tab2 = st.tabs(["🚀 Response Engine", "📊 Strategic Audit"])

# --- TAB 1: REPLY GENERATOR ---
with tab1:
    st.markdown("### ⚡ Instant Reply Generator")
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        biz = st.text_input("Business Name", placeholder="Enter store name...")
        rev = st.text_area("Customer Review", height=200, placeholder="Paste the text here...")
        generate_btn = st.button("GENERATE ELITE RESPONSE")
        
    with col2:
        if generate_btn and biz and rev:
            with st.spinner("Processing..."):
                res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":f"Write a professional response for {biz}: {rev}"}])
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.subheader("Final Draft")
                st.code(res.choices[0].message.content, language=None)
                st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 2: BUSINESS AUDITOR ---
with tab2:
    st.markdown("### 📋 Strategic Business Audit")
    bulk_input = st.text_area("Bulk Reviews (Paste list)", height=200)
    
    if st.button("RUN FULL DIAGNOSTIC"):
        if bulk_input:
            with st.spinner("Analyzing Intelligence..."):
                prompt = f"Analyze these reviews. Start with 'SCORE: X/10'. Then list PROS, CONS, and ACTION PLAN. Reviews: {bulk_input}"
                res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                report = res.choices[0].message.content
                scores = re.findall(r'\d+', report)
                score_num = int(scores[0]) if scores else 5
                
                # Metrics UI
                m1, m2, m3 = st.columns(3)
                m1.metric("Health Score", f"{score_num}/10")
                m2.metric("Market Sentiment", "Positive" if score_num > 6 else "Critical")
                m3.metric("Urgency", "Low" if score_num > 5 else "High")
                
                st.progress(score_num/10)
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.markdown(report)
                st.markdown("</div>", unsafe_allow_html=True)
