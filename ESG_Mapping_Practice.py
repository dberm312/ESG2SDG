# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 23:54:56 2020

@author: Berma
"""
#%%
from Mapping_util import *
import nltk
#nltk.download('punkt')
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import gensim.downloader as api
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity as cos_sim
import requests
#%%
sdgs = SDGs().sdgs

#text = SnP_reader().Sector2Text('Energy')
text = SnP_reader().lst2Text(['aapl','fb','goog','msft'])
text = [i+' ' for i in text]
text = ''.join(text)
text = text.replace('\n',' ').replace('\xa0', ' ')
print('read text')
text_list=nltk.tokenize.sent_tokenize(text)
text_dict = dict(zip(range(len(text_list)),text_list))
print('text tokenized')
del(text,text_list)

model = Word2Vec(api.load("text8"))#.wv
wv = model.wv
#wv = api.load('word2vec-google-news-300') 
del(model)
print('wv model loaded')
#%%
text_vec = vectorize(text_dict,wv)
sdgs_vec = vectorize(sdgs,wv)
#%%
text_sim = similarity(text_vec)
new_text_dict = dict(pd.Series(text_dict)[(text_sim<0.75).mean()>0.95].reset_index()[0])
#%%
new_text_vec = vectorize(new_text_dict,wv)
#%%
new_sim = similarity(new_text_vec,sdgs_vec).stack().sort_values(ascending=False).head(100)
out = []
for i,j in new_sim.index:
    out.append((new_text_dict[i],sdgs[j]))
out = pd.DataFrame(
    data = out,
    columns = ['text','sdg'])
out.to_csv('Energy.csv')
#%%
out = {}
for i in sim.columns:
    out[i] = sim[i].sort_values(ascending=False).head(10).mean()
out = pd.Series(out).sort_values(ascending=False).head(10)
print(out)