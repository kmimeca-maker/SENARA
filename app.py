with tab2:
    st.markdown("## Strategic Audit")
    st.write("Extract live market data and generate single-business executive reports.")
    url_input = st.text_input("Location URL", placeholder="Paste Google Maps link...", key="single_audit")
    
    if st.button("RUN DIAGNOSTIC", key="btn_audit"):
        if url_input:
            with st.status("Gathering Intelligence...") as status:
                try:
                    data = out_client.google_maps_reviews(url_input, reviews_limit=15, language='en')
                    if data:
                        biz_name = data[0].get('name', 'Business')
                        reviews = [r.get('review_text', '') for r in data[0].get('reviews_data') if r.get('review_text')]
                        
                        ai_res = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{"role":"user", "content": f"Audit for {biz_name}: {' '.join(reviews[:10])}"}]
                        )
                        report = ai_res.choices[0].message.content
                        
                        if biz_name not in st.session_state.history:
                            st.session_state.history.append(biz_name)
                        
                        status.update(label="Complete", state="complete")

                        # FIXED HTML BLOCK
                        st.subheader(f"Executive Report: {biz_name}")
                        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
                        st.markdown(report)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Error: {e}")

with tab3:
    st.markdown("## Market Versus")
    st.write("Compare your business directly against a local rival.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        url_a = st.text_input("Primary Business URL", key="url_a_val")
    with col_b:
        url_b = st.text_input("Competitor URL", key="url_b_val")
    
    if st.button("EXECUTE BATTLE ANALYSIS", key="btn_compare"):
        if url_a and url_b:
            with st.status("Analyzing Competitive Gap...") as status:
                try:
                    data_a = out_client.google_maps_reviews(url_a, reviews_limit=15)
                    data_b = out_client.google_maps_reviews(url_b, reviews_limit=15)
                    
                    name_a = data_a[0].get('name', 'Business A')
                    name_b = data_b[0].get('name', 'Business B')
                    
                    rev_a = " ".join([r.get('review_text','') for r in data_a[0].get('reviews_data')])
                    rev_b = " ".join([r.get('review_text','') for r in data_b[0].get('reviews_data')])
                    
                    prompt = f"""Compare {name_a} vs {name_b}. 
                    1. Create a Markdown table comparing them on Price, Quality, and Service scores (/10).
                    2. Add a section 'Revenue Impact' estimating % of customers lost to competitor.
                    3. Add '30-Day Win Strategy' with 2 bullet points."""
                    
                    res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
                    
                    status.update(label="Battle Report Ready", state="complete")
                    
                    st.markdown(f"### {name_a} vs {name_b}")
                    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
                    st.markdown(res.choices[0].message.content)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
