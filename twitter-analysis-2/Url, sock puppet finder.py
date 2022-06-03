
#%%

#

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

    lofl = []

    for f in range(len(i)):


        try:

            s = str((i[f]))
            s = re.sub(r"[^a-zA-Z/:.0-9]","",s)

            response = requests.get(s)

            url = response.url



            from urllib.parse import urlparse

            domain = urlparse(url).netloc
    
            d.append(domain)

            lofl.append(domain)    

            from urllib.request import urlopen
            from bs4 import BeautifulSoup


            soup = BeautifulSoup(urlopen(s))
 

            #print("Title of the website is : ")
            t.append(soup.title.get_text())    

        except:

            print('http error occured')
            #d.append('http error occured')
            #lofl.append('http error occured')  


        #d.append(lofl)
        #print(url)
# %%

print(d)


# %%

print(t)

 
domaindf = pd.DataFrame (d, columns = ['domain'])


# %%

domaincat = pd.Categorical(domaindf)



# %%
domaindf.value_counts().plot(kind='barh')


#%%

#import geopandas

#import geoplot





# %%

# import pygal
# from pygal_maps_world.maps import World


# worldmap_chart = World()


# worldmap_chart.title = 'Some countries'
# #%%
# worldmap_chart.add('F countries', ['fr', 'fi'])

# #%%
# worldmap_chart.render_to_file('chart.svg')


#%%

import pandas as pd
import tweepy
#User created date

#%%

creation_date = []

consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""
 
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

# auth = OAuthHandler(ckey, csecret)
# auth.set_access_token(atoken, asecret)
# api = API(auth)

print('Getting statistics for @user:')

for username in df['username']:

# Get information about the user
    data = api.get_user(screen_name=username)
    print(str(data.created_at))

    creation_date.append(str(data.created_at))


creation_date = pd.DataFrame(creation_date)


#%%

#convert into date format pd dataframe


creation_date.columns = ["Datetime"]


creation_date['Datetime'] = pd.to_datetime(creation_date['Datetime'])

#%%

import matplotlib.pyplot as plt

plt.subplot(2,3,1)
creation_date.hist(column='Datetime')
plt.title('Account creation date')












