import streamlit as st
from openai import OpenAI

# 1. Setup
st.set_page_config(page_title="Senara Elite", page_icon="💎", layout="wide")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 2. Sidebar
with st.sidebar:
    st.title("💎 Senara Elite")
    st.write("Professional Business Intelligence")
    st.markdown("---")
    st.info("Switch between the tabs at the top to change tools.")

# 3. THE TABS (This creates the navigation at the top of your website)
tab1, tab2 = st.tabs(["🚀 Response Engine", "📊 Strategic Audit"])

# --- TAB 1: REPLY GENERATOR ---
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Draft a Reply")
        biz = st.text_input("Business Name")
        rev = st.text_area("Paste Review")
        if st.button("Generate"):
            res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":f"Reply to this for {biz}: {rev}"}])
            st.session_state.reply = res.choices[0].message.content
    with col2:
        if "reply" in st.session_state:
            st.subheader("Your AI Reply")
            st.code(st.session_state.reply)

# --- TAB 2: BUSINESS AUDITOR (Where the error was!) ---
with tab2:
    st.title("Strategic Business Audit")
    bulk_input = st.text_area("Paste 5+ Reviews here", height=200)
    
    if st.button("Run Diagnostic"):
        if bulk_input:
            with st.spinner("Analyzing..."):
                prompt = f"Analyze these reviews. Give a SCORE: [1-10] and then list PROS and CONS. Reviews: {bulk_input}"
                res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                report = res.choices[0].message.content
                
                # THE SAFETY NET: This looks for the number so it doesn't crash
                import re
                scores = re.findall(r'\d+', report)
                score_num = int(scores[0]) if scores else 5
                
                # Display Results
                st.metric("Business Health Score", f"{score_num}/10")
                st.progress(score_num/10)
                st.markdown(report)
