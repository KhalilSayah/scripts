#!/usr/bin/env python
# coding: utf-8

# In[16]:


from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import urllib.parse
from concurrent.futures import ThreadPoolExecutor


# In[17]:


#Load file 
file_ = open('mydata.json', 'r')
Json_object = json.load(file_)


# In[18]:


#Scrap data from domain
#Data bellow : output_data = [{ville,secteur,links[]}]
def get_num(data):
    encoded_data = urllib.parse.quote(data)
    url = 'https://www.pages-annuaire.net/ajax/getMERNumber?tag=F_PRO_DSK_SEO&encodeData='+encoded_data
    Headers = {'X-Requested-With':'XMLHttpRequest'}
    res = requests.get(url, headers=Headers)
    num = res.content
    num = str(num).replace('b','').replace("'", "")
    return num
    


def pdp(url,s):
    req = s.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    try:
        t = soup.select('html body div.col-md-6 h1')
        title = t[0].text
        a = soup.select('html body div.col-md-6 h2')
        adresse = a[0].text
        b = soup.select('html body div.btn.text-uppercase.btn-numero')
        btn_data = b[0].attrs['data']
        num = get_num(btn_data)
        
    except:
        title = 'None'
        adresse = 'None'
        num = 'None'
    
    data = {
        'Title : ' : title,
        'Adresse : ': adresse,
        'Number : ': num
    }
    
    print(title + ' has been scraped')
    
    
    return title,adresse,num


# In[25]:


def fetch(link):
    s = requests.Session()
    t,a,n = pdp(link,s)
    domain = {
        'Title':t,
        'Ville':output_data[i]['Ville'],
        'Secteur':output_data[i]['Secteur'],
        'Adresse':a,
        'Numero':n
        }
    out = domain + ','
    with open('dump.json','w') as f:
        f.write(out)
    


# In[ ]:



for i in range(len(Json_object)):
    #for link in output_data[i]['Links']:
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(fetch,Json_object[i]['Links'])

    


# In[ ]:




