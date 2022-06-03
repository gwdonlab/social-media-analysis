#######################################
## NetVision API for Reddit, Utility ##
#######################################

#Author: Andy Christian

#%%##########
## Imports ##
#############

import requests
import numpy as np
import pandas as pd
import datetime as dt
import re

#################################################
#<<<<<<<<<<<<<<<<< END SECTION >>>>>>>>>>>>>>>>>#

#%%############
## Functions ##
###############

def load_credentials(directory,credentials_file_name):
    """
    Read in credentials needed to access API from text file
    :param directory: the current working directory (should also be
     the location of the credentials text file)
    :credentials_file_name: name of the file
    :return: a dataframe holding the needed credentials
    """
    #Load credentials from text file
    try:
        credentials_df=pd.read_csv(f"{directory}\\{credentials_file_name}")
    except:
        print("Could not find file, please check for correct file name/working directory.")

    return credentials_df

#################################################

def connect_to_api(credentials_df):
    """
    Retrieves an authentication token needed for accessing API endpoints
    :param credentials_df: a dataframe holding the credentials necessary
     for obtaining the access token. This includes a Rediit Client ID,
     a Secret Token, and a Redditt username and password
    :return: a headers file containing the authentication token
    """
    #Assign credentials to variables
    try:
        #personal use script (client_id) -- the 'username' for the API
        CLIENT_ID=credentials_df.iloc[0,0]
        #secret (secret_key) -- the 'password' for the API
        SECRET_KEY=credentials_df.iloc[1,0]
        #Reddit username
        USERNAME=credentials_df.iloc[2,0]
        #Reddit password
        PASSWORD=credentials_df.iloc[3,0]
        #Url to obtain access_token for API
        TOKEN_URL='https://www.reddit.com/api/v1/access_token'
    except:
        print("Did not find the appropriate credentials. Please check your credentials file for proper length and format.")
    
    #Authenticate app
    try:
        auth=requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
    except:
        print('\nIssue with app authorization -- check personal use script (Client ID) and secret (Secret Key)\n')
    
    #Set request header info    
    headers = {'User-agent': 'investigateAPI'} 
    
    #Set user login info
    user_data={'grant_type':'password',
               'username':USERNAME,
               'password':PASSWORD}
        
    #3Obtain access_token
    try:
        request = requests.post(TOKEN_URL, auth=auth, data=user_data, headers=headers)
        TOKEN=request.json()['access_token']
        #add access token to headers parameter for later API calls
        headers={**headers, **{'Authorization':f'bearer {TOKEN}'}} #The **a, **b syntax merges all elements of 2 dictionaries
        print('\nAccess Token obtained\n')
    except:
        print('\nAn error occured gaining access token\nCheck login information\n')
        exit(-1)
    
    return headers

#################################################

def get_subreddits_json(params,headers):
    """
    Search Reddit for subreddits that match search criteria
    :param params: the parameters for the search (see /search reddit api)
    :return: a json file of the information returned from the call
    """
    try: 
        base_url=f'https://oauth.reddit.com/search'
        request=requests.get(base_url, params=params, headers=headers)
        if str(request)=="<Response [200]>":
            return request.json()
        else:
            print(f'\n{request}\nAn error occured connecting to API')
            print('If error was 504 timeout, try changing the limit\n\
paramter to 50 and below and bracket up from there.\n\
Otherwise, check arguments fed to function.')
            return None
    except:
        print('\nAn error occured connecting to API\n')
        return None
    
##################################################

def get_posts_by_sort_type_json(sr,sort_type,params,headers):
    """ 
    Find data on the posts of a given subreddit
    :param sr: subreddit to get the posts from
    :param search_type: Method to conduct sorting by (i.e top, new, etc. -- see /sort reddit api)
    :param params: additional parameters (see /sort reddit api)
    :return: a json file of the information returned from the call
    """
    try:
        base_url=f'https://oauth.reddit.com/r/{sr}/{sort_type}'
        request=requests.get(base_url, params=params, headers=headers)
        if str(request)=="<Response [200]>":
            return request.json()
        else:
            print(f'\n{request}\nAn error occured connecting to API')
            print('If error was 504 timeout, try changing the limit\n\
paramter to 50 and below and bracket up from there.\n\
Otherwise, check arguments fed to function.')
            return None
    except:
        print('\nAn error occured connecting to API\n')
        return None

