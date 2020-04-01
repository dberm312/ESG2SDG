# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 13:06:59 2020

@author: Berma
"""
#%%
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import numpy as np
#%%
def url2SDGs(url):
    '''
    Parameters
    ----------
    url : str
        string of URL.

    Returns
    -------
    SDGs relevent.

    '''
    response = requests.get(url)
    soup = bs(response.content)
    a=soup.find_all('li',class_="selected_question")
    out = []
    for i in a:
        try:
            hold = i.find_all('p')[0].text.split(':')[0]
            if(hold[:3]=='SDG'):
                out.append(hold)
        except:
            pass
    return(out)

def url2listnums(url):
    #url = 'https://www.unglobalcompact.org/participation/report/cop/create-and-submit/active?page=1&per_page=250#paged_results'
    
    text = requests.get(url).text
    soup = bs(text)
    a = soup.find_all('tr')[1:]
    b=[i.find_all('a')[0]['href'].split('/')[-1] for i in a]
    return(b)
#%%
table = 'blank'
url = 'https://www.unglobalcompact.org/participation/report/cop/create-and-submit/active?page={}&per_page=250#paged_results'
go = True
count = 1
while(go):
    hold = pd.read_html(url.format(count))[0]
    hold['nums']=url2listnums(url.format(count))
    if(type(table)==str):
        table=hold
    else:
        table=table.append(hold)
    if(hold.shape[0]<250):
        go=False
    print(count)
    count+=1
table =table.reset_index().drop(columns=['index'])
#%%
table = table[table['Year']==2020].reset_index().drop(columns=['index'])
table =table.iloc[:,:5]
for i in range(1,18):
    i = 'SDG '+str(i)
    table[i]=np.zeros(table.shape[0])
    
url = 'https://www.unglobalcompact.org/participation/report/cop/create-and-submit/active/{}'
out = []
for i in range(table.shape[0])[:]:
    out.append(url2SDGs(url.format(table['nums'][i])))
    print(i)

for i in range(len(out)):
    for j in out[i]:
        table[j][i]=1
table['const']=np.ones(table.shape[0])
table1 = table.groupby('Sector').sum().iloc[:,-18:].sort_values('const',ascending=False).head(25)
