import streamlit as st
from openai import OpenAI
import re

# 1. Config
st.set_page_config(page_title="Senara Elite", page_icon="💎", layout="wide")

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
    .result-card { background-color: #112240; padding: 20px; border-radius: 10px; border: 1px solid #233554; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 2. Sidebar
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #3498db !important;'>💎 SENARA</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.write("Mode: **Full Suite Active**")

# 3. Tabs
tab1, tab2, tab3 = st.tabs(["🚀 Response Engine", "📊 Strategic Audit", "⚔️ Market Versus"])

# --- TAB 1: RESPONSE ENGINE ---
with tab1:
    st.markdown("### ⚡ Instant Reply Generator")
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        biz = st.text_input("Business Name", placeholder="Enter store name...", key="t1_biz")
        rev = st.text_area("Customer Review", height=200, placeholder="Paste a single review...", key="t1_rev")
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

# --- TAB 2: STRATEGIC AUDIT ---
with tab2:
    st.markdown("### 📋 Strategic Business Audit")
    if st.button("📂 Load Sample Review Data"):
        st.session_state.demo_text = "1. Cold food. 2. Great service. 3. Too loud. 4. Expensive but worth it. 5. Slow drinks."
    
    bulk_input = st.text_area("Bulk Reviews", value=st.session_state.get('demo_text', ''), height=200, key="t2_bulk")
    
    if st.button("RUN FULL DIAGNOSTIC"):
        if bulk_input:
            with st.spinner("Analyzing..."):
                prompt = f"Analyze these reviews. SCORE: X/10, PROS, CONS, ACTION PLAN. Reviews: {bulk_input}"
                res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                report = res.choices[0].message.content
                scores = re.findall(r'\d+', report)
                score_num = int(scores[0]) if scores else 5
                st.metric("Health Score", f"{score_num}/10")
                st.progress(score_num/10)
                st.markdown(f"<div class='result-card'>{report}</div>", unsafe_allow_html=True)

# --- TAB 3: MARKET VERSUS ---
with tab3:
    st.markdown("### ⚔️ Competitive Battle Report")
    c_a, c_b = st.columns(2)
    with c_a:
        my_biz = st.text_input("My Shop", key="t3_my_biz")
        my_revs = st.text_area("My Reviews", height=150, key="t3_my_revs")
    with c_b:
        rival_biz = st.text_input("Rival Shop", key="t3_rival_biz")
        rival_revs = st.text_area("Rival Reviews", height=150, key="t3_rival_revs")

    if st.button("🚀 EXECUTE BATTLE ANALYSIS"):
        if my_revs and rival_revs:
            with st.spinner("Analyzing Competition..."):
                prompt = f"Compare {my_biz} (My Reviews: {my_revs}) vs {rival_biz} (Rival Reviews: {rival_revs}). Who wins and why?"
                res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                st.markdown(f"<div class='result-card'>{res.choices[0].message.content}</div>", unsafe_allow_html=True)
