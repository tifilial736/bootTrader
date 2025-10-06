# Criar todos os arquivos Python corrigidos de uma vez

# 1️⃣ news_ingestor.py
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

# 2️⃣ nlp_worker.py
%%writefile nlp_worker.py
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

# 3️⃣ signal_publisher.py
%%writefile signal_publisher.py
import os
import json
import csv
import time

def load_processed_news(path="news_out/news_processed.json"):
    with open(path, "r", encoding="utf8") as f:
        news = json.load(f)
    return news

def generate_signals(news, output_csv="signals/signals.csv"):
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    with open(output_csv, "w", newline="", encoding="utf8") as f:
        writer = csv.writer(f)
        writer.writerow(["symbol", "action", "lot", "confidence", "timestamp"])
        for article in news:
            action = "BUY" if "up" in article.get("title","").lower() else "SELL"
            writer.writerow(["EURUSD", action, 0.01, 0.7, int(time.time())])
    print(f"Sinais salvos em {output_csv}")

if __name__ == "__main__":
    news = load_processed_news()
    generate_signals(news)

# 4️⃣ inference_service.py
%%writefile inference_service.py
from fastapi import FastAPI
from signal_publisher import load_processed_news, generate_signals
import nest_asyncio
import uvicorn

app = FastAPI()

@app.get("/generate_signals")
def api_generate_signals():
    news = load_processed_news()
    generate_signals(news)
    return {"status": "Signals generated successfully"}

if __name__ == "__main__":
    nest_asyncio.apply()
    uvicorn.run(app, host="0.0.0.0", port=8000)
