# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 16:07:45 2020

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
from sklearn.metrics.pairwise import cosine_similarity as cos_sim
#%%
S = SnP_reader()
texts = S.Sector2Text('Real Estate')
#text =''.join(texts)
text_list = nltk.tokenize.sent_tokenize(''.join(texts))
wv = api.load('word2vec-google-news-300') # https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html#sphx-glr-auto-examples-tutorials-run-word2vec-py
#%%
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(text_list)
df = pd.DataFrame(data = vectorizer.vocabulary_.values(),index = vectorizer.vocabulary_.keys(),columns = ['count'])
df1 = pd.DataFrame(data = np.ones(len(wv.vocab)),index = wv.vocab.keys())
df2 = df.join(df1,how = 'inner')
df2['word'] = df2.index
df2['vec']=df2['word'].apply(lambda x:wv[x])
dfwv = df2[['word','vec']]
del(df,df1,df2,wv,text_list)
#%%
text_vec = pd.DataFrame(
    data= X.T.todense(),
    index = vectorizer.get_feature_names())
dfall = dfwv.join(text_vec,how='inner')
del(text_vec,dfwv,X)
#print(vectorizer.get_feature_names())
#%%
dfsdg = pd.DataFrame(
    data = vectorizer.transform(SDGs().SDGs.values()).T.todense(),
    index = vectorizer.get_feature_names(),
    columns = list(SDGs().SDGs.keys()))

dfall = dfall.join(dfsdg, how = 'left')
del(dfsdg)

#%%
dfall = dfall.drop(columns = ['word'])
Vec = pd.DataFrame(dfall['vec'])
dfall = dfall.drop(columns = ['vec'])
loc = list(dfall).index('1.1')
SnP_Txt = dfall[dfall.columns[:loc]]
SDG_Txt = dfall.drop(columns = dfall.columns[:loc])
del(dfall,loc)

#%%SnP Vectorization
out = []
for i in SnP_Txt.columns:
    out.append(np.array(SnP_Txt[i]*Vec['vec']).T.sum())
    if(i%np.floor(len(SnP_Txt.columns)/100)==0):
        print(np.round(i/len(SnP_Txt.columns,2))
SnP_Vec = pd.DataFrame(out,index = SnP_Txt.columns)
del(out,i)

#%%SDG sentance Vectorization
out = []
for i in SDG_Txt.columns:
    out.append(np.array(SDG_Txt[i]*Vec['vec']).T.sum())
SDG_Vec = pd.DataFrame(out,index = SDG_Txt.columns)
del(i,out)
SDG_sim = pd.DataFrame(
    data = cos_sim(SDG_Vec.values),
    index = SDG_Txt.columns,
    columns = SDG_Txt.columns).stack()
SDG_sim=SDG_sim[SDG_sim<0.999999].drop_duplicates().sort_values(ascending=False)
pd.DataFrame(SDG_sim.head(100),columns = ['sim']).to_csv('SDG_sim.csv')

#%%
sim = cos_sim(SDG_Vec.values,SnP_Vec.values)
sim = pd.DataFrame(
    data = sim,
    index = SDG_Txt.columns).T

#%%
hold1=[]
for i in SDG_Txt.columns:
    hold = sim[i].sort_values(ascending=False).head(3).mean()
    hold1.append(hold)
hold2 = pd.DataFrame(data = hold1,index = SDG_Txt.columns,columns = ['cat']).sort_values('cat',ascending=False)
print(hold2.head(25))
hold2.to_csv('Real_Estate.csv')