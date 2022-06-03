###########################################
## NetVision API for Reddit, Example Use ##
###########################################

#Author: Andy Christian

#%%##########
## Imports ##
#############

import os
import pandas as pd
from IPython.display import display
import re

#NetVision API Utility File
import NetVisionUtility as nv

#################################################
#<<<<<<<<<<<<<<<<< END SECTION >>>>>>>>>>>>>>>>>#

#%%###########
## Settings ##
##############

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 3)

#################################################
#<<<<<<<<<<<<<<<<< END SECTION >>>>>>>>>>>>>>>>>#

#%%############
## API SETUP ##
###############

#Resources I used
#https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c
#https://medium.com/geekculture/utilizing-reddits-api-8d9f6933e192

#Step 1: Load credentials from file on computer

#1.A -- get current directory in use. Make sure your credentials file is located there
directory=os.getcwd()
#1.B -- Change this variable to match what you have named your credentials file
credentials_file_name='credentials.txt'
#1.C -- Read contents of credentials file into a pd dataframe for future use
credentials_df=nv.load_credentials(directory, credentials_file_name)

#Step 2: Connect to Reddit API

    #Connceting to the Reddit API requires a few things
    # A. Must authenticate API app
    #   -Use HTTPBasicAUth to pass app's id (personal use script) and password (secret)
    # B. Must login with reddit profile
    # C. Must use the info from steps 1 to obtain an authentication token, used for future API calls
    #   -The info from steps 2.A & 2.B get passed as parameters in a request call in step 2.C
    #   -Note that the .post call is used for this step, not the .get call
headers=nv.connect_to_api(credentials_df)

#################################################
#<<<<<<<<<<<<<<<<< END SECTION >>>>>>>>>>>>>>>>>#

#%%###########################
## Basic Functions Examples ##
##############################

#%%

#1. Get info on subreddits related to topic

#Set the parameters for the subreddit search
#Note that the type is designated sr for subreddits
params={'q':'ukraine', 'limit':100, 'type':'sr', 'sort':'relevance', 't':'all'}
#Run function and display results
subreddits_df=nv.create_subredditsDF(params,headers)
print(f"\nNumber of Subreddits Returned: {len(subreddits_df)}\n\nDF Head")
display(subreddits_df.head())

#################################################
#%%

#2. Check a specific subreddit returned in the previous querry for posts on a specific topic

#Set the subreddit to look in as the top returned in the subreddit search
sr=subreddits_df.iloc[0,0]
#Set the topic to look for posts about 
q="counterattack"
#parameters specific to searching a subreddit about a given topic
#Note that the restrict_sr parameter is set to True
#If set to false, all subreddits will be searched for the topic
#Note that the type of object being searched for is link, which is a post
params={'limit':100, 'type':'link', 'q':q, 'restrict_sr':True}
#Set the number of queries to conduct (results returned will be n*limit)
n=10
#Run function and display results
topic_df=nv.create_postsDF_by_topic(sr,params,n,headers)
print(f"\nNumber of Posts Returned: {len(topic_df)}\n\nDF Head")
display(topic_df.head())

#################################################

#%%

#3. Look at the posts of a subreddit based on a sort method (irrespective of topic)

#Set the subreddit to look in as the top returned in the subreddit search
sr=subreddits_df.iloc[0,0]
#Set the type of sort method to be used, in this case the most popular posts
sort_type='top'
#parameters specific to sorting posts as opposed to searching them
#Note that for a top search, the t parameter is needed, which indicates the timeframe to search in
#Other sorts, like new, do not need a time parameter
params={'limit':100, 't':'all'}
#Set the number of queries to conduct (results returned will be n*limit)
n=10
#Run function and display results
sort_df=nv.create_postsDF_by_sort_type(sr,sort_type,params,n,headers)
print(f"\nNumber of Posts Returned: {len(sort_df)}\n\nDF Head")
display(sort_df.head())

#################################################

#%%

#4. Look at the crossposts of one of the posts returned in the previous query

#Extract the post id of the post for which crossposts will be looked at
article=f"{sort_df.iloc[1,2]}"
#Extract the subbreddit name of the post for which crossposts will be looked at
sr=sort_df.iloc[1,8]
#parameters specific to searching for crossposts
params={"limit":100}
#Run function and display results
xpost_df=nv.create_xpostsDF(sr,article,params,headers)
print(f"\nNumber of Posts Returned: {len(xpost_df)}\n\nDF Head")
display(xpost_df.head())

#################################################

#%%#############################################
## Functions that Manipulate Returned Results ##
################################################

#Some terms used:
# smp:
#      -Social media platform
# explicit external links:
#     -These are media uploaded from other smp when the post was created, stored in the "domain" field
#     -If someone downloaded a video, say from TikTok, then uploaded it from their own computer,
#      it would show up as coming from Reddit, not TikTok in the "domain" field.
# other external links:
#     -These are media from other sources, but not uploaded directly from those sources when the post
#      was made, i.e. the TikTok video example above
#     -Currently, only links found in the text of a post are able to be identified. Links, such as the
#      TikTok video example, are not able to be identified at this time.
#
# internal links:
#      -These are crossposts connecting one subreddit to another
#      

#################################################

#%%

#Grab the 1000 newest posts in the ukraine subreddit for use in examples
sr=subreddits_df.iloc[0,0]
sort_type='new'
params={'limit':100, 't':'all'}
n=10
ukr_recent_df=nv.create_postsDF_by_sort_type(sr,sort_type,params,n,headers)
print(f"\nNumber of Posts Returned: {len(ukr_recent_df)}\n\nDF Head")
display(ukr_recent_df.head())

