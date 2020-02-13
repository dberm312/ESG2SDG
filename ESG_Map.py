# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 12:17:40 2020

@author: Berma
"""
#%%
import nltk
#nltk.download('punkt')
from SnP_Report_Scraping import SnP_reader
from sklearn.feature_extraction.text import TfidfVectorizer
from SDG_Scraping import SDGs
import pandas as pd
import numpy as np
import gensim.downloader as api
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity as cos_sim
#%%
snp = SnP_reader()
sdg = SDGs()
text = snp.lst2Text(['msft','aapl','amzn','fb','goog'])
text = [i+' ' for i in text]
text = ''.join(text)
text = text.replace('\n',' ').replace('\xa0', ' ')
print('read text')
text_list=nltk.tokenize.sent_tokenize(text)
print('text_tokenized')
del(text)
#%%
snp_vectorizor = TfidfVectorizer()
snp_vec = snp_vectorizor.fit_transform(text_list)
snp_vec = pd.DataFrame(
    data = snp_vec.todense(),
    columns = snp_vectorizor.get_feature_names()).T

sdg_vectorizor = TfidfVectorizer()
sdg_vec = sdg_vectorizor.fit_transform(sdg.SDGs.values())
sdg_vec = pd.DataFrame(
    data = sdg_vec.todense(),
    columns = sdg_vectorizor.get_feature_names(),
    index = sdg.SDGs.keys()).T
print('vectorized')
#%%
model = Word2Vec(api.load("text8"))#.wv
wv = model.wv
del(model)
print('wv model loaded')

sdg_vec = sdg_vec[sdg_vec.index.isin(wv.vocab.keys())]
snp_vec = snp_vec[snp_vec.index.isin(wv.vocab.keys())]

sdg_vec['vec'] = [wv[i] for i in sdg_vec.index]
snp_vec['vec'] = [wv[i] for i in snp_vec.index]
print('final vector')
del(wv)
#%%
snp_out = []
for i in snp_vec.columns[:-1]:
    snp_out.append(np.array([np.array(i) for i in (snp_vec[i]*snp_vec['vec'])]).sum(axis=0))
    if(i%np.floor(len(snp_vec.columns)/100)==0):
        print(np.round(i/len(snp_vec.columns),2))
snp_out = np.array(snp_out)

sdg_out = []
for i in sdg_vec.columns[:-1]:
    sdg_out.append(np.array([np.array(i) for i in (sdg_vec[i]*sdg_vec['vec'])]).sum(axis=0))
del(i,snp,snp_vec,snp_vectorizor,sdg,sdg_vectorizor)
sdg_out = np.array(sdg_out)

Report_sim_table = pd.DataFrame(
    data = cos_sim(snp_out),
    columns = snp_vec.columns[:-1],
    index = snp_vec.columns[:-1])
#hold = (Report_sim_table<0.75).mean()<0.98
hold = ((Report_sim_table<0.80).mean()>0.9)

Report2sdg_sim_table = pd.DataFrame(
    data = cos_sim(snp_out,sdg_out),
    columns = sdg_vec.columns[:-1],
    index = snp_vec.columns[:-1])
print(Report2sdg_sim_table.stack().sort_values(ascending=False).head(10))
Report2sdg_sim_table[hold]
#%%
out = pd.DataFrame(
    data = np.zeros((5,5)),
    index = [0.75,0.8,0.85,0.9,0.95],
    columns = [0.75,0.8,0.85,0.9,0.95])
for i in out.columns:
    for j in out.index:
        out.loc[i][j] = ((Report_sim_table<i).mean()>j).mean()
print(out)