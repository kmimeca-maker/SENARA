import streamlit as st
from openai import OpenAI
from outscraper import ApiClient

# 1. Core Setup
st.set_page_config(page_title="Senara Elite", page_icon="💎", layout="wide")

# 2. Connection Logic
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    out_client = ApiClient(api_key=st.secrets["OUTSCRAPER_API_KEY"])
except Exception as e:
    st.error("Connection Keys Missing. Please check your Streamlit Secrets.")

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

with tab1:
    st.markdown("### 🚀 AI Response Generator")
    rev_to_respond = st.text_area("Paste a review to answer:", placeholder="Paste here...")
    if st.button("GENERATE AI RESPONSE"):
        if rev_to_respond:
            res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":f"Write a professional response to: {rev_to_respond}"}])
            st.markdown(f"<div class='report-box'>{res.choices[0].message.content}</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("### 📊 Automated Business Intelligence")
    target_link = st.text_input("Google Maps URL", placeholder="Paste the KFC link here...")
    
    if st.button("🔍 INITIATE GLOBAL AUDIT"):
        if target_link:
            with st.status("🚀 Scraping Live Reviews...", expanded=True) as status:
                try:
                    # Searching for the place and its reviews
                    results = out_client.google_maps_reviews(target_link, reviews_limit=20, language='en')
                    
                    if results and len(results) > 0:
                        biz_name = results[0].get('name', 'The Business')
                        reviews = results[0].get('reviews_data', [])
                        
                        review_text_combined = ""
                        for r in reviews:
                            if r.get('review_text'):
                                review_text_combined += f"- {r.get('review_text')}\n"
                        
                        if review_text_combined:
                            st.write(f"🧠 AI Analyzing {biz_name}...")
                            prompt = f"Perform a strategic audit on these reviews for {biz_name}. Give a Score/10, Pros, Cons, and a Growth Plan: {review_text_combined}"
                            ai_res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                            
                            status.update(label="✅ Audit Complete", state="complete")
                            st.subheader(f"Report for {biz_name}")
                            st.markdown(f"<div class='report-box'>{ai_res.choices[0].message.content}</div>", unsafe_allow_html=True)
                        else:
                            st.error("Found the business, but couldn't find any written reviews. Try a busier location.")
                    else:
                        st.error("Could not find that location. Try a shorter link.")
                except Exception as e:
                    st.error(f"Technical Error: {e}")

with tab3:
    st.markdown("### ⚔️ Market Versus")
    st.write("Manual comparison mode active.")
