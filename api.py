from dotenv import load_dotenv
import os
import requests
from newspaper import Article
from newspaper.article import ArticleException

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API")
URL = "https://newsapi.org/v2/everything"

def fetch_news(query):
    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY not found in environment variables")
        
    params = {
        "apiKey": NEWS_API_KEY,
        "q": query,
        "sortBy": "publishedAt",
        "pageSize": 5,
        "language": "en"
    }

    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        articles = []

        for item in data.get("articles", []):
            try:
                article = Article(item["url"])
                article.download()
                article.parse()

                articles.append({
                    "title": article.title or item["title"],
                    "content": article.text or item["content"],
                    "url": item["url"],
                    "source": item["source"]["name"],
                    "image": item.get("urlToImage"),
                    "publishedAt": item["publishedAt"]
                })
            except ArticleException as e:
                print(f"Skipping article due to error: {e}")
                # Add fallback content if article parsing fails
                articles.append({
                    "title": item["title"],
                    "content": item.get("content", "Content not available"),
                    "url": item["url"],
                    "source": item["source"]["name"],
                    "image": item.get("urlToImage"),
                    "publishedAt": item["publishedAt"]
                })
            except Exception as e:
                print(f"Unexpected error: {e}")

        return articles
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

categories = ["India", "US", "stock market", "health", "sports", "technology"]

for category in categories:
    print(f"\n===== {category.upper()} =====")
    news = fetch_news(category)
    if news:
        for article in news:
            print(f"• {article['title']}")
            print(f"  Source: {article['source']}")
            print(f"  Published At: {article['publishedAt']}")
            print(f"  Content Snippet: {article['content'][:300]}...\n")
    else:
        print("No articles found.\n")