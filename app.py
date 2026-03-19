import streamlit as st
from openai import OpenAI

# 1. Page Config
st.set_page_config(page_title="Senara AI", page_icon="💎", layout="centered")

# 2. Key Connection
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 3. Sidebar Design
with st.sidebar:
    st.title("💎 Senara Pro")
    st.markdown("---")
    st.write("Helping you retire the stress of customer management.")
    st.info("Tip: Use the 'Empathetic' tone for 1-star reviews.")

# 4. Main Interface
st.title("🥈 Senara Reviews")
st.subheader("Professional AI Response Generator")

# Inputs
biz_name = st.text_input("Business Name", placeholder="e.g. Senara Bistro")
tone = st.selectbox("Response Tone", ["Professional", "Empathetic", "Concise", "Witty"])
review = st.text_area("Paste Customer Review", height=150)

# 5. Logic & Response
if st.button("Generate Senara Reply"):
    if biz_name and review:
        with st.spinner("Senara is crafting your response..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": f"You are a world-class customer relations expert for {biz_name}. Write a {tone} reply to this review. Max 4 sentences."},
                        {"role": "user", "content": review}
                    ]
                )
                answer = response.choices[0].message.content
                
                # Visual Result
                st.success("Response Generated!")
                st.markdown(f"### Proposed Reply for {biz_name}:")
                st.code(answer, language=None) # This creates a 'Click to Copy' box!
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please fill in the business name and the review.")
