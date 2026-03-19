
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key="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")

st.set_page_config(page_title="Senara Reviews", page_icon="🥈")
st.title("🥈 Senara Reviews")
st.subheader("Professional AI Response Generator")

biz_name = st.text_input("Business Name")
tone = st.selectbox("Tone", ["Professional", "Friendly", "Apologetic"])
review = st.text_area("Paste Customer Review")

if st.button("Generate Senara Reply"):
    if biz_name and review:
        with st.spinner("Senara is crafting a response..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are Senara, an AI for {biz_name}. Write a {tone} reply. Max 4 sentences."},
                    {"role": "user", "content": review}
                ]
            )
            st.success(response.choices[0].message.content)
    else:
        st.error("Please fill in the boxes!")
