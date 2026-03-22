with tab3:
    st.subheader("Competitive Comparison")
    
    # 📝 Simple Tutorial 
    st.markdown("""
    **How to use:**
    1. Paste **your** Google Maps link below.
    2. Click **'Scan for Local Rivals'** to automatically find businesses within 1km.
    3. Select a rival from the list and click **'Compare'**.
    """)
    st.markdown("---")
    
    # Step 1: Your Business
    u1 = st.text_input("Your Business Link", placeholder="Paste your Google Maps URL here...")
    
    if st.button("Step 1: Scan for Local Rivals"):
        if u1:
            with st.status("Scanning 1km radius...") as status:
                try:
                    # 1. Get your business details to find your niche/location
                    my_biz = out_client.google_maps_reviews(u1, reviews_limit=1)
                    lat = my_biz[0].get('latitude')
                    lon = my_biz[0].get('longitude')
                    category = my_biz[0].get('type', 'Restaurant') # Falls back to Restaurant if hidden
                    
                    # 2. Search for similar businesses nearby
                    search_query = f"{category} near {lat}, {lon}"
                    rivals = out_client.google_maps_search([search_query], limit=4) # Get 4 to exclude self
                    
                    # 3. Filter out the original business and keep top 3
                    rival_list = [r for r in rivals[0] if r.get('google_id') != my_biz[0].get('google_id')][:3]
                    
                    if rival_list:
                        st.session_state.found_rivals = {r['name']: r['google_id'] for r in rival_list}
                        status.update(label="Rivals Detected", state="complete")
                    else:
                        st.error("No similar businesses found within 1km.")
                except Exception as e:
                    st.error(f"Scan failed: {e}")
        else:
            st.warning("Please paste your link first.")

    # Step 2: Select and Compare
    if "found_rivals" in st.session_state:
        st.markdown("### Step 2: Select a Rival to Analyze")
        selected_rival_name = st.selectbox("Choose a competitor:", list(st.session_state.found_rivals.keys()))
        
        if st.button("Step 3: Run Full Comparison"):
            rival_id = st.session_state.found_rivals[selected_rival_name]
            rival_link = f"https://www.google.com/maps/place/?q=place_id:{rival_id}"
            
            with st.status(f"Analyzing {selected_rival_name}...") as status:
                # Fetching Data for the comparison
                data_a = out_client.google_maps_reviews(u1, reviews_limit=15)
                data_b = out_client.google_maps_reviews(rival_link, reviews_limit=15)
                
                n1, n2 = data_a[0]['name'], data_b[0]['name']
                
                prompt = f"""
                Compare {n1} and {n2}.
                1. Table comparing Service, Price, and Quality (Score 1-10).
                2. 'Revenue Leak': Explain why customers might leave {n1} for {n2}.
                3. '30-Day Plan': 3 steps for {n1} to win.
                """
                
                res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":prompt}])
                
                status.update(label="Analysis Complete", state="complete")
                
                st.markdown(f"### Results: {n1} vs {n2}")
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown(res.choices[0].message.content)
                st.markdown('</div>', unsafe_allow_html=True)
