# train_pipeline.py
# Pipeline para juntar notícias + candles e treinar um XGBoost
import joblib, numpy as np, pandas as pd
from sklearn.model_selection import TimeSeriesSplit
import xgboost as xgb


# Este arquivo é um esqueleto: você precisa juntar
# 1) /tmp/news_out/*.json -> extrair embedding, sentiment
# 2) candles históricos (MT5 ou provedor) -> calcular return futuro e label
# Depois: treinar e salvar model_xgb.joblib


# pseudocódigo simplificado


def load_features_news(folder='/tmp/news_out'):
# cole aqui: leitura dos jsons, retornar df com embedding e sentiment
pass


if __name__=='__main__':
print('Preencha o pipeline com seus dados históricos e rode treinamento')