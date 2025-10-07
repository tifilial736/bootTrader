# trading_executor.py
from binance.client import Client
import json, time

# 🔑 Carrega API Key do arquivo config.json
with open("config.json") as f:
    cfg = json.load(f)

client = Client(cfg["api_key"], cfg["api_secret"], testnet=True)

def execute_trade(symbol, side, qty):
    """Executa ordem de compra/venda via Binance Testnet"""
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=qty
        )
        print(f"✅ Ordem executada: {side} {symbol} {qty}")
        return order
    except Exception as e:
        print(f"❌ Erro ao enviar ordem: {e}")

if __name__ == "__main__":
    execute_trade("BTCUSDT", "BUY", 0.001)
