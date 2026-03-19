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
    st.write("Business Intelligence & Reputation Management")
    st.markdown("---")
    st.subheader("📜 Recent Activity")
    for item in reversed(st.session_state.history[-3:]):
        st.info(f"**{item['biz']}**\n{item['type']}")

# 4. Tabs
tab1, tab2 = st.tabs(["🚀 Reply Generator", "📊 Business Auditor"])

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.title("Senara Replies")
        biz_name = st.text_input("Business Name", key="biz_gen")
        rating = st.select_slider("Review Stars", options=[1, 2, 3, 4, 5])
        review = st.text_area("Single Review")
        if st.button("Generate Reply"):
            prompt = f"Write a professional response for {biz_name} for a {rating} star review: {review}"
            res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
            answer = res.choices[0].message.content
            st.session_state.history.append({"biz": biz_name, "type": "Reply Generated"})
            st.success("Done!")
            st.code(answer)

with tab2:
    st.title("Business Health Audit")
    st.write("Paste a batch of reviews to see your deep-dive analytics.")
    all_reviews = st.text_area("Paste multiple reviews here", height=250, placeholder="Review 1...\nReview 2...\nReview 3...")
    
    if st.button("Run Senara Audit"):
        if all_reviews:
            with st.spinner("Extracting business intelligence..."):
                # We ask the AI to give us the score as a number we can use
                audit_prompt = f"""
                Analyze these reviews. 
                FIRST, give a single number from 1 to 10 for overall customer satisfaction.
                THEN, provide:
                - TOP PROS
                - TOP WEAKNESSES
                - ACTION PLAN
                
                Reviews: {all_reviews}
                """
                res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": audit_prompt}])
                report = res.choices[0].message.content
                
                # Visual Score Logic (Parsing the first number it finds)
                try:
                    score = int(''.join(filter(str.isdigit, report[:10]))) / 10
                except:
                    score = 0.5
                
                st.markdown("---")
                st.subheader("📋 Senara Health Score")
                st.progress(score) # This is the "Health Bar"
                st.write(f"**Overall Rating: {int(score*10)}/10**")
                
                st.markdown(report)
                st.session_state.history.append({"biz": "Batch Audit", "type": "Health Report"})
