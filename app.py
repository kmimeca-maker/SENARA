import streamlit as st
from openai import OpenAI
import re

# 1. Page Config & Professional Theme
st.set_page_config(page_title="Senara Elite", page_icon="💎", layout="wide")

# --- CUSTOM CSS (This makes it look high-quality) ---
st.markdown("""
    <style>
    /* Change background and font */
    .stApp {
        background-color: #0e1117;
    }
    h1, h2, h3 {
        color: #ffffff !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    /* Style the buttons */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        transition: 0.3s;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
    }
    /* Style the cards/boxes */
    div.stCodeBlock {
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    /* Style the sidebar */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Connection
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 3. Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3176/3176392.png", width=50) # A small logo
    st.title("Senara Intelligence")
    st.write("Retire the stress of management.")
    st.markdown("---")
    st.caption("Version 2.4 Gold")

# 4. Tabs
tab1, tab2 = st.tabs(["🚀 Response Engine", "📊 Strategic Audit"])

# --- TAB 1: REPLY GENERATOR ---
with tab1:
    st.title("Instant Reply Generator")
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        biz = st.text_input("Business Name", placeholder="e.g. Senara Bistro")
        rev = st.text_area("Paste Review", height=200)
        generate_btn = st.button("✨ Craft Response")
        
    with col2:
        if generate_btn:
            if biz and rev:
                with st.spinner("AI is writing..."):
                    res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":f"Reply to this for {biz}: {rev}"}])
                    answer = res.choices[0].message.content
                    st.success("Draft Ready")
                    st.code(answer, language=None)
            else:
                st.warning("Please fill out both fields.")

# --- TAB 2: BUSINESS AUDITOR ---
with tab2:
    st.title("Strategic Business Audit")
    st.write("Analyze patterns across multiple reviews.")
    bulk_input = st.text_area("Paste 5+ Reviews here", height=250)
    
    if st.button("📈 Run Full Diagnostic"):
        if bulk_input:
            with st.spinner("Analyzing Business Health..."):
                prompt = f"Analyze these reviews. Start your response with 'SCORE: X/10'. Then list PROS, CONS, and a 1-sentence ACTION PLAN. Reviews: {bulk_input}"
                res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                report = res.choices[0].message.content
                
                # Safety Score Logic
                scores = re.findall(r'\d+', report)
                score_num = int(scores[0]) if scores else 5
                
                # UI Layout for Audit
                c1, c2, c3 = st.columns(3)
                c1.metric("Trust Score", f"{score_num}/10")
                c2.metric("Market Sentiment", "Positive" if score_num > 6 else "Neutral")
                c3.metric("Urgency", "Low" if score_num > 5 else "High")
                
                st.progress(score_num/10)
                st.markdown("---")
                st.markdown(report)
