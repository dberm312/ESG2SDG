# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 16:43:04 2020

@author: Berma
"""
#%%
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
#%%
class SDGs():
    def __init__(self):       
        url = 'https://github.com/IBM/Semantic-Search-for-Sustainable-Development/raw/master/src/targets.txt'
        text= requests.get(url).text.split('\n')
        SDGs = {}
        for i in text:
            i = i.split()
            SDGs[i[0]]=''.join([j+' ' for j in i[1:]])[:-1]
        del(i,text,url)
        self.SDGs = SDGs
        self.Env_tar = ['1.4', '1.5', '11.2', '11.3', '11.4', '11.5', '11.6', '11.7', '11.b', '11.c', '12.1', '12.2', '12.3', '12.4', '12.5', '12.6', '12.7', '12.8', '12.a', '12.b', '12.c', '13.1', '13.2', '13.3', '13.a', '13.b', '14.1', '14.2', '14.3', '14.4', '14.5', '14.6', '14.7', '14.a', '14.c', '15.1', '15.2', '15.3', '15.4', '15.5', '15.6', '15.7', '15.8', '15.9', '15.a', '15.b', '15.c', '16.8', '17.14', '17.7', '17.9', '2.4', '2.5', '3.9', '4.7', '5.a', '6.1', '6.3', '6.4', '6.5', '6.6', '6.a', '6.b', '7.1', '7.2', '7.3', '7.a', '7.b', '8.4', '8.9', '9.4']
    def Vectorize(self):
        '''
        Returns
        -------
        returns DataFrame with words and SDG targets.
        '''
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(self.SDGs.values())
        return(pd.DataFrame(X.todense(),index = self.SDGs.keys(),columns = vectorizer.get_feature_names()).T)