##################################################

def get_posts_by_topic_json(sr,params,headers):
    """ 
    Find data on the posts of a given subreddit
    :param sr: subreddit to get the posts from
    :param params: additional parameters for search (see /search reddit api)
    :return: a json file of the information returned from the call
    """
    try:
        base_url=f'https://oauth.reddit.com/r/{sr}/search'
        request=requests.get(base_url, params=params, headers=headers)
        if str(request)=="<Response [200]>":
            return request.json()
        else:
            print(f'\n{request}\nAn error occured connecting to API')
            print('If error was 504 timeout, try changing the limit\n\
paramter to 50 and below and bracket up from there.\n\
Otherwise, check arguments fed to function.')
            return None
    except:
        print('\nAn error occured connecting to API\n')
        return None

##################################################

def get_xpost_data_json(sr,article,params,headers):
    """
    Find data on the duplicates (crossposts) of a given post_id 
    :param sr: subreddit to find the original post in
    :param article: the id of the post (without the t3_)
    :param params: additional parameters (see /duplicates reddit api)
    :return: a json file of the information returned from the call
    """
    try: 
        base_url=f'https://oauth.reddit.com/r/{sr}/duplicates/{article}'
        request=requests.get(base_url, params=params, headers=headers)
        #print(request) #for testing
        if str(request)=="<Response [200]>":
            #print("request is good")
            return request.json()
        else:
            print(f'\n{request}\nAn error occured connecting to API')
            print('If error was 504 timeout, try changing the limit\n\
paramter to 50 and below and bracket up from there.\n\
Otherwise, check arguments fed to function.')
            return None
    except:
        print('\nAn error occured connecting to API\n')
        return None

##################################################

def extract_sr_data(req):
    """
    Extract data for subreddits matching a search criteria
    :param req: the json file holding the objects/data on the subreddits
    :return a dataframe of the desired subreddit details
    """
    myDict = {}
    try:
        for i, sub in enumerate(req['data']['children']):
            date=dt.datetime.fromtimestamp(sub['data']['created_utc'])
            #date=f'{date.month}/{date.day}/{date.year}'
            myDict[i+1] = {'subreddit':sub['data']['display_name'],
                        'subreddit_id':sub['data']['name'],
                        'type':sub['data']['subreddit_type'],
                        'url':sub['data']['url'],
                        'title':sub['data']['title'],
                        'description':sub['data']['description'],
                        #'creation_date':sub['data']['created_utc'],
                        'creation_date':date,
                        'subscribers':sub['data']['subscribers'],
                        'submit_text':sub['data']['submit_text']
                        }
        df = pd.DataFrame.from_dict(myDict, orient='index')
        return df
    except:
        print("Did not returned expected json file, check paramters")
        exit(-1)
        #return None

##################################################

def extract_posts_data(req):
    """
    Extract post data after searching a subreddit for posts matching a given search method
    :param req: the json file holding the objects/data on the posts
    :return: a dataframe of the desired post information
    """
    myDict = {}
    try:
        for i, post in enumerate(req['data']['children']):
            try:
                author_id=post['data']['author_fullname']
                author_username=post['data']['author']
                date=dt.datetime.fromtimestamp(post['data']['created_utc'])
                #myDict[i+1] = {'author':post['data']['author_fullname']}
            except:
                author_id='No author_id'
                author_username='No author username'
                continue
                #myDict[i+1] = {'author':'No Author Name'}
            myDict[i+1] = {'author_username':author_username,
                        'author_id':author_id,
                        'post_id':post['data']['id'],
                        'title':post['data']['title'],
                        'text':post['data']['selftext'],
                        'flair':post['data']['link_flair_text'],
                        'url':post['data']['url'],
                        'permalink':post['data']['permalink'],
                        'subreddit':post['data']['subreddit'],
                        'subreddit_id':post['data']['subreddit_id'],
                        'post_creation':date,
                        'original':post['data']['is_original_content'],
                        'domain':post['data']['domain'],
                        'score':post['data']['score'],
                        'upvote_ratio':post['data']['upvote_ratio'],
                        'comments':post['data']['num_comments'],
                        'crosspostable':post['data']['is_crosspostable'],
                        'crossposts':post['data']['num_crossposts']}
        df = pd.DataFrame.from_dict(myDict, orient='index')
        return df
    except:
        print("Did not returned expected json file, check paramters")
        exit(-1)
        #return None

