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
