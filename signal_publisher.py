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
            # Simulação de decisão baseada no título
            action = "BUY" if "up" in article.get("title","").lower() else "SELL"
            writer.writerow(["EURUSD", action, 0.01, 0.7, int(time.time())])
    print(f"Sinais salvos em {output_csv}")

if __name__ == "__main__":
    news = load_processed_news()
    generate_signals(news)
