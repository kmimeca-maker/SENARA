import streamlit as st
from openai import OpenAI
import re

# 1. Page Config
st.set_page_config(page_title="Senara Intelligence", page_icon="💎", layout="wide")

# --- BRANDED CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0a192f; color: #ccd6f6; }
    h1, h2, h3, p { color: #e6f1ff !important; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #112240; border-right: 1px solid #233554; }
    .stButton>button {
        background-color: #3498db; color: white; border-radius: 4px; border: none;
        width: 100%; padding: 12px; font-weight: 600; transition: all 0.2s ease;
    }
    .stButton>button:hover { background-color: #2980b9; box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3); }
    .stProgress > div > div > div > div { background-color: #3498db; }
    .result-card { background-color: #112240; padding: 20px; border-radius: 10px; border: 1px solid #233554; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Connection
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 3. Sidebar
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #3498db !important;'>💎 SENARA</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.write("Current Status: **Enterprise Ready**")
    st.info("Tip: Use 'Strategic Audit' for high-level business consulting.")

# 4. Tabs
tab1, tab2 = st.tabs(["🚀 Response Engine", "📊 Strategic Audit"])

# --- TAB 1: REPLY GENERATOR ---
with tab1:
    st.markdown("### ⚡ Instant Reply Generator")
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        biz = st.text_input("Business Name", placeholder="Enter store name...")
        rev = st.text_area("Customer Review", height=200, placeholder="Paste a single review...")
        if st.button("GENERATE ELITE RESPONSE"):
            if biz and rev:
                with st.spinner("Processing..."):
                    res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":f"Write a professional response for {biz}: {rev}"}])
                    st.session_state.current_reply = res.choices[0].message.content
    with col2:
        if "current_reply" in st.session_state:
            st.markdown("<div class='result-card'>", unsafe_allow_html=True)
            st.subheader("Final Draft")
            st.code(st.session_state.current_reply, language=None)
            st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 2: BUSINESS AUDITOR ---
with tab2:
    st.markdown("### 📋 Strategic Business Audit")
    
    # --- NEW: DEMO BUTTON ---
    if st.button("📂 Load Sample Review Data"):
        st.session_state.demo_text = """1. The food was cold and the manager didn't care. 1 star.
2. Best pizza in town, but the delivery took 90 minutes.
3. Great atmosphere but the music is way too loud to talk.
4. Staff are friendly but they always run out of the specials by 7pm.
5. Inconsistent quality. One day it's 10/10, next day it's burnt."""
    
    # Using a key to let the button fill the text area
    bulk_input = st.text_area("Bulk Reviews", value=st.session_state.get('demo_text', ''), height=200)
    
    if st.button("RUN FULL DIAGNOSTIC"):
        if bulk_input:
            with st.spinner("Analyzing Intelligence..."):
                prompt = f"Analyze these reviews. Start with 'SCORE: X/10'. Give 3 Pros, 3 Cons, and a CEO Action Plan. Reviews: {bulk_input}"
                res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                report = res.choices[0].message.content
                
                scores = re.findall(r'\d+', report)
                score_num = int(scores[0]) if scores else 5
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Health Score", f"{score_num}/10")
                m2.metric("Sentiment", "Mixed" if score_num < 7 else "Positive")
                m3.metric("Urgency", "High" if score_num < 6 else "Low")
                
                st.progress(score_num/10)
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.markdown(report)
                st.markdown("</div>", unsafe_allow_html=True)
