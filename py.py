#!/usr/bin/env python
# coding: utf-8

# In[1]:


from collections import defaultdict
from datetime import datetime as dt
from pathlib import Path
from sysconfig import get_python_version
from tkinter.tix import DisplayStyle
from flask import Flask, render_template
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
from IPython.core.display import HTML
from matplotlib import pyplot as plt
from scipy import stats
import pymongo
import matplotlib.pyplot as plt, mpld3




# In[2]:



def toDICT(KEYS, OPES, DICT):
    for OPE in OPES:
        for KEY in KEYS:
            DICT[KEY].append(OPE.get(KEY))
    return DICT

def toDF(DICT):
    DF = pd.DataFrame(data=DICT)
    DF['date'] = DF['date'].apply(convDATE)
    DF['amount'] = DF['amount'].apply(float).apply(abs)

    DF['vol'] = DF['wording'].apply(getVolDist, args=['v']).apply(np.float32)
    DF['vol'] = DF['vol'].apply(lambda x: round(x, 2))

    DF['dist'] = DF['wording'].apply(getVolDist, args=['d']).apply(np.int32)
    DF.drop(columns=['wording'], inplace=True)
    DF.sort_values('date', inplace=True)
    DF['kms'] = DF['dist'].diff(periods=-1)
    DF['kms'] = DF['kms'].apply(abs)
    DF['px/l'] = round(DF['amount'] / DF['vol'], 3)
    DF['cum kms'] = DF['kms'].cumsum()
    DF['cum vol'] = DF['vol'].cumsum()
    DF['conso'] = round(DF['cum vol'] * 100 / DF['cum kms'], 2)
    consommation = round(DF['cum vol'] * 100 / DF['cum kms'], 2)
    DF.fillna(value=0, inplace=True)
    return DF
   
def convDATE(i):
    return dt.fromordinal(int(i))

def getVolDist(s, k):
    s = s.split(' ')
    d = {x.split('=')[0]: x.split('=')[1] for x in s}
    return d.get(k)


# In[9]:

from IPython.display import HTML


FILE = Path(r'C:\Users\Mohamed\Desktop\operations.xml.txt')
XML = bs(FILE.read_text(), features='xml')

OPES = XML.findAll(name='ope', attrs={'category': '185'})
KEYS = ['date','amount','vol','dist','wording']
DICT = defaultdict(list)
DICT = toDICT(KEYS, OPES, DICT)
DF = toDF(DICT)
HTML(DF.to_html())
print(DF)
html = DF.to_html()
  
text_file = open("C:/Users/Mohamed/Desktop/inpro+/front/src/app/app.component.html", "w")
text_file.write(html)
text_file.close()

from pymongo import MongoClient 
myclient = MongoClient("mongodb://localhost:27017/")
db = myclient["inpro"]
collection = db["tabs"]
mylist=[DICT]
x=collection.insert_many(mylist)
dblist = myclient.list_database_names()
if "inpro" in dblist:
  print("The database exists.")
print(x)
# In[11]:


fig, axe = plt.subplots(figsize=(10.6,8))
x = DF.iloc[:-1]['date'].dt.strftime('%Y-%m-%d')
y = DF.iloc[:-1]['conso']
axe.bar(x, y, label='Consommation', color='#1B80EA')
axe.set_ylabel('Consommation')
axe.set_xlabel('Période')
axe.set_ylim(int(DF.iloc[:-1]['conso'].min()))
axe.set_title('In Pro+: Conso moyenne: {} l/100kms'.format(round(DF.iloc[:-1].conso.mean(), 2)))
fig.autofmt_xdate()
_x = DF.iloc[:-1].index
lr = stats.linregress(_x, y)
axe.plot(x, lr.intercept + lr.slope * _x, marker='.', color='r', label='Tendance Consommation')
axe.legend(loc='upper left')
ax2 = axe.twinx()
y = DF.iloc[:-1]['px/l']
ax2.plot(x, y, color='#C7A986', marker='o', label='px/l')
ax2.set_ylabel('Prix au litre')
ax2.legend(loc='lower right')
plt.show()
plt.show()


# In[12]:


R = DF.resample('M',on='date')
DF2 = R.agg({'amount':sum,'vol':sum,'dist':max,'kms':sum,'px/l':np.mean,'cum kms':max,'cum vol':max,'conso':np.mean})
DF2['conso'] = DF2['conso'].apply(lambda x: round(x, 2))
DF2['px/l'] = DF2['px/l'].apply(lambda x: round(x, 3))
DF2['kms'] = DF2['kms'].apply(int)
DF2['cum kms'] = DF2['cum kms'].apply(int)
HTML(DF2.to_html())

HTML(DF2.to_html())

print(DF2)
html = DF2.to_html()
  
text_file = open("index1.html", "w")
text_file.write(html)
text_file.close()





