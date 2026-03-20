import streamlit as st
from openai import OpenAI
from outscraper import ApiClient
import plotly.express as px
import pandas as pd
from fpdf import FPDF

# 1. Page Configuration
st.set_page_config(page_title="Senara Intelligence", page_icon="✨", layout="wide")

# Initialize Session State
if "audit_history" not in st.session_state:
    st.session_state.audit_history = []

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    out_client = ApiClient(api_key=st.secrets["OUTSCRAPER_API_KEY"])
except:
    st.error("API Keys missing in Secrets.")

# 2. THE DESIGNER'S CSS (Soft UI & Modern Gradients)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    
    /* Subtle Background */
    .stApp { background-color: #fcfcfd; color: #1a1a1a; }
    
    /* Glass Sidebar */
    [data-testid="stSidebar"] { 
        background-color: #ffffff !important; 
        border-right: 1px solid #f0f0f0; 
    }
    
    /* Soft UI Cards */
    .premium-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #f1f1f1;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        margin-bottom: 25px;
    }

    /* Modern Tabs */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent;
        border-radius: 10px;
        color: #666;
    }
    .stTabs [data-baseweb="tab"]:hover { color: #000; }
    
    /* Buttons: Dark & Elegant */
    .stButton>button {
        background-color: #111827;
        color: #ffffff;
        border-radius: 12px;
        padding: 12px 24px;
        border: none;
        font-weight: 600;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (The Archive)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1055/1055644.png", width=50)
    st.title("Senara")
    st.markdown("### 🗂️ Analysis Vault")
    if not st.session_state.audit_history:
        st.caption("No recent intelligence captured.")
    for item in st.session_state.audit_history:
        with st.expander(f"📍 {item['name']}"):
            st.write(f"Score: {item['score']}")

# 4. MAIN INTERFACE
tab1, tab2, tab3 = st.tabs(["🚀 Engine", "📊 Strategic Audit", "⚔️ Market Versus"])

with tab2:
    st.markdown("## 📊 Strategic Intelligence")
    st.write("Extract live market data and generate executive reports.")
    
    url_input = st.text_input("Google Maps URL", placeholder="Paste the business link here...")
    
    if st.button("EXECUTE AUDIT"):
        if url_input:
            with st.status("📡 Intercepting Data...", expanded=True) as status:
                data = out_client.google_maps_reviews(url_input, reviews_limit=20, language='en')
                
                if data:
                    biz_name = data[0].get('name', 'Business')
                    reviews_list = data[0].get('reviews_data', [])
                    ratings = [r.get('rating') for r in reviews_list]
                    texts = " ".join([r.get('review_text', '') for r in reviews_list[:10]])
                    
                    # AI Analysis Logic
                    ai_prompt = f"Analyze reviews for {biz_name}. Format as: SCORE: X/10, PROS: [List], CONS: [List], STRATEGY: [List]. {texts}"
                    res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": ai_prompt}])
                    full_report = res.choices[0].message.content
                    
                    # Extract Score for Sidebar
                    score_val = full_report.split("SCORE:")[1].split("/10")[0] if "SCORE:" in full_report else "N/A"
                    st.session_state.audit_history.append({"name": biz_name, "report": full_report, "score": score_val})

                    status.update(label="✅ intelligence Extracted", state="complete")

                    # DISPLAY RESULTS
                    col1, col2 = st.columns([3, 2], gap="large")
                    
                    with col1:
                        st.markdown(f"<div class='premium-card'><h3>🛡️ Executive Summary: {biz_name}</h3><p>{full_report}</p></div>", unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("<div class='premium-card'><h3>📈 Sentiment Heatmap</h3>", unsafe_allow_html=True)
                        # The "Sick Graph" Logic
                        df = pd.DataFrame(ratings, columns=['Stars'])
                        star_counts = df['Stars'].value_counts().reset_index()
                        fig = px.pie(star_counts, values='count', names='Stars', hole=.4, 
                                     color_discrete_sequence=px.colors.sequential.RdBu)
                        fig.update_layout(showlegend=False, height=250, margin=dict(t=0, b=0, l=0, r=0))
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown("</div>", unsafe_allow_width=True)
                        
                        st.markdown("<div class='premium-card'><h3>📋 Next Steps</h3>Generate a pitch email for this client?</div>", unsafe_allow_html=True)
