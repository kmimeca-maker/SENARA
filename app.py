import streamlit as st
from openai import OpenAI
from outscraper import ApiClient
import re

# 1. Core Setup
st.set_page_config(page_title="Senara Elite", page_icon="💎", layout="wide")

# 2. Connection Logic (Uses the Secrets you saved!)
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

# --- TAB 2: THE AUTOMATED AUDIT ---
with tab2:
    st.markdown("### 📊 Automated Business Intelligence")
    st.write("Paste a Google Maps link below to extract live reviews and generate a report.")
    
    # This is the "Big Box" for the URL
    target_link = st.text_input("Google Maps URL", placeholder="https://www.google.com/maps/place/...")
    
    if st.button("🔍 INITIATE GLOBAL AUDIT"):
        if target_link:
            with st.status("🚀 Deploying Scraper...", expanded=True) as status:
                st.write("🛰️ Connecting to Google Cloud Nodes...")
                
                try:
                    # The Data Extraction (Outscraper doing the work)
                    data = out_client.google_maps_reviews(target_link, reviews_limit=20, language='en')
                    
                    st.write("📝 Decoding Sentiment Data...")
                    reviews_text = ""
                    biz_name = "The Business"
                    
                    for place in data:
                        biz_name = place.get('name', 'The Business')
                        for r in place.get('reviews_data', []):
                            reviews_text += f"- {r.get('review_text')}\n"
                    
                    if reviews_text:
                        st.write(f"🧠 AI Analyzing {biz_name}...")
                        prompt = f"Act as a high-end consultant. Analyze these reviews for {biz_name}. Give a SCORE (X/10), 3 PROS, 3 CONS, and a 3-step GROWTH PLAN: {reviews_text}"
                        res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                        
                        status.update(label="✅ Audit Complete", state="complete", expanded=False)
                        
                        # Displaying the Result
                        st.subheader(f"Strategic Report: {biz_name}")
                        st.markdown(f"<div class='report-box'>{res.choices[0].message.content}</div>", unsafe_allow_html=True)
                    else:
                        st.error("No reviews found. Try a different business link.")
                except Exception as e:
                    st.error(f"Scraper Error: {e}")
        else:
            st.warning("Please paste a URL first!")

# --- TAB 3: MARKET VERSUS ---
with tab3:
    st.markdown("### ⚔️ Competitive Battle Report")
    col1, col2 = st.columns(2)
    with col1:
        my_name = st.text_input("My Shop Name")
        my_revs = st.text_area("Paste My Reviews")
    with col2:
        rival_name = st.text_input("Rival Shop Name")
        rival_revs = st.text_area("Paste Rival Reviews")
    
    if st.button("⚔️ EXECUTE BATTLE ANALYSIS"):
        prompt = f"Compare {my_name} vs {rival_name} based on these reviews. Who wins and why? {my_revs} VS {rival_revs}"
        res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
        st.markdown(f"<div class='report-box'>{res.choices[0].message.content}</div>", unsafe_allow_html=True)
