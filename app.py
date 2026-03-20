import streamlit as st
from openai import OpenAI
from outscraper import ApiClient
import plotly.graph_objects as go
from fpdf import FPDF

# 1. Setup & Premium White Theme
st.set_page_config(page_title="Senara Elite | Intelligence", page_icon="💎", layout="wide")

# Initialize Session State for History
if "audit_history" not in st.session_state:
    st.session_state.audit_history = []

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    out_client = ApiClient(api_key=st.secrets["OUTSCRAPER_API_KEY"])
except:
    st.error("API Keys missing in Secrets.")

# Custom CSS for "Expensive" White Theme
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #f8fafc; color: #1e293b; }
    
    /* Clean Sidebar */
    section[data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e2e8f0; }
    
    /* Modern Cards */
    .premium-card {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    
    /* Typography */
    h1, h2, h3 { color: #0f172a !important; font-weight: 700 !important; }
    p { color: #475569; }
    
    /* Buttons */
    .stButton>button {
        background-color: #0f172a;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover { background-color: #334155; transform: translateY(-1px); }
    </style>
    """, unsafe_allow_html=True)

# PDF Generator
def create_pdf(biz_name, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"EXECUTIVE AUDIT: {biz_name}", ln=True, align='C')
    pdf.set_font("Arial", size=11)
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=content.encode('latin-1', 'replace').decode('latin-1'))
    return pdf.output(dest='S').encode('latin-1')

# --- SIDEBAR HISTORY ---
with st.sidebar:
    st.title("💎 Senara Elite")
    st.markdown("---")
    st.subheader("Recent Intelligence")
    if not st.session_state.audit_history:
        st.write("No recent audits.")
    for item in st.session_state.audit_history:
        st.info(f"📍 {item['name']}")

# --- MAIN INTERFACE ---
tab1, tab2, tab3 = st.tabs(["🚀 Response Engine", "📊 Strategic Audit", "⚔️ Market Versus"])

with tab1:
    st.title("Response Engine")
    with st.container():
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        rev_in = st.text_area("Input Customer Sentiment", placeholder="Paste review here...", height=150)
        if st.button("Generate Response"):
            if rev_in:
                res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": f"Write a luxury-brand response to: {rev_in}"}])
                st.markdown("### Drafted Response")
                st.write(res.choices[0].message.content)
        st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.title("Strategic Audit")
    url_in = st.text_input("Google Maps URL", placeholder="https://maps.google.com/...")
    
    if st.button("Execute Audit"):
        with st.spinner("Analyzing Market Data..."):
            data = out_client.google_maps_reviews(url_in, reviews_limit=15, language='en')
            if data:
                biz_name = data[0].get('name', 'Business')
                reviews = [r.get('review_text', '') for r in data[0].get('reviews_data') if r.get('review_text')]
                ratings = [r.get('rating') for r in data[0].get('reviews_data')]
                
                # AI Logic
                ai_res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":f"Audit this: {' '.join(reviews[:10])}"}])
                report = ai_res.choices[0].message.content
                
                # Add to History
                if biz_name not in [x['name'] for x in st.session_state.audit_history]:
                    st.session_state.audit_history.append({"name": biz_name, "report": report})

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"<div class='premium-card'><h3>{biz_name} Report</h3>{report}</div>", unsafe_allow_html=True)
                    st.download_button("Download Executive PDF", data=create_pdf(biz_name, report), file_name=f"{biz_name}_Audit.pdf")
                with col2:
                    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
                    fig = go.Figure(data=[go.Histogram(x=ratings, marker_color='#0f172a')])
                    fig.update_layout(title="Sentiment Distribution", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig)
                    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.title("Market Versus")
    st.info("Compare competitors side-by-side. Code expanding...")