#################################################

#%%

#5. Find explicit external links
    
#Show a DF of just the posts in the subreddit with an external domain
# that is, those posts display information explicitly linked from an outside platform
ukr_recent_ext_links_df=nv.create_external_domainsDF(ukr_recent_df.copy(deep=True))
print(f"\nNumber of Externally Linked Posts: {len(ukr_recent_ext_links_df)}\n\nDF Head")
display(ukr_recent_ext_links_df.head())

#################################################

#%%

#6. Aggregate explicit external links

#Use the external aggregate function to add the number of external links
# for a given subreddit back to that subreddit's row in the subreddit DF
nv.aggregate_num_external_domains_to_df(subreddits_df,ukr_recent_df.copy(deep=True))
display(subreddits_df.head())

#################################################

#%%

#7. Create DF of the explicit external link values

#Create and display a dataframe showing the type and number of
# explicit external links found in a given subreddit
#link_df=nv.create_ext_link_df(ukr_recent_ext_links_df.copy(deep=True))
link_df=nv.create_ext_link_df(ukr_recent_df.copy(deep=True))    
display(link_df)

#################################################

#%%

#8. Aggregate internal links (i.e. crossposts)

#Use the internal aggregate function to add the number of external links
# for a given subreddit back to that subreddit's row in the subreddit DF
nv.aggregate_num_internal_links_to_df(subreddits_df, ukr_recent_df.copy(deep=True))
display(subreddits_df.head())

#################################################

#%%

#9. Mine links in the text of the most recent posts in a subreddit

#First lets just see how many potential links are observed
cond=ukr_recent_df[['text']].apply(lambda x: x.str.contains('https')).any(axis=1)
print(f"Number of posts in this DF potentially containing links in their text: {len(ukr_recent_df[cond])}")

#################################################

#%%

#Now, let's take just the first 5 posts and look at the content
link_list=ukr_recent_df.loc[cond, 'text'].values
link_list_test=link_list[0:5]
print("\nCOMMENT\n\
As can be seen, this is super messy. Luckily, the text mining function\n \
will take care of all of this. It grabs all links in a given post\n \
and also checks for duplicates. Then it tallies up the total for each\n \
link type into a dictionary. Finally, it produces a DF of the links.\n\
----------------------------------------------------------------------\n")
print(link_list_test)

#################################################

#%%

#Use text mining function on first 5 posts with links in text
# A modified version of the function is used here to display
# intermediate steps

print('\nExample of mining unqiue links from text of posts.\n\
Short links retrieved after discarding duplicates.\n')

def mine_text_links_example(df):
    """
    Info here
    """
    #Get list of posts that appear to have links in their text
    cond=df[['text']].apply(lambda x: x.str.contains('https')).any(axis=1)
    link_list=df.loc[cond, 'text'].values
    #FOR EXAMPLE ONLY -- get first 5 posts
    link_list_test=link_list[0:5]

    #Will hold final set of links
    final_link_list=[]
    #Extract all links from list of post texts
    for i,link in enumerate(link_list_test):
        #Check for duplicate links
        regex1=r"https://[a-zA-z0-9'-.]*[.com|.pl|.gov|.edu|.net|.org][^()\s\][]*"
        #regex1=r"https://.*[.com|.pl|.gov|.edu|.net|.org][^()\s\][]*"
        smp=re.findall(regex1, link)
        smp=list(set(smp))
        #Extract simple links
        link_list=[]
        #Indicate which post is being mined
        print(f"post {i}\nfull links: {len(smp)}\n{smp}")
        for link in smp:
            regex2=r"https://[a-zA-z0-9'-.]*[.com|.pl|.gov|.edu|.net|.org][a-zA-z0-9'-.]*[^/]" #[^()\s\][]*[^.]"
            smp2=re.findall(regex2, link)
            link_list.append(str(smp2[0]))
        #Show the short verison of all the unique links 
        print(f"short links (no duplicates): {len(link_list)}\n{link_list}\n")
        #Add each unique link from each post to the final link list
        for link in link_list:
            final_link_list.append(link)

    #Display the short version of all the links that were for unique media
    print(f"All Links:\n{final_link_list}\n")

    #Aggregate each link type into a dictinoary counting how many of each type
    link_dict={}
    for link in final_link_list:
        if link in link_dict:
            link_dict[link]+=1
        else:
            link_dict[link]=1
    print(f"Final Link Dictionary:\n{link_dict}")

mine_text_links_example(ukr_recent_df)

#################################################

#%%

#Now the results of using the regular function on the full dataframe
text_link_df=nv.mine_text_links(ukr_recent_df)
print("Text Link Dataframe:")
display(text_link_df)

#################################################

#%%

#10. Aggregating text links back to subreddit DF by type

#We can now determine whether these are internal or external links,
# and then aggregate those number back to the given subreddit in
# the subreddits DF
print("\nSubreddit DF before adding links from posts' text")
display(subreddits_df.head())
nv.aggregate_text_links_to_df(subreddits_df, text_link_df)
print("\nSubreddit DF after adding links from posts' text")
display(subreddits_df.head())

#################################################
#<<<<<<<<<<<<<<<<< END SECTION >>>>>>>>>>>>>>>>>#

#%%