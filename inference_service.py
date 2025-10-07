from fastapi import FastAPI
import nest_asyncio
import uvicorn
import joblib
import os
from signal_publisher import load_processed_news, generate_signals

app = FastAPI()

MODEL_PATH = "model.pkl"

# Carregar modelo de forma segura
try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    print("Modelo não encontrado, treine antes de usar")
    model = None

@app.get("/generate_signals")
def api_generate_signals():
    news = load_processed_news()
    generate_signals(news)
    return {"status": "Signals generated successfully"}

if __name__ == "__main__":
    nest_asyncio.apply()
    uvicorn.run(app, host="0.0.0.0", port=8000)
