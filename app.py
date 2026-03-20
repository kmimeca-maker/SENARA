import streamlit as st
from openai import OpenAI
from outscraper import ApiClient
import re

# 1. Core Setup
st.set_page_config(page_title="Senara Elite", page_icon="💎", layout="wide")

# 2. Connection Logic
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    out_client = ApiClient(api_key=st.secrets["OUTSCRAPER_API_KEY"])
except Exception as e:
    st.error("Connection Keys Missing in Secrets.")

# --- CSS STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0a192f; color: #ccd6f6; }
    .stButton>button { background-color: #3498db; color: white; border: none; height: 3em; font-weight: bold; width: 100%; }
    .report-box { background-color: #112240; padding: 25px; border-radius: 15px; border: 1px solid #233554; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

# 3. App Tabs
tab1, tab2, tab3 = st.tabs(["🚀 Response Engine", "📊 Auto-Audit", "⚔️ Market Versus"])

# --- TAB 1: RESPONSE ENGINE ---
with tab1:
    st.markdown("### 🚀 AI Response Generator")
    review_input = st.text_area("Paste a customer review here to generate a perfect response:", height=150)
    if st.button("GENERATE RESPONSE"):
        if review_input:
            with st.spinner("Writing response..."):
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": f"Write a professional, empathetic response to this review: {review_input}"}]
                )
                st.markdown(f"<div class='report-box'>{res.choices[0].message.content}</div>", unsafe_allow_html=True)

# --- TAB 2: THE AUTOMATED AUDIT ---
with tab2:
    st.markdown("### 📊 Automated Business Intelligence")
    target_link = st.text_input("Google Maps URL", placeholder="https://www.google.com/maps/place/...")
    
    if st.button("🔍 INITIATE GLOBAL AUDIT"):
        if target_link:
            with st.status("🚀 Deploying Scraper...", expanded=True) as status:
                try:
                    # Logic: Get reviews from the link
                    data = out_client.google_maps_reviews(target_link, reviews_limit=10, language='en')
                    
                    reviews_text = ""
                    biz_name = "The Business"
                    
                    if data and len(data) > 0:
                        biz_name = data[0].get('name', 'The Business')
                        reviews_list = data[0].get('reviews_data', [])
                        
                        for r in reviews_list:
                            if r.get('review_text'):
                                reviews_text += f"- {r.get('review_text')}\n"
                    
                    if reviews_text:
                        st.write(f"🧠 AI Analyzing {biz_name}...")
                        prompt = f"Analyze these reviews for {biz_name}. Give a SCORE (X/10), 3 PROS, 3 CONS, and a GROWTH PLAN: {reviews_text}"
                        res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                        
                        status.update(label="✅ Audit Complete", state="complete", expanded=False)
                        st.subheader(f"Strategic Report: {biz_name}")
                        st.markdown(f"<div class='report-box'>{res.choices[0].message.content}</div>", unsafe_allow_html=True)
                    else:
                        status.update(label="❌ No Reviews Found", state="error")
                        st.error("The scraper connected, but couldn't find text reviews. Try a more popular business link.")
                except Exception as e:
                    st.error(f"Scraper Error: {e}")

# --- TAB 3: MARKET VERSUS ---
with tab3:
    st.markdown("### ⚔️ Competitive Battle Report")
    col1, col2 = st.columns(2)
    with col1:
        my_revs = st.text_area("Paste Your Reviews")
    with col2:
        rival_revs = st.text_area("Paste Rival Reviews")
    
    if st.button("⚔️ EXECUTE BATTLE ANALYSIS"):
        res = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[{"role":"user", "content": f"Compare these businesses based on reviews: {my_revs} VS {rival_revs}"}]
        )
        st.markdown(f"<div class='report-box'>{res.choices[0].message.content}</div>", unsafe_allow_html=True)
