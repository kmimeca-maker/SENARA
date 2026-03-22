import streamlit as st
from openai import OpenAI
from outscraper import ApiClient

# 1. System Setup
st.set_page_config(page_title="Senara Elite", layout="wide")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    out_client = ApiClient(api_key=st.secrets["OUTSCRAPER_API_KEY"])
except:
    st.error("Credential Error: Please verify your Streamlit Secrets.")

# 2. Professional Studio Styling
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #111827; }
    .premium-card {
        background: #ffffff;
        padding: 24px;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
    th { background-color: #f9fafb; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.title("Senara Elite")
    st.info("High-Value Strategic Intelligence")

# 4. Defining the Tabs (This prevents the 'NameError')
tab1, tab2, tab3 = st.tabs(["Response Engine", "Strategic Audit", "Market Versus"])

with tab1:
    st.header("Response Engine")
    st.write("Professional review management.")
    st.text_area("Paste Review", placeholder="Enter customer feedback here...", height=200)
    st.button("Generate Response")

with tab2:
    st.header("Strategic Audit")
    st.write("Single-location deep dive.")
    url_audit = st.text_input("Google Maps URL", key="audit_url")
    if st.button("Run Audit"):
        st.warning("Fetching data... please wait.")

with tab3:
    st.header("Market Versus")
    st.write("Identify why customers are choosing the competition over you.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        url_a = st.text_input("Primary Business URL", placeholder="Your link...", key="v_a")
    with col_b:
        url_b = st.text_input("Competitor URL", placeholder="Their link...", key="v_b")
    
    if st.button("Execute Battle Analysis"):
        if url_a and url_b:
            with st.status("Gathering Intelligence...") as status:
                try:
                    # 1. Scrape
                    data_a = out_client.google_maps_reviews(url_a, reviews_limit=10)
                    data_b = out_client.google_maps_reviews(url_b, reviews_limit=10)
                    
                    name_a = data_a[0].get('name', 'Your Business')
                    name_b = data_b[0].get('name', 'Competitor')
                    
                    revs_a = " ".join([r.get('review_text', '') for r in data_a[0].get('reviews_data')])
                    revs_b = " ".join([r.get('review_text', '') for r in data_b[0].get('reviews_data')])

                    # 2. Analyze
                    prompt = f"""
                    Compare {name_a} vs {name_b}.
                    1. Create a Markdown table for: Price, Service, and Quality (Scores /10).
                    2. Add 'Revenue Leakage': Explain one reason customers are leaving A for B.
                    3. Add '30-Day Win Strategy': Two specific action steps for {name_a}.
                    Reviews for {name_a}: {revs_a[:1000]}
                    Reviews for {name_b}: {revs_b[:1000]}
                    """
                    
                    res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                    report_content = res.choices[0].message.content
                    
                    status.update(label="Analysis Complete", state="complete")

                    # 3. Render (Safe method)
                    st.subheader(f"Battle Report: {name_a} vs {name_b}")
                    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
                    st.markdown(report_content)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"System Error: {e}")
