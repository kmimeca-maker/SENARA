import streamlit as st
from openai import OpenAI
from outscraper import ApiClient

# 1. Page Configuration & Session Data
st.set_page_config(page_title="Senara Elite", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    out_client = ApiClient(api_key=st.secrets["OUTSCRAPER_API_KEY"])
except:
    st.error("Credential Error: Please check your Streamlit Secrets.")

# 2. Clean, Reliable CSS (Fixed Rendering Issues)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    
    .stApp { background-color: #ffffff; color: #1f2937; }

    /* Clean Sidebar */
    section[data-testid="stSidebar"] { background-color: #111827 !important; }
    section[data-testid="stSidebar"] * { color: #f9fafb !important; }

    /* Simplified Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: #f3f4f6;
        padding: 6px;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600 !important;
        color: #6b7280 !important;
        border: none !important;
    }
    .stTabs [data-baseweb="tab--active"] {
        background-color: #ffffff !important;
        color: #111827 !important;
        border-radius: 6px !important;
    }

    /* Professional Result Cards */
    .result-card {
        background: #ffffff;
        padding: 24px;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        margin-top: 15px;
    }
    
    .stButton>button {
        background-color: #111827 !important;
        color: #ffffff !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        width: 100%;
        border: none !important;
        height: 45px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Navigation
with st.sidebar:
    st.title("Senara Elite")
    st.markdown("---")
    st.subheader("Saved Analysis")
    if not st.session_state.history:
        st.caption("No history yet.")
    for item in st.session_state.history:
        st.markdown(f"• {item}")

# 4. Main Dashboard
st.title("Business Intelligence Dashboard")
st.markdown("Gain insights from customer reviews to improve your business and outperform competition.")

t1, t2, t3 = st.tabs(["Review Drafting", "Location Audit", "Competitive Comparison"])

with t1:
    st.subheader("Review Drafting")
    st.write("Create professional, helpful replies to your customer reviews.")
    rev_text = st.text_area("Paste the review text here:", height=150)
    if st.button("Create Draft"):
        st.info("Generating a professional response draft...")

with t2:
    st.subheader("Location Audit")
    st.write("Understand your strengths and weaknesses based on recent customer feedback.")
    url_audit = st.text_input("Enter Google Maps URL:", placeholder="Paste link here...", key="audit_in")
    if st.button("Generate Audit Report"):
        st.warning("Analyzing data... this may take up to 30 seconds.")

with t3:
    st.subheader("Competitive Comparison")
    
    # 📝 Simple Tutorial (No buggy icons)
    st.markdown("""
    **How to use this tool:**
    1. **Copy your link:** Search your business on Google Maps and click 'Share' to copy the link.
    2. **Paste your link:** Put it in the 'Your Business' box below.
    3. **Copy rival link:** Find a nearby competitor and copy their 'Share' link.
    4. **Paste rival link:** Put it in the 'Competitor' box.
    5. **Analyze:** Click 'Compare Businesses' to see where you can improve.
    """)
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        link_a = st.text_input("Your Business Link", placeholder="Paste Google Maps URL...")
    with c2:
        link_b = st.text_input("Competitor Link", placeholder="Paste Google Maps URL...")
    
    if st.button("Compare Businesses"):
        if link_a and link_b:
            with st.status("Gathering comparative data...") as status:
                try:
                    # Fetching Data
                    data_a = out_client.google_maps_reviews(link_a, reviews_limit=10)
                    data_b = out_client.google_maps_reviews(link_b, reviews_limit=10)
                    
                    n1, n2 = data_a[0]['name'], data_b[0]['name']
                    
                    if n1 not in st.session_state.history:
                        st.session_state.history.append(n1)

                    # Simple AI Prompt
                    prompt = f"""
                    Compare {n1} and {n2} based on their reviews.
                    1. Create a table comparing them on Service, Price, and Quality (Score 1-10).
                    2. Explain the main reason customers might choose {n2} over {n1}.
                    3. List 3 specific steps {n1} can take to win back customers.
                    """
                    
                    res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                    
                    status.update(label="Analysis Complete", state="complete")
                    
                    st.markdown(f"### Comparison: {n1} vs {n2}")
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.markdown(res.choices[0].message.content)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error connecting to data sources: {e}")
