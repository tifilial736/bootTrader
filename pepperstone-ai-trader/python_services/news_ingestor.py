# news_ingestor.py
%%writefile news_ingestor.py
import os
import requests
import json

NEWSAPI_KEY = "COLOQUE_SUA_CHAVE_AQUI"

def get_news(query="forex", page_size=10):
    if not NEWSAPI_KEY:
        raise ValueError("A NEWSAPI_KEY válida é necessária")
    
    url = f"https://newsapi.org/v2/everything?q={query}&pageSize={page_size}&apiKey={NEWSAPI_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Erro ao buscar notícias: {response.status_code}")
    
    data = response.json()
    news_list = []
    for article in data.get("articles", []):
        news_list.append({
            "title": article["title"],
            "description": article["description"],
            "publishedAt": article["publishedAt"]
        })
    return news_list

def save_news(news, path="news_in/news_feed.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf8") as f:
        json.dump(news, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    news = get_news()
    save_news(news)
    print(f"Salvas {len(news)} notícias em news_in/news_feed.json")