##################################################

def extract_xposts_data(req):
    """
    Extract crosspost data of a given post
    :param req: the json file holding the objects/data on the crossposts of the given post
    :return: a dataframe of the desired post information
    """
    myDict = {}
    try:
        for i, xpost in enumerate(req[1]['data']['children']):
            try:
                xposter_id=xpost['data']['author_fullname']
                xposter_username=xpost['data']['author']
                org_created=xpost['data']['crosspost_parent_list'][0]['created_utc']
                xpost_created=xpost['data']['created_utc']
                elapsed_time=time_convert(xpost_created-org_created)
            except:
                xposter_id='No author_id'
                xposter_username='No author username'
                continue
            myDict[i+1] = {'parent_post_id':xpost['data']['crosspost_parent'],
                        'parent_subreddit':xpost['data']['crosspost_parent_list'][0]['subreddit'],
                        'parent_subreddit_id':xpost['data']['crosspost_parent_list'][0]['subreddit_id'],
                        'xposter_username':xposter_username,
                        'xposter_id':xposter_id,
                        'xpost_id':xpost['data']['id'],
                        'title':xpost['data']['title'],
                        'text':xpost['data']['selftext'],
                        'flair':xpost['data']['link_flair_text'],
                        'url':xpost['data']['url'],
                        'permalink':xpost['data']['permalink'],
                        'subreddit':xpost['data']['subreddit'],
                        'subreddit_id':xpost['data']['subreddit_id'],
                        'subreddit_type':xpost['data']['subreddit_type'],
                        'subreddit_subs':xpost['data']['subreddit_subscribers'],
                        'xpost_creation':dt.datetime.fromtimestamp(xpost_created),
                        'original_creation':dt.datetime.fromtimestamp(org_created),
                        'elapsed_time_days':elapsed_time,
                        'edited':xpost['data']['edited'],
                        'domain':xpost['data']['domain'],
                        'ups':xpost['data']['ups'],
                        'downs':xpost['data']['downs'],
                        'score':xpost['data']['score'],
                        'upvote_ratio':xpost['data']['upvote_ratio'],
                        'comments':xpost['data']['num_comments'],
                        'crosspostable':xpost['data']['is_crosspostable'],
                        'crossposts':xpost['data']['num_crossposts']}
        df = pd.DataFrame.from_dict(myDict, orient='index')
        return df
    except:
        print("Did not returned expected json file, check paramters")
        exit(-1)
        #return None
    
#################################################

def create_subredditsDF(params,headers):
    """
    Create dataframe of subreddits that match search criteria
    :param params: the parameters for the search (see /search reddit api)
    :return: a dataframe of the information returned from the api call
    """
    #Get json file from api to extract data into DF
    try:
        req=get_subreddits_json(params,headers)
    except:
        exit(-1)
    #Get dataframe from response
    try:
        new_df=extract_sr_data(req)
        return(new_df)
    except:
        empty=pd.DataFrame()
        return empty

##################################################

