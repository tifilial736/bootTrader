# signal_publisher.py
import os, json, time
OUT_DIR = os.getenv('SIGNAL_DIR','C:\\signal_folder') # use pasta acessível pelo MT5 (Windows path)
os.makedirs(OUT_DIR, exist_ok=True)


THRESH = float(os.getenv('CONF_THRESHOLD','0.65'))
MAX_LOT = float(os.getenv('MAX_LOT','0.1'))


# exemplo simples: gera csvs com formato: SYMBOL,SIDE,LOT,CONF,TS


def publish(symbol, side, confidence, lot):
ts = int(time.time())
fn = os.path.join(OUT_DIR, f"signal_{symbol.replace('/','')}_{ts}.csv")
with open(fn,'w',encoding='utf8') as f:
f.write(','.join([symbol, side, str(lot), str(confidence), str(ts)]))
return fn


# loop integrador: monitora /tmp/news_out, chama inference, publica sinal
import requests
IN_DIR = os.getenv('NEWS_OUT_DIR','/tmp/news_out')
INF_URL = os.getenv('INF_URL','http://127.0.0.1:8000/predict')


import glob


def main_loop():
while True:
files = sorted(glob.glob(os.path.join(IN_DIR,'*.json')))[:20]
for p in files:
try:
with open(p,'r',encoding='utf8') as f:
j = json.load(f)
payload = {'embedding': j['embedding'], 'sentiment_score': j['sentiment_score'], 'recent_return': 0.0}
r = requests.post(INF_URL, json=payload, timeout=5)
if r.status_code==200:
prob = r.json().get('prob_up',0.0)
if prob >= THRESH:
publish('EURUSD','BUY', prob, MAX_LOT)
elif prob <= (1-THRESH):
publish('EURUSD','SELL', 1-prob, MAX_LOT)
os.remove(p)
except Exception as e:
print('publisher error', e)
time.sleep(0.5)


if __name__=='__main__':
main_loop()