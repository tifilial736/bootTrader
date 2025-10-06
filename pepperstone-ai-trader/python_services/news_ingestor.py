# news_ingestor.py
import os, time, json, requests, feedparser
from datetime import datetime


NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')
RSS_SOURCES = [
'https://www.reutersagency.com/feed/?best-topics=markets',
'https://feeds.finance.yahoo.com/rss/2.0/headline?s=EURUSD',
]
OUT_DIR = os.getenv('NEWS_IN_DIR','/tmp/news_in')
os.makedirs(OUT_DIR, exist_ok=True)


def fetch_newsapi(q='forex OR EURUSD'):
if not NEWSAPI_KEY:
return []
url = ('https://newsapi.org/v2/everything?'
f'q={q}&language=en&pageSize=50&apiKey={NEWSAPI_KEY}')
r = requests.get(url, timeout=10)
if r.status_code==200:
return r.json().get('articles', [])
return []


def fetch_rss(url):
d = feedparser.parse(url)
items = []
for e in d.entries:
items.append({
'title': e.get('title',''),
'link': e.get('link',''),
'published': e.get('published',''),
'summary': e.get('summary','')
})
return items




def normalize_article(a):
uid = a.get('url') or a.get('link') or (a.get('title','') + str(time.time()))
return {
'id': uid.replace('/','_').replace('\\','_'),
'title': a.get('title') or a.get('title',''),
'text': (a.get('description') or a.get('content') or a.get('summary') or '')[:4000],
'source': (a.get('source',{}).get('name') if isinstance(a.get('source'), dict) else a.get('source','')),
'published_at': a.get('publishedAt') or a.get('published') or datetime.utcnow().isoformat()
}




def main_loop():
main_loop()