def create_postsDF_by_topic(sr,params,n,headers):
    """ 
    Create dataframe of posts in the given subreddit on the given topic
    :param sr: subreddit to get the posts from
    :param params: additional parameters for search (see /search reddit api)
    :param n: number of queries to conduct (total observations returned = n*limit)
    :return: a dataframe of the information returned from the api call(s)
    """
    #Create dummy df and final post
    final_df=pd.DataFrame()
    final_post_id=None
    
    #Build full DF through n multiple calls to API (returns n*limit results)
    for n in range(n):
        #Get json file from api to extract data into DF
        try:
            req=get_posts_by_topic_json(sr,params,headers)
            #If unexpected behavior, return empty dataframe and stop function
            if req==None:
                return final_df
        #If unexpected behavior, return empty dataframe and stop function
        except:
            return final_df
        try:
            #Get dataframe from response
            new_df=extract_posts_data(req)
            #Concat new_df to data
            final_df=pd.concat([final_df, new_df]).reset_index(drop=True)
            #Get id of the final row (oldest entry)
            final_post_id=f"t3_{new_df.iloc[len(new_df)-1, 2]}"
            #Add/update last post as starting point for next query in params
            params['after']=final_post_id
        except:
            #To avoid errors if no more posts to grab
            pass
    
    return(final_df)

##################################################

def create_postsDF_by_sort_type(sr,sort_type,params,n,headers):
    """ 
    Create dataframe of posts in the given subreddit sorted by provided method
    :param sr: subreddit to get the posts from
    :param sort_type: Method to conduct sorting by (i.e top, new, etc. -- see /sort reddit api)
    :param params: additional parameters (see /sort reddit api)
    :param n: number of queries to conduct (total observations returned = n*limit)
    :return: a dataframe of the information returned from the api call(s)
    """
    #Create dummy df and final post
    final_df=pd.DataFrame()
    final_post_id=None
    
    #Build full DF through n multiple calls to API (returns n*limit results)
    for n in range(n):
        #Get json file from api to extract data into DF
        try:
            req=get_posts_by_sort_type_json(sr,sort_type,params,headers)
            #If unexpected behavior, return empty dataframe and stop function
            if req==None:
                return final_df
        #If unexpected behavior, return empty dataframe and stop function
        except:
            return final_df
        try:
            #Get dataframe from response
            new_df=extract_posts_data(req)
            #Concat new_df to data
            final_df=pd.concat([final_df, new_df]).reset_index(drop=True)
            #Get id of the final row (oldest entry)
            final_post_id=f"t3_{new_df.iloc[len(new_df)-1, 2]}"
            #Add/update last post as starting point for next query in params
            params['after'] = final_post_id
        except:
            #To avoid errors if no more posts to grab
            pass
    
    return(final_df)

##################################################

def create_xpostsDF(sr,article,params,headers):
    """ 
    Create dataframe of crossposts of given post
    :param sr: subreddit to find the original post in
    :param article: the id of the post (without the t3_)
    :param params: additional parameters (see /duplicates reddit api)
    :return: a dataframe of the information returned from the api call(s)
    """ 
    #Get json file from api to extract data into DF
    try:
        req=get_xpost_data_json(sr,article,params,headers)
    except:
        exit(-1)
    #Get dataframe from response
    try:
        new_df=extract_xposts_data(req)
        return(new_df)
    except:
        empty=pd.DataFrame()
        return empty
##################################################

def time_convert(time):
    """ 
    Convert seconds to days, hours, minutes, seconds in text form
    Used to display the 'lifetime' of a post/xpost
    :param time: time in seconds
    :return: a string of the time converted to days, hours, minutes, and seconds
    """
    #Could update to include years...
    
    sec=time%60
    time//=60
    
    min=time%60
    time//=60
    
    hours=time%24
    time//=24
  
    days=time
    #hours=time
 
    #return(days)
    #return(f'Hours: {hours} --- Min: {min} --- Sec: {sec}')
    return(f'{int(days)} days, {int(hours)} hours, {int(min)} minutes, and {int(sec)} seconds.')

##################################################

def create_external_domainsDF(df):
    """
    Create a dataframe of only those posts which explicitly come from an external domain
    :param df: the original df from which to pull those externally sourced posts
    :return: a dataframe of only posts with a non-Reddit source
    """
    #Setup conditions for finding external links
    #Get name of subreddit
    df.name=df.iloc[0,8]
    #Condition list include all reddit self-reference, and the subreddit self-reference
    cond_list=['v.redd.it', 'i.redd.it', 'reddit.com', f'self.{df.name}']
    #Check for any values in domain that are not referencing the Reddit or the subreddit
    cond=df['domain'].isin(cond_list)
    #Filter for condition and display DF of only external links
    ext_links_df=df[~cond].reset_index(drop=True)
    
    return ext_links_df

