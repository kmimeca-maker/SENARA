import streamlit as st
from openai import OpenAI

# 1. Page Config - Wide mode is essential for that 'SaaS' feel
st.set_page_config(page_title="Senara Intelligence", page_icon="💎", layout="wide")

# 2. Key Connection
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "history" not in st.session_state:
    st.session_state.history = []

# 3. Sidebar Styling
with st.sidebar:
    st.title("💎 Senara Elite")
    st.caption("v2.0 - Professional Suite")
    st.markdown("---")
    if st.button("🗑️ Clear Workspace"):
        st.session_state.history = []
        st.rerun()

# 4. Main Navigation
tab1, tab2 = st.tabs(["🚀 Response Engine", "📊 Strategic Audit"])

with tab1:
    col_in, col_out = st.columns([1, 1.2], gap="large")
    with col_in:
        st.subheader("Draft a Reply")
        biz_name = st.text_input("Business Name", placeholder="e.g. Senara Bistro")
        rating = st.select_slider("Customer Rating", options=[1, 2, 3, 4, 5])
        review_text = st.text_area("Customer Review", height=150)
        
        if st.button("✨ Craft Response", use_container_width=True):
            prompt = f"Write a professional response for {biz_name} for a {rating} star review: {review_text}"
            res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
            st.session_state.last_reply = res.choices[0].message.content

    with col_out:
        if "last_reply" in st.session_state:
            st.subheader("Final Draft")
            st.info("Copy the text below to your clipboard.")
            st.code(st.session_state.last_reply, language=None)

with tab2:
    st.title("Strategic Business Audit")
    st.write("Input bulk review data to generate a SWOT analysis and Health Score.")
    
    bulk_input = st.text_area("Paste Reviews (One per line)", height=200)
    
    if st.button("📈 Run Full Diagnostic", use_container_width=True):
        if bulk_input:
            with st.spinner("Processing Business Intelligence..."):
                # We ask for structured data
                audit_prompt = f"""Analyze these reviews. Return ONLY a JSON-like format:
                SCORE: [number 1-10]
                PROS: [3 bullet points]
                CONS: [3 bullet points]
                ACTION: [1 major instruction]
                Reviews: {bulk_input}"""
                
                res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": audit_prompt}])
                raw_report = res.choices[0].message.content
                
                # Extracting the score for the progress bar
                score_num = int(''.join(filter(str.isdigit, raw_report.split('\n')[0])))
                
                # --- PRO UI LAYOUT ---
                m1, m2, m3 = st.columns(3)
                m1.metric("Health Score", f"{score_num}/10", delta=f"{score_num-5} vs Avg")
                m2.metric("Sentiment", "Analyzed" if score_num > 5 else "Critical")
                m3.metric("Status", "Operational" if score_num > 4 else "Requires Action")
                
                st.progress(score_num/10)
                
                col_left, col_right = st.columns(2)
                with col_left:
                    with st.expander("✅ Core Strengths", expanded=True):
                        st.write(raw_report.split("PROS:")[1].split("CONS:")[0])
                with col_right:
                    with st.expander("⚠️ Critical Weaknesses", expanded=True):
                        st.write(raw_report.split("CONS:")[1].split("ACTION:")[0])
                
                st.divider()
                st.subheader("🎯 CEO Action Plan")
                st.success(raw_report.split("ACTION:")[1])
