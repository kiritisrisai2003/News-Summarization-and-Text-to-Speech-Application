import streamlit as st
from utils import fetch_news, summarize_article, analyze_sentiment, comparative_analysis, generate_hindi_tts
import os

st.title("📰 News Summarization & Sentiment Analysis with Hindi TTS")
st.markdown("### Enter a company name to fetch news articles and analyze sentiment.")

# Input box for the company name
company_name = st.text_input("Enter Company Name:", "")

if company_name:
    st.markdown(f"### Fetching News for: {company_name}")

    # Step 1: Get News Articles
    articles = fetch_news(company_name)
    print("Fetched Articles:", articles)  # Debugging: Check if articles are fetched

    if not articles:
        st.warning("No articles found. Try another company name.")
    else:
        processed_articles = []

        for article in articles:
            st.subheader(article["title"])
            summary = summarize_article(article["url"])
            sentiment = analyze_sentiment(summary)

            # Display article info
            st.write(f"**Summary:** {summary}")
            st.write(f"**Sentiment:** {sentiment}")

            # Store processed article
            processed_articles.append({
                "title": article["title"],
                "summary": summary,
                "sentiment": sentiment,
                "topics": ["Business", "Market"]  # Placeholder topics
            })

        # Step 2: Perform Comparative Analysis
        st.markdown("## 📊 Comparative Analysis")
        analysis = comparative_analysis(processed_articles)
        st.json(analysis)

        # Step 3: Generate Hindi TTS
        final_summary = f"Company: {company_name}. Sentiment Report: {analysis['Sentiment Distribution']}."
        tts_file = generate_hindi_tts(final_summary)

        # Step 4: Play Hindi Speech Output
        st.audio(tts_file, format="audio/mp3", start_time=0)
        st.success("✅ Hindi Speech Generated! Click play to listen.")

# Footer
st.markdown("---")
st.markdown("Developed with ❤️ using Streamlit, NLP & TTS.")