##################################################

def aggregate_num_external_domains_to_df(sr_df, df):
    """
    Determines the number of externally sourced posts in a given subreddit,
    then updates that subreddit's row in the subreddit dataframe with the
    number of such links that it has.
    :param sr_df: the dataframe to add the total links to (should be subreddits DF)
    :param df: the dataframe of a subreddit's posts, which will be mined for links 
    :return: None (actions to subreddit's DF done in function)
    """
    #Setup conditions for finding external links
    #Check if subreddit df has column for external links, otherwise setup
    if 'external_domain_links' not in sr_df.columns:
        sr_df['external_domain_links']=np.nan
    #Get name of subreddit
    df.name=df.iloc[0,8]
    #Condition list include all reddit self-reference, and the subreddit self-reference
    cond_list=['v.redd.it', 'i.redd.it', 'reddit.com', f'self.{df.name}']
    #Check for any values in domain that are not referencing the Reddit or the subreddit
    cond=df['domain'].isin(cond_list)
    #Find number of external links
    total_ext_links=df[~cond].count()[0]
    #update the the row for this subreddit in the subreddit df with its number of external links
    cond=sr_df['subreddit']==df.name
    #Check if given subreddit already has value in column
    if sr_df.loc[cond, 'external_domain_links'].isna().all():
        sr_df.loc[cond, 'external_domain_links']=total_ext_links
    else:
        sr_df.loc[cond, 'external_domain_links']+=total_ext_links
    
    return None

##################################################

def aggregate_num_internal_links_to_df(sr_df, df):
    """
    Determines the number of links a subreddit has with other subreddits,
    that is to say, the total crossposts in other subreddit's that the posts
    in the given subreddit have. Then the given subreddit's row in the subreddit
    dataframe is updated with the number of such links that it has.
    :param sr_df: the dataframe to add the total links to (should be subreddits DF)
    :param df: the dataframe of a subreddit's posts, which will be mined for links 
    :return: None (actions to subreddit's DF done in function)
    """
    #Setup conditions for finding external links
    #Check if subreddit df has column for external links, otherwise setup
    if 'internal_links' not in sr_df.columns:
        sr_df['internal_links']=np.nan
    #Get name of subreddit
    df.name=df.iloc[0,8]
    #Find total crossposts in the newest posts of the subreddit
    total_int_links=sum(df['crossposts'])
    #update the the row for this subreddit in the subreddit df with its number of external links
    cond=sr_df['subreddit']==df.name
    sr_df.loc[cond, 'internal_links']=total_int_links
    
    return None

##################################################

def create_ext_link_df(df):
    """
    For those posts externally sourced in a subreddit, determines where they are
    sourced from, then tallies up the number of links for each source domain and
    displays the results in a dataframe.
    :param df: the dataframe of a subreddit's posts, which will be mined for links 
    :return: a dataframe of all external link domains and their number of links
    """
    #Aggregate number of incoming links from external sources (i.e. which smp are people using to post content in the sr)
    #Get a df of just the externally sourced posts
    df=create_external_domainsDF(df)
    #Count total links and drop all but 1 columns of results
    link_df=df.groupby('domain').count().iloc[:,0:1]
    #Get the name of the kept column and rename it
    col_name=link_df.columns[0]
    link_df=link_df.rename(columns={col_name:'total_links'})
    #If youtube is a link, consolidate into one type (they go to the same website)
    #Multiple situation of this, so ignoring for now...
    #try:
    #    link_df.loc['youtube.com', 'total_links']+=link_df.loc['youtu.be', 'total_links']
    #    link_df.drop(labels='youtu.be', axis=0, inplace=True)
    #except:
    #    pass
    #Sort by most common link
    link_df=link_df.sort_values(by=['total_links'], ascending=False).iloc[:,0:1]
    #Include columns indicating the subreddit the links came from
    link_df['parent_sr']=df['subreddit'][0]
    link_df['parent_sr_id']=df['subreddit_id'][0]
    
    return link_df

