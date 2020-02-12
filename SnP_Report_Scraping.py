# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 11:06:24 2020

@author: Berma
"""
#%%
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import time
#%%
class SnP_reader():
    def __init__(self):
        '''
        Returns
        -------
        None.

        '''
        self.SnP_table= pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
        self.SnP_table = self.SnP_table[['Symbol','Security','GICS Sector','GICS Sub Industry']]
        self.broken = ['O','CTVA','VZ']#broken tickers are tickers which do not properly pull for the SECs website
        
    def Sectors(self):
        '''
        Returns
        -------
        DataFrame of all the sectors in S&P along with the number of compaines in each group.

        '''
        return(self.SnP_table.groupby('GICS Sector').count()['Symbol'].sort_values(ascending=False))
    
    def Sym210k(self, Sym):
        '''

        Parameters
        ----------
        Sym : str
            Ticker Symbol of Company.
        Returns
        -------
        The text of the most recent 10-K with the company submitted.

        '''
        #Getting the CIK
        url = 'https://www.sec.gov/cgi-bin/browse-edgar?CIK={}&action=getcompany'.format(Sym)
        target = requests.get(url)
        soup = BeautifulSoup(target.text,'html.parser')
        CIK = soup.get_text().split()[soup.get_text().split().index('CIK#:')+1]
        
        #Getting SEC Accession_No
        url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=&dateb=&owner=exclude&count=100'.format(CIK)
        table = pd.read_html(url)[-1]
        adjT = table[table['Filings']=='10-K'].iloc[0]
        l = adjT['Description'].replace(']', ' ').split()
        SECA = (l[1+l.index('Acc-no:')])
        
        #Get 10k Location
        SECA1 = SECA.replace('-','')
        #https://www.sec.gov/Archives/edgar/data/66740/000155837020000581/0001558370-20-000581-index.htm
        url = 'https://www.sec.gov/Archives/edgar/data/{}/{}/{}-index.htm'.format(str(int(CIK)),SECA1,SECA)
        table = pd.read_html(url)[0]
        loc = table.iloc[0,2].split()[0]
        
        #Get 10K Text
        url = 'https://www.sec.gov/Archives/edgar/data/{}/{}/{}'.format(str(int(CIK)),SECA1,loc)
        target = requests.get(url)
        soup = BeautifulSoup(target.text,'lxml')
        text = soup.get_text()
        return(text)
        
    def lst2Text(self, lstSym):
        '''
        Parameters
        ----------
        lstSym : List of Stings
            List of strings of stock tickers which you are examining(e.g. ['MMM','AAPL','SPG']).
        Returns
        -------
        One string of all the text found in the annual reports of the companies quaried.

        '''
        out = []
        count = 0
        for i,j in enumerate(lstSym):
            print(j,np.round(i/len(lstSym),2))
            if(j not in self.broken):
                out.append(self.Sym210k(j))
        return(out)
    
    def Sector2Text(self,Sector):
        '''
        Parameters
        ----------
        Sector : str
            One of the 'GICS Sector' in the 'SnP_table'.
            for example 'Real Estate'
        Returns
        -------
        All the text associated with that Sector.
        '''
        lst = self.SnP_table[self.SnP_table['GICS Sector']==Sector]['Symbol'].values
        return(self.lst2Text(lst))
    
if(__name__=='__main__'):
    s=SnP_reader()    
#%%
'''
Sym='SPG'
url = 'https://www.sec.gov/cgi-bin/browse-edgar?CIK={}&action=getcompany'.format(Sym)
target = requests.get(url)
soup = BeautifulSoup(target.text,'html.parser')
CIK = soup.get_text().split()[soup.get_text().split().index('CIK#:')+1]

#Getting SEC Accession_No
url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=&dateb=&owner=exclude&count=100'.format(CIK)
table = pd.read_html(url)[-1]
adjT = table[table['Filings']=='10-K'].iloc[0]
l = adjT['Description'].replace(']', ' ').split()
SECA = (l[1+l.index('Acc-no:')])

#Get 10k Location
SECA1 = SECA.replace('-','')
#https://www.sec.gov/Archives/edgar/data/66740/000155837020000581/0001558370-20-000581-index.htm
url = 'https://www.sec.gov/Archives/edgar/data/{}/{}/{}-index.htm'.format(str(int(CIK)),SECA1,SECA)
table = pd.read_html(url)[0]
loc = table.iloc[0,2].split()[0]

#Get 10K Text
url = 'https://www.sec.gov/Archives/edgar/data/{}/{}/{}'.format(str(int(CIK)),SECA1,loc)
target = requests.get(url)
soup = BeautifulSoup(target.text,'lxml')
text = soup.get_text()
#return(text)
'''