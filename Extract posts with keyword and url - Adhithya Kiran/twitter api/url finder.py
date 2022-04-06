
#%%
from os import PRIO_USER
import string
from urllib import response
import pandas as pd
import re 
import requests

# %%


df = pd.read_csv('scraped_tweets.csv')
# %%

print(df.columns)


# %%

df['url'] = df['text'].str.extract('(....-..-..)', expand=True)

# %%




# %%

ulist = []

# %%

for i in df['text']:
    #print (i)

    #print(re.findall('http[a-zA-Z/:.0-9]+', i))

    ulist.append(re.findall('http[a-zA-Z/:.0-9]+', i))
# %%

print(ulist)


# %%
'''Adding the url list to the data frame '''

df['url'] = ulist

print(df)

# %%

df.columns
# %%
df['url']
# %%

'''finding and adding the real domain name to the df from shor url'''




# %%

d = []

t = []

#url = (df['url'][1])

for i in df['url']:

    for f in range(len(i)):


        try:

            s = str((i[f]))
            s = re.sub(r"[^a-zA-Z/:.0-9]","",s)

            response = requests.get(s)

            url = response.url



            from urllib.parse import urlparse

            domain = urlparse(url).netloc
    #print(domain)
            d.append(domain)    

            from urllib.request import urlopen
            from bs4 import BeautifulSoup


            soup = BeautifulSoup(urlopen(s))
 

    #print("Title of the website is : ")
            t.append(soup.title.get_text())    

        except:

            print('error occured')
    #print(url)
# %%

print(d)


# %%

print(t)

 



# %%





# %%