#################################################

def mine_text_links(df):
    """
    Takes the posts from a given subreddit and mines those posts for any
    links in the text of the post. Then, determines the source of those links,
    tallies them up and creates a dataframe of the sources and their number of links.
    :param df: the dataframe of a subreddit's posts, which will be mined for links 
    :return: a dataframe of all the links found in the text of the posts
    """
    #Get list of posts that appear to have links in their text
    cond=df[['text']].apply(lambda x: x.str.contains('https')).any(axis=1)
    link_list=df.loc[cond, 'text'].values

    #Will hold final set of links
    final_link_list=[]
    #Extract all links from list of post texts
    for i,link in enumerate(link_list):
        #Check for duplicate links
        regex1=r"https://[a-zA-z0-9'-.]*[.com|.pl|.gov|.edu|.net|.org][^()\s\][]*"
        smp=re.findall(regex1, link)
        smp=list(set(smp))
        #Extract simple links
        link_list=[]
        for link in smp:
            regex2=r"https://[a-zA-z0-9'-.]*[.com|.pl|.gov|.edu|.net|.org][a-zA-z0-9'-.]*[^/]"
            smp2=re.findall(regex2, link)
            link_list.append(str(smp2[0]))
        #Add each unique link from each post to the final link list
        for link in link_list:
            final_link_list.append(link)

    #Aggregate each link type into a dictinoary counting how many of each type
    link_dict={}
    for link in final_link_list:
        if link in link_dict:
            link_dict[link]+=1
        else:
            link_dict[link]=1
    
    text_link_df=pd.DataFrame(list(link_dict.items()))
    text_link_df=text_link_df.rename(columns={0:"domain", 1:"total_links"}).set_index('domain').sort_values(by='total_links', ascending=False)
    text_link_df['parent_sr']=df['subreddit'][0]
    text_link_df['parent_sr_id']=df['subreddit_id'][0]

    return text_link_df

#################################################

def aggregate_text_links_to_df(sr_df, link_df):
    """
    Takes a list of links (mined from text of posts), determines whether they
    are external links or internal links, sums up the total of both types
    and then updates the given subreddit's external and internal link totals
    in the subreddit DF.
    :param sr_df: the dataframe to add the total links to (should be subreddits DF) 
    :param df: the dataframe of a subreddit's posts, which will be mined for links 
    :return: None (actions to subreddit's DF done in function)
    """
    #Setup conditions for finding external links
    #Check if subreddit df has column for external links, otherwise setup
    if 'external_domain_links' not in sr_df.columns:
        sr_df['external_domain_links']=np.nan
    #Get name of subreddit
    link_df.name=link_df.iloc[0,1]
    #Condition list include all reddit self-reference, and the subreddit self-reference
    cond_list=['https://preview.redd.it',
               'https://www.reddit.com',
               'https://reddit.com',
               'https://i.redd.it',
               'https://v.redd.it',
               f'https://.self.{link_df.name}']
    #Check for any values in domain that are not referencing the Reddit or the subreddit
    cond=link_df.index.isin(cond_list)
    #Find number of external links
    total_ext_links=link_df.loc[~cond, 'total_links'].sum()
    #Find number of internal links
    total_int_links=link_df.loc[cond, 'total_links'].sum()
    #Check if given subreddit already has value in column, then add/update
    cond=sr_df['subreddit']==link_df.name
    if sr_df.loc[cond, 'external_domain_links'].isna().all():
        sr_df.loc[cond, 'external_domain_links']=total_ext_links
    else:
        sr_df.loc[cond, 'external_domain_links']+=total_ext_links
    if sr_df.loc[cond, 'internal_links'].isna().all():
        sr_df.loc[cond, 'internal_links']=total_int_links
    else:
        sr_df.loc[cond, 'internal_links']+=total_int_links

    return None

#################################################
#<<<<<<<<<<<<<<<<< END SECTION >>>>>>>>>>>>>>>>>#

# %%
