import streamlit as st
from openai import OpenAI
from outscraper import ApiClient
import plotly.graph_objects as go
from fpdf import FPDF
import base64

# 1. Setup & Styling
st.set_page_config(page_title="Senara Elite | BI Protocol", page_icon="💎", layout="wide")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    out_client = ApiClient(api_key=st.secrets["OUTSCRAPER_API_KEY"])
except:
    st.error("Credentials missing in Secrets.")

# Glassmorphism CSS
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #e2e8f0; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    .report-card { 
        background: rgba(255, 255, 255, 0.05); 
        backdrop-filter: blur(10px);
        border-radius: 15px; 
        padding: 25px; 
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 20px;
    }
    .stButton>button { 
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%); 
        color: white; border: none; border-radius: 8px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# PDF Logic
def create_pdf(biz_name, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"SENARA ELITE: {biz_name} STRATEGIC AUDIT", ln=True, align='C')
    pdf.set_font("Arial", size=11)
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=content)
    return pdf.output(dest='S').encode('latin-1')

# 2. Tabs
tab1, tab2, tab3 = st.tabs(["🚀 Response Engine", "📊 Strategic Auto-Audit", "⚔️ Market Versus"])

# --- TAB 2: THE POLISHED AUDIT ---
with tab2:
    st.title("💎 Automated Business Intelligence")
    target_link = st.text_input("Enter Google Maps URL", placeholder="Paste business link here...")
    
    if st.button("EXECUTE PROTOCOL"):
        with st.status("📡 Extracting Intelligence...", expanded=True) as status:
            data = out_client.google_maps_reviews(target_link, reviews_limit=20, language='en')
            
            if data and data[0].get('reviews_data'):
                biz_name = data[0].get('name', 'The Business')
                reviews = [r.get('review_text', '') for r in data[0].get('reviews_data') if r.get('review_text')]
                ratings = [r.get('rating') for r in data[0].get('reviews_data')]
                
                # AI Analysis
                prompt = f"Analyze these reviews for {biz_name}. Give a SCORE/10, 3 PROS, 3 CONS, and a GROWTH PLAN: {' '.join(reviews[:15])}"
                res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                report = res.choices[0].message.content

                # UI Layout
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown(f"### 🛡️ Report: {biz_name}")
                    st.markdown(f"<div class='report-card'>{report}</div>", unsafe_allow_html=True)
                    
                    # PDF Download
                    pdf_data = create_pdf(biz_name, report)
                    st.download_button(label="📥 Download PDF Report", data=pdf_data, file_name=f"{biz_name}_Audit.pdf", mime="application/pdf")

                with col2:
                    st.markdown("### 📈 Sentiment Distribution")
                    fig = go.Figure(data=[go.Histogram(x=ratings, marker_color='#3b82f6', nbinsx=5)])
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=300)
                    st.plotly_chart(fig)
                    
                    st.markdown("### 📧 Outreach Agent")
                    if st.button("Draft Acquisition Email"):
                        email_prompt = f"Write a cold email to the owner of {biz_name} mentioning their {sum(ratings)/len(ratings):.1f} star rating and offering to help fix their 'Cons' found in this report: {report}"
                        email_res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":email_prompt}])
                        st.markdown(f"<div class='report-card'>{email_res.choices[0].message.content}</div>", unsafe_allow_html=True)
                
                status.update(label="✅ Analysis Complete", state="complete")
            else:
                st.error("No intelligence found at that link.")
