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
    .vs-tag { background-color: #e74c3c; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 3. Sidebar
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #3498db !important;'>💎 SENARA</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.write("Mode: **Competitive Intel**")

# 4. Tabs
tab1, tab2, tab3 = st.tabs(["🚀 Response Engine", "📊 Strategic Audit", "⚔️ Market Versus"])

# (Tab 1 & 2 stay the same, but let's look at the NEW Tab 3)

with tab1:
    st.markdown("### ⚡ Response Engine")
    # ... (Your existing Response Engine code goes here)

with tab2:
    st.markdown("### 📋 Strategic Audit")
    # ... (Your existing Audit code goes here)

with tab3:
    st.markdown("### ⚔️ Competitive Battle Report")
    st.write("Compare your business directly against your local rival.")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Your Business")
        my_biz = st.text_input("My Shop Name", placeholder="e.g. KFC Morden")
        my_revs = st.text_area("Your Reviews", height=150, key="my_revs")
        
    with col_b:
        st.subheader("The Competitor")
        rival_biz = st.text_input("Rival Shop Name", placeholder="e.g. Burger King")
        rival_revs = st.text_area("Rival Reviews", height=150, key="rival_revs")

    if st.button("🚀 EXECUTE BATTLE ANALYSIS"):
        if my_revs and rival_revs:
            with st.spinner("Crunching Competitive Data..."):
                prompt = f"""Compare {my_biz} and {rival_biz}. 
                Format:
                WINNER: [Name]
                WHY: [1 sentence]
                YOUR EDGE: [What you do better]
                THEIR EDGE: [What they do better]
                KILLER MOVE: [One thing you should do to steal their customers]
                
                My Reviews: {my_revs}
                Rival Reviews: {rival_revs}"""
                
                res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                battle_report = res.choices[0].message.content
                
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.markdown(battle_report)
                st.markdown("</div>", unsafe_allow_html=True)
