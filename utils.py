import requests
from transformers import pipeline
import re
from bs4 import BeautifulSoup
from newspaper import Article
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from collections import Counter
from gtts import gTTS
from deep_translator import GoogleTranslator
import os


analyzer = SentimentIntensityAnalyzer()
sentiment_model = pipeline("sentiment-analysis")


import requests

API_KEY = "351f22ae0cbc4d7685f59bd4584d6666"  # Replace with your actual NewsAPI key
NEWS_URL = "https://newsapi.org/v2/everything"

def fetch_news(company):
    params = {
        "q": company,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": API_KEY
    }

    response = requests.get(NEWS_URL, params=params)
    data = response.json()

    if data.get("status") == "ok":
        articles = [
            {"title": article["title"], "url": article["url"]}
            for article in data.get("articles", [])[:10]
        ]
        return articles
    return []
    

def get_news_articles(company_name):
    search_url = f"https://www.google.com/search?q={company_name}+news"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    articles = []
    
    for result in soup.find_all("div", class_="tF2Cxc"):
        title = result.find("h3").text if result.find("h3") else "No Title"
        link = result.find("a")["href"] if result.find("a") else "#"
        
        article_data = {
            "title": title,
            "link": link,
            "summary": summarize_article(link)
        }
        articles.append(article_data)
    
    return articles

from newspaper import Article

def summarize_article(url):
    """Extracts and summarizes full content from a news article URL."""
    try:
        article = Article(url)
        article.download()
        article.parse()

        # Use first 300 characters as a simple summary
        summary = article.text[:300] if article.text else "Summary not available."

        return summary
    except Exception as e:
        print(f"Error summarizing article: {e}")
        return "Summary not available."
    
def analyze_sentiment(text):
    """Perform sentiment analysis using both VADER and Transformers."""
    if not text or text == "Summary not available.":
        return "Neutral"

    vader_score = analyzer.polarity_scores(text)["compound"]
    hf_result = sentiment_model(text[:512])[0]["label"]  # First 512 chars

    if vader_score >= 0.05 and hf_result == "POSITIVE":
        return "Positive"
    elif vader_score <= -0.05 and hf_result == "NEGATIVE":
        return "Negative"
    else:
        return "Neutral"

def comparative_analysis(articles):
    """
    Performs comparative sentiment analysis on multiple articles.
    Returns structured sentiment distribution and topic overlap.
    """
    sentiment_counts = Counter([article["sentiment"] for article in articles])

    comparisons = []
    topics = [set(article["topics"]) for article in articles]

    for i in range(len(articles) - 1):
        comparison = {
            "Comparison": f"Article {i+1} vs Article {i+2}",
            "Sentiment Impact": f"{articles[i]['sentiment']} vs {articles[i+1]['sentiment']}",
            "Topic Overlap": topics[i].intersection(topics[i+1]),
            "Unique Topics in Article 1": topics[i] - topics[i+1],
            "Unique Topics in Article 2": topics[i+1] - topics[i],
        }
        comparisons.append(comparison)

    return {
        "Sentiment Distribution": dict(sentiment_counts),
        "Coverage Differences": comparisons
    }    
    
def generate_hindi_tts(text, filename="hindi_speech.mp3"):
    """Convert English summary to Hindi and generate speech."""
    
    # Translate English text to Hindi for audio
    translated_text = GoogleTranslator(source="en", target="hi").translate(text)

    # Generate Hindi speech
    tts = gTTS(translated_text, lang="hi")
    tts.save(filename)
    
    return filename    

    
        

if __name__ == "__main__":
    company = "Tesla"
    news = get_news_articles(company)
    for article in news:
        print(article)

