import streamlit as st
from openai import OpenAI

# 1. Page Config
st.set_page_config(page_title="Senara AI Elite", page_icon="💎", layout="wide")

# 2. Connection
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "history" not in st.session_state:
    st.session_state.history = []

# 3. Sidebar
with st.sidebar:
    st.title("💎 Senara Elite")
    st.write("Helping you retire your mum, one business at a time.")
    st.markdown("---")
    st.subheader("📜 Recent Replies")
    for item in reversed(st.session_state.history[-3:]):
        st.info(f"**{item['biz']}**\n{item['reply'][:40]}...")

# 4. Tabs (The New Part!)
tab1, tab2 = st.tabs(["🚀 Reply Generator", "📊 Business Auditor"])

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.title("Senara Reviews")
        biz_name = st.text_input("Business Name")
        rating = st.select_slider("Stars", options=[1, 2, 3, 4, 5])
        review = st.text_area("Single Review to Reply To")
        if st.button("Generate Reply"):
            # ... (Same logic as before)
            prompt = f"Write a professional response for {biz_name} for a {rating} star review: {review}"
            res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
            answer = res.choices[0].message.content
            st.session_state.history.append({"biz": biz_name, "reply": answer})
            st.success("Done!")
            st.code(answer)

with tab2:
    st.title("Business Audit")
    st.write("Paste multiple reviews below to see your biggest Pros and Cons.")
    all_reviews = st.text_area("Paste 5-10 reviews here (one per line)", height=300)
    
    if st.button("Analyze Business Health"):
        if all_reviews:
            with st.spinner("Analyzing patterns..."):
                audit_prompt = f"""
                Analyze these customer reviews for a business.
                Provide a report in this exact format:
                1. BIGGEST WEAKNESSES (Top 3 points)
                2. BIGGEST PROS (Top 3 points)
                3. URGENT FIXES (What should the owner do tomorrow?)
                4. SCORE: X/10
                
                Reviews:
                {all_reviews}
                """
                res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": audit_prompt}])
                report = res.choices[0].message.content
                
                st.subheader("📋 Senara Health Report")
                st.markdown(report)
                st.download_button("Download Report as Text", report)
