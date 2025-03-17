from fastapi import FastAPI
from utils import fetch_news, summarize_article, analyze_sentiment, comparative_analysis, generate_hindi_tts
from pydantic import BaseModel

app = FastAPI()

# Define input model
class NewsRequest(BaseModel):
    company_name: str

@app.post("/get_news")
def get_news(data: NewsRequest):
    """
    Fetches news articles, summarizes them, and analyzes sentiment.
    Returns structured sentiment data.
    """
    company_name = data.company_name
    articles = fetch_news(company_name)

    if not articles:
        return {"error": "No articles found"}

    processed_articles = []
    for article in articles:
        summary = summarize_article(article["url"])
        sentiment = analyze_sentiment(summary)
        
        processed_articles.append({
            "title": article["title"],
            "summary": summary,
            "sentiment": sentiment,
            "topics": ["Business", "Market"]  # Placeholder topics
        })

    # Perform comparative analysis
    analysis = comparative_analysis(processed_articles)

    return {
        "company": company_name,
        "articles": processed_articles,
        "comparative_analysis": analysis
    }

@app.post("/generate_tts")
def generate_tts(data: NewsRequest):
    """
    Converts sentiment report into Hindi speech.
    Returns the file path.
    """
    text = f"Company: {data.company_name}. Sentiment Analysis completed."
    filename = generate_hindi_tts(text)
    return {"tts_file": filename}

