import os
import json
from sentence_transformers import SentenceTransformer

def load_news(path="news_in/news_feed.json"):
    with open(path, "r", encoding="utf8") as f:
        news = json.load(f)
    return news

def process_news(news):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    for article in news:
        text = (article.get("title","") + " " + article.get("description","")).strip()
        article["embedding"] = model.encode(text).tolist()
    return news

def save_processed(news, path="news_out/news_processed.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf8") as f:
        json.dump(news, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    news = load_news()
    processed = process_news(news)
    save_processed(processed)
    print(f"Processadas {len(processed)} notícias em news_out/news_processed.json")
