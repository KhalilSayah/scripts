#!/usr/bin/env python
# coding: utf-8

# In[4]:


get_ipython().system('pip3 install requests wget')


# In[65]:


from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import urllib.parse


# In[3]:


url_1 = 'https://www.pages-annuaire.net/pros'


# In[93]:


#Get Urls
links = []
req = requests.get(url_1)
soup = BeautifulSoup(req.content, 'html.parser')
links_container  = soup.select('html body div.listing-block-container a')
for link in links_container:
    url = 'https://www.pages-annuaire.net' + str(link.attrs['href'])
    links.append(url)
links.append('https://www.pages-annuaire.net/pros/ville/Paris')
links.append('https://www.pages-annuaire.net/pros/ville/Lyon')
links.append('https://www.pages-annuaire.net/pros/ville/Marseille')
print(len(links))


# In[94]:


def get_urls_cat(url):
    c_urls = []
    res = requests.get(url)
    r_soup = BeautifulSoup(res.content, 'html.parser')
    t = r_soup.select('html body div.container-categories a')
    
    for link in t:
        url_c = 'https://www.pages-annuaire.net'+str(link.attrs['href'])
        c_urls.append(url_c)
    
    print(url + ' Has been scraped')
    
    return c_urls



# In[95]:


def get_urls_domain(url): #url data[ville][....]
    
    data = []
    
    flag = 1 #Continue...
    i = 1 #initialising
    while flag:
        d_url = url + '?p=' + str(i)
        req = requests.get(d_url)
        soup = BeautifulSoup(req.content, 'html.parser')
        d = soup.select('html body div.col-xs-12.col-sm-6.abonne-container a')
        if len(d)==0:
            #print("STOP")
            flag = 0
            
            
        else:
            for link in d:
                domain = 'https://www.pages-annuaire.net'+ str(link.attrs['href'])
                data.append(domain)  
                print(domain)
            
            
        i = i+1
        #print(flag)
        #print(i)
        
    return data
    


# In[11]:


#Get all links categories for each ville
data = []
for link in links:
    data.append(get_urls_cat(link))


# In[50]:


#Extract all link domain for each ville and each secteur 
for i in range(len(data)):
    for secteur in data[i]:
        data_out = get_urls_domain(secteur)
        output = {
            'Ville' : secteur.split('/')[-1],
            'Secteur' : secteur.split('/')[-2],
            'Links' : data_out
        }
        output_data.append(output)


# In[54]:


with open("mydata.json", "w") as final:
    json.dump(output_data, final)


# In[96]:


df = pd.DataFrame(output_data)


# In[88]:


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
    


def pdp(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    t = soup.select('html body div.col-md-6 h1')
    title = t[0].text
    a = soup.select('html body div.col-md-6 h2')
    adresse = a[0].text
    b = soup.select('html body div.btn.text-uppercase.btn-numero')
    btn_data = b[0].attrs['data']
    num = get_num(btn_data)
    
    data = {
        'Title : ' : title,
        'Adresse : ': adresse,
        'Number : ': num
    }
    
    print(title + ' has been scraped')
    
    
    return title,adresse,num


# In[90]:


def main(output_data):
    Dump_data = []
    for i in range(len(output_data)):
        for link in output_data[i]['Links']:
            t,a,n = pdp(link)
            domain = {
                'Title':t,
                'Ville':output_data[i]['Ville'],
                'Secteur':output_data[i]['Secteur'],
                'Adresse':a,
                'Numero':n
            }
            Dump_data.append(domain)
    
    


# In[ ]:


with open("dump.json", "w") as Extract:
    json.dump(Dump_data, Extract)

