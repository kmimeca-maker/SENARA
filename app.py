import streamlit as st
from openai import OpenAI
from outscraper import ApiClient
import plotly.graph_objects as go
from fpdf import FPDF

# 1. Setup & Styling
st.set_page_config(page_title="Senara Elite | BI Protocol", page_icon="💎", layout="wide")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    out_client = ApiClient(api_key=st.secrets["OUTSCRAPER_API_KEY"])
except:
    st.error("Credentials missing in Secrets. Please check OPENAI_API_KEY and OUTSCRAPER_API_KEY.")

# Improved CSS for visibility
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #e2e8f0; }
    .report-card { 
        background: rgba(255, 255, 255, 0.07); 
        border-radius: 12px; 
        padding: 20px; 
        border: 1px solid rgba(255,255,255,0.1);
        margin-top: 10px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.05);
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# PDF Logic
def create_pdf(biz_name, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"SENARA ELITE: {biz_name} AUDIT", ln=True, align='C')
    pdf.set_font("Arial", size=11)
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=content.encode('latin-1', 'replace').decode('latin-1'))
    return pdf.output(dest='S').encode('latin-1')

# 2. Tabs Construction
tab1, tab2, tab3 = st.tabs(["🚀 Response Engine", "📊 Strategic Auto-Audit", "⚔️ Market Versus"])

# --- TAB 1: RESPONSE ENGINE ---
with tab1:
    st.header("🚀 AI Response Generator")
    st.write("Turn negative reviews into loyalty-building opportunities.")
    rev_input = st.text_area("Paste Customer Review:", height=150, key="resp_input")
    
    if st.button("GENERATE ELITE RESPONSE"):
        if rev_input:
            with st.spinner("Drafting..."):
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": f"Write a professional, high-end response to this review: {rev_input}"}]
                )
                st.markdown("### Suggested Response")
                st.markdown(f"<div class='report-card'>{res.choices[0].message.content}</div>", unsafe_allow_html=True)

# --- TAB 2: AUTO-AUDIT ---
with tab2:
    st.header("📊 Automated Business Intelligence")
    target_link = st.text_input("Google Maps URL:", placeholder="Paste link here...", key="audit_link")
    
    if st.button("EXECUTE AUDIT PROTOCOL"):
        if target_link:
            with st.status("📡 Extracting Intelligence...") as status:
                data = out_client.google_maps_reviews(target_link, reviews_limit=20, language='en')
                
                if data and data[0].get('reviews_data'):
                    biz_name = data[0].get('name', 'The Business')
                    reviews = [r.get('review_text', '') for r in data[0].get('reviews_data') if r.get('review_text')]
                    ratings = [r.get('rating') for r in data[0].get('reviews_data')]
                    
                    # AI Report
                    prompt = f"Analyze reviews for {biz_name}. Score/10, 3 Pros, 3 Cons, 3-step Growth Plan: {' '.join(reviews[:15])}"
                    res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                    report_text = res.choices[0].message.content

                    status.update(label="✅ Analysis Complete", state="complete")
                    
                    col_left, col_right = st.columns([1, 1])
                    with col_left:
                        st.subheader(f"🛡️ {biz_name} Report")
                        st.markdown(f"<div class='report-card'>{report_text}</div>", unsafe_allow_html=True)
                        st.download_button("📥 Download PDF", data=create_pdf(biz_name, report_text), file_name=f"{biz_name}_Audit.pdf")

                    with col_right:
                        st.subheader("📈 Rating Spread")
                        fig = go.Figure(data=[go.Histogram(x=ratings, marker_color='#3b82f6')])
                        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=300)
                        st.plotly_chart(fig)
                        
                        if st.button("Draft Outreach Email"):
                            e_res = client.chat.completions.create(
                                model="gpt-4o-mini", 
                                messages=[{"role":"user", "content": f"Write a pitch email to {biz_name} owner using this report: {report_text}"}]
                            )
                            st.markdown(f"<div class='report-card'>{e_res.choices[0].message.content}</div>", unsafe_allow_html=True)
                else:
                    st.error("Intelligence extraction failed. Verify link.")

# --- TAB 3: MARKET VERSUS ---
with tab3:
    st.header("⚔️ Competitive Battle Report")
    st.write("Compare your performance directly against a local rival.")
    c1, c2 = st.columns(2)
    with c1:
        my_name = st.text_input("Your Business Name")
        my_revs = st.text_area("Your Reviews:", height=200, key="my_revs")
    with c2:
        ri_name = st.text_input("Rival Business Name")
        ri_revs = st.text_area("Rival Reviews:", height=200, key="ri_revs")
    
    if st.button("⚔️ INITIATE BATTLE ANALYSIS"):
        if my_revs and ri_revs:
            with st.spinner("Analyzing Market Position..."):
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"user", "content": f"Compare {my_name} vs {ri_name}. Who is winning and where? {my_revs} vs {ri_revs}"}]
                )
                st.markdown("### Tactical Comparison")
                st.markdown(f"<div class='report-card'>{res.choices[0].message.content}</div>", unsafe_allow_html=True)
