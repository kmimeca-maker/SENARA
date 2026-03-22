import streamlit as st
from openai import OpenAI
from outscraper import ApiClient

# 1. Setup & Error Prevention
st.set_page_config(page_title="Senara Elite", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    out_client = ApiClient(api_key=st.secrets["OUTSCRAPER_API_KEY"])
except:
    st.error("Credential Error: Please check your Streamlit Secrets.")

# 2. Modern & Readable UI Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    
    /* Sidebar: Clean Dark Mode */
    section[data-testid="stSidebar"] { background-color: #111827 !important; }
    section[data-testid="stSidebar"] * { color: #ffffff !important; }

    /* Tabs: Bold & Easy to See */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #f3f4f6;
        padding: 8px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        font-weight: 600 !important;
        color: #4b5563 !important;
        border: none !important;
    }
    .stTabs [data-baseweb="tab--active"] {
        background-color: #ffffff !important;
        color: #111827 !important;
        border-radius: 6px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Professional Result Cards */
    .result-card {
        background: #ffffff;
        padding: 25px;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-top: 20px;
    }

    .stButton>button {
        background-color: #111827 !important;
        color: #ffffff !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        width: 100%;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Archive
with st.sidebar:
    st.title("Senara Elite")
    st.markdown("---")
    st.subheader("Saved Audits")
    if not st.session_state.history:
        st.caption("No history yet.")
    for item in st.session_state.history:
        st.markdown(f"• {item}")

# 4. Main App Header
st.title("Business Intelligence Center")
st.markdown("Improve your business by analyzing customer feedback and local competition.")

tab1, tab2, tab3 = st.tabs(["Review Helper", "Business Audit", "Competitive Comparison"])

with tab1:
    st.subheader("Review Helper")
    st.write("Draft polite and professional replies to your customer reviews.")
    review_text = st.text_area("Paste the review here:", height=150)
    if st.button("Draft Reply"):
        st.info("Generating a draft for you...")

with tab2:
    st.subheader("Business Audit")
    st.write("Get a detailed report on what customers love and hate about a specific location.")
    url_audit = st.text_input("Enter Google Maps Link:", key="audit_input")
    if st.button("Run Audit"):
        st.warning("Fetching data... this takes about 30 seconds.")

with tab3:
    st.subheader("Competitive Comparison")
    
    # Tutorial Section
    with st.expander("📖 How to use this tool", expanded=True):
        st.markdown("""
        1. **Find your business** on Google Maps and copy the link from the 'Share' button.
        2. Paste your link into the **'Your Business'** box below.
        3. **Find a competitor** nearby and copy their Google Maps link.
        4. Paste their link into the **'Competitor'** box.
        5. Click **'Compare Businesses'** to see how you stack up.
        """)
    
    col1, col2 = st.columns(2)
    with col1:
        u1 = st.text_input("Your Business Link", placeholder="Paste Google Maps URL...")
    with col2:
        u2 = st.text_input("Competitor Link", placeholder="Paste Google Maps URL...")
    
    if st.button("Compare Businesses"):
        if u1 and u2:
            with st.status("Analyzing differences...") as s:
                try:
                    # Scraping logic
                    d1 = out_client.google_maps_reviews(u1, reviews_limit=10)
                    d2 = out_client.google_maps_reviews(u2, reviews_limit=10)
                    
                    name1, name2 = d1[0]['name'], d2[0]['name']
                    
                    if name1 not in st.session_state.history:
                        st.session_state.history.append(name1)

                    # Simple, Direct AI Prompt
                    prompt = f"""
                    Compare {name1} and {name2} using their reviews.
                    1. Create a table comparing them on Service, Price, and Quality (Score 1-10).
                    2. Explain why people might pick {name2} over {name1}.
                    3. List 3 simple things {name1} should do to improve.
                    """
                    
                    res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                    
                    s.update(label="Comparison Ready", state="complete")
                    
                    st.markdown(f"### Comparison: {name1} vs {name2}")
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.markdown(res.choices[0].message.content)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
