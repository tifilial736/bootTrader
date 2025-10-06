# inference_service.py
from fastapi import FastAPI
import uvicorn, joblib, numpy as np


app = FastAPI()
# Carregue seu modelo treinado (XGBoost/LightGBM/Sklearn)
MODEL_PATH = '/app/model/model_xgb.joblib'
model = None
try:
model = joblib.load(MODEL_PATH)
except Exception as e:
print('Model not found, run training first', e)


@app.post('/predict')
def predict(payload: dict):
# payload: { 'embedding': [...], 'sentiment_score': float, 'recent_return': float }
emb = np.array(payload.get('embedding',[]))
sent = float(payload.get('sentiment_score',0.0))
recent = float(payload.get('recent_return',0.0))
feat = np.concatenate([emb, [sent, recent]])
prob = float(model.predict_proba(feat.reshape(1,-1))[0,1])
return {'prob_up': prob}


if __name__=='__main__':
uvicorn.run(app, host='0.0.0.0', port=8000)