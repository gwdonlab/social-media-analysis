# %%
# Requirements:
# Python 2.7 or Python 3.5+
# The pip package management tool
# The Google APIs Client Library for Python
# pip install --upgrade google-api-python-client
# The google-auth-oauthlib and google-auth-httplib2 libraries for user authorization
# pip install --upgrade google-auth-oauthlib google-auth-httplib2

from googleapiclient.discovery import build

api_key = ""

# creating youtube resource object
youtube = build('youtube', 'v3',
                developerKey=api_key)


request = youtube.videos().list(
    part="snippet,contentDetails,statistics",
    id='GTr28z9tp7s'
)
response = request.execute()

# %%
# Takes in a simple query and number of results the user is looking for.
# setting a global variable
vid_id = []

def video_identification(q, maxResults):
    # # Your request can also use the Boolean NOT (-) and OR (|) operators to exclude videos or to find videos that are associated with one of several search terms. For example, to search for videos matching either "boating" or "sailing", set the q parameter value to boating|sailing. Similarly, to search for videos matching either "boating" or "sailing" but not "fishing", set the q parameter value to boating|sailing -fishing.

    # Uses the search function to fetch VideoId's - present in snippet.
    # We can add location/Location Radius/Region Code here!
    # Video duration: any/long/medium/short

    # to store video id's. Using global variable to allow changes. 
    global vid_id

    response = youtube.search().list(
        part="snippet",
        type='video',
        q=q,
        order='date',
        videoDuration='medium',
        maxResults=maxResults  # 0 to 50 inclusive
    ).execute()

    for item in response['items']:
        videoid = item['id']['videoId']
        vid_id.append(videoid)

    return vid_id  # returns list of video id's

# %%
# fetches video statistics like views since the release, likes,  dislikes and comments.
# Also provides content details like dimension, definition, caption(T/F) and whether content is licensed or not. 
# Pass in videoId and get results:

# In an ideal scenarion, below function should be executed first to gather preliminary information about the video. And then comments and replies should be fetched. 

def get_vid_stats(videoId):
    # This function needs a request call
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=videoId
    )

    response = request.execute()
    for item in response['items']:
        title = item['snippet']['title']
        description = item['snippet']['description']
        statistics = item['statistics']
        contentDetails = item['contentDetails']
        # Thumbnails? do we need them?

        return {
            'Video Title': title,
            'Video Description': description,
            'Video Statistics': statistics,
            'More Content Details': contentDetails
        }
        
# Below function is just for fetching the description section of one video and putting it in a txt file and displaying it as output. - To snatch links.         
def get_vid_description(videoId):
    # This function needs a request call      
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=videoId
    )
        response = request.execute()
        for item in response['items']:
            description = item['snippet']['description']
        
        # Creates a new file: description_file here  
        with open('description_file', 'a', encoding='utf-8') as f:
            f.write(description)
        
        return {
        'Video Description': description
        }
            
#%%
# creating a loop that will pass all the videoIds into the get_vid_description method and will copy the info in a file. 

# The method takes in vid_id as the input. vid_id contains all the videoId's and is also a global parameter. 
# If nothing is given in as input, it will use the global parameter vid_id as input. 

def get_vid_description_all(vid_id):
    for i in vid_id:
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=i
    )
        response = request.execute()
        for item in response['items']:
            description = item['snippet']['description']
        
        # Creates a new file: description_file here  
        with open('description_file', 'a', encoding="utf-8") as f:
            f.write(description)
            f.write('\n-----\n-----\n----->>\n')
            f.close()
            
    return print(f'Added {len(vid_id)} descriptions in the file.')


# %%
# Use regex to fetch links from the file
import os
import re
def get_desc_links(filename):
# Load the file:
    with open(filename, encoding='utf-8') as f:
        contents = f.read()

    urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', contents)
    return urls
#%%
# Below requires the Spacy package to be installed.
# Spacy is a nlp package which can help in fetching links from a file. 
# pip install spacy 

# regex function is still there but adding this functionality to get links and urls of all kinds. 

# Feel Spacy can do a better job at grabbing links of different kinds. 

import spacy
nlp = spacy.load('en_core_web_sm')
f = open('description_file', 'r', encoding = 'utf-8' )

doc = nlp(f.read())
links = []
for token in doc:
    if token.like_email or token.like_url:
        links.append(token)
print(f'There are {len(links)} description links.\n{links}') 
#------------------------------------------------------------------

# %%
# For a single videoId: 

# stores comment and reply information from a video. VideoID and MaxResults are required parameters. Rest are optional, set already.


def fetch_comments(videoId, maxResults, part='id, replies, snippet',  textFormat='plainText', order='time'):
    # Generate response.
    response = youtube.commentThreads().list(
        part=part,
        maxResults=maxResults,
        textFormat=textFormat,
        order=order,
        videoId=videoId
    ).execute()

# create empty list to store info.
    comments = []
    comment_ids = []
    replies = []
    likes = []
    published_dates = []
    reply_comment = []
    reply_posted = []
    reply_likes = []
# Will continue until API Quota is maxed out or Comments run out. 10,000 units for a day. Each commentThread call is 1 unit.
    while response:

       # Will only get the comments.
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
            comment_id = item['snippet']['topLevelComment']['id']
            comment_ids.append(comment_id)
            reply_count = item['snippet']['totalReplyCount']
            replies.append(reply_count)
            like_count = item['snippet']['topLevelComment']['snippet']['likeCount']
            likes.append(like_count)
            comment_published = item['snippet']['topLevelComment']['snippet']['publishedAt']
            published_dates.append(comment_published)

 # Will get the replies (fetches the reply information from a comment video)
        for item in response['items']:
            if item['snippet']['totalReplyCount'] >= 1:
                for i in range(len(item['replies']['comments'])):
                    comment = item['replies']['comments'][i]['snippet']['textOriginal']
                    reply_comment.append(comment)
                    publish_date = item['replies']['comments'][i]['snippet']['publishedAt']
                    reply_posted.append(publish_date)
                    like_count = item['replies']['comments'][i]['snippet']['likeCount']
                    reply_likes.append(like_count)
            else:
                pass

    # Check if the video comment section has a next page... if it does generate a new response with 'pageToken' value.
        if 'nextPageToken' in response:
            # Regenrate response for the new vid:
            response = youtube.commentThreads().list(
                part=part,
                maxResults=maxResults,
                textFormat=textFormat,
                order=order,
                videoId=videoId,
                pageToken=response['nextPageToken']
            ).execute()
        else:
            break

# Finally, return the data back
    return {
        'Comments': comments,
        'Comment Id': comment_ids,
        'Reply Count': replies,
        'Likes Count': likes,
        'Published Date of Comment': published_dates,
        'Replies': reply_comment,
        'Published Date of Reply': reply_posted,
        'Likes on Reply': reply_likes,
        # below includes comments + replies.
        'Number of Total Comments': len(comment_ids)+len(reply_comment)
    }


# %%
# 
# To run through a list of VideoId's:

def fetch_comments_all(vid_id, maxResults):
    # Generate response.
    part='id, replies, snippet'
    textFormat='plainText'
    order='time'
    # create empty list to store info.
    comments = []
    comment_ids = []
    replies = []
    likes = []
    published_dates = []
    reply_comment = []
    reply_posted = []
    reply_likes = []
    for i in vid_id:
        response = youtube.commentThreads().list(
            part=part,
            maxResults=maxResults,
            textFormat=textFormat,
            order=order,
            videoId=i
        ).execute()
# Will continue until API Quota is maxed out or Comments run out. 10,000 units for a day. Each commentThread call is 1 unit.
        while response:

        # Will only get the comments.
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                with open('description_file', 'a', encoding="utf-8") as f:
                    f.write(comment)
                    f.close()
                comments.append(comment)
                comment_id = item['snippet']['topLevelComment']['id']      
                comment_ids.append(comment_id)
                reply_count = item['snippet']['totalReplyCount']  
                replies.append(reply_count)
                like_count = item['snippet']['topLevelComment']['snippet']['likeCount']             
                likes.append(like_count)
                comment_published = item['snippet']['topLevelComment']['snippet']['publishedAt']              
                published_dates.append(comment_published)

 # Will get the replies (fetches the reply information from a comment video)
            for item in response['items']:
                if item['snippet']['totalReplyCount'] >= 1:
                    for i in range(len(item['replies']['comments'])):                       
                        rep_comment = item['replies']['comments'][i]['snippet']['textOriginal']
                        with open('description_file', 'a', encoding="utf-8") as f:
                            f.write(rep_comment)
                            f.write('----\n----\n----\n---->\n')
                            f.close()
                        reply_comment.append(rep_comment)                                 
                        publish_date = item['replies']['comments'][i]['snippet']['publishedAt']        
                        reply_posted.append(publish_date)                  
                        like_count = item['replies']['comments'][i]['snippet']['likeCount']           
                        reply_likes.append(like_count)
                else:
                    pass

    # Finally, return the data back
    return {
        'Comments': comments,
        'Comment Id': comment_ids,
        'Reply Count': replies,
        'Likes Count': likes,
        'Published Date of Comment': published_dates,
        'Replies': reply_comment,
        'Published Date of Reply': reply_posted,
        'Likes on Reply': reply_likes,
        # below includes comments + replies.
        'Number of Total Comments': len(comment_ids)+len(reply_comment)
    }
    