# nlp_worker.py
import os, json, time
from sentence_transformers import SentenceTransformer
from transformers import pipeline


IN_DIR = os.getenv('NEWS_IN_DIR','/tmp/news_in')
OUT_DIR = os.getenv('NEWS_OUT_DIR','/tmp/news_out')
os.makedirs(OUT_DIR, exist_ok=True)


EMB_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
SENT = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')


def process_file(path):
with open(path,'r',encoding='utf8') as f:
art = json.load(f)
text = (art.get('title','') + '. ' + art.get('text',''))[:2000]
emb = EMB_MODEL.encode(text).tolist()
sent = SENT(text[:512])[0]
out = {
'id': art['id'], 'title': art['title'], 'source': art['source'],
'published_at': art['published_at'], 'sentiment_label': sent['label'],
'sentiment_score': float(sent['score']), 'embedding': emb
}
with open(os.path.join(OUT_DIR, os.path.basename(path)),'w',encoding='utf8') as f:
json.dump(out,f,ensure_ascii=False)
os.remove(path)




def loop():
while True:
files = sorted([f for f in os.listdir(IN_DIR)])[:50]
for fn in files:
try:
process_file(os.path.join(IN_DIR,fn))
except Exception as e:
print('nlp error', e)
time.sleep(0.5)


if __name__=='__main__':
loop()