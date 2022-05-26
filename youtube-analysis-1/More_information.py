#################### Import Libraries ##########################################
from googleapiclient.discovery import build
import pandas as pd
################################################################################
api_key='APIKEY'
youtube = build('youtube','v3', developerKey=api_key)

#function gets a YouTube service object
def get_video_details(youtube, **kwargs):
    return youtube.videos().list(
        part="snippet,contentDetails,statistics",
        **kwargs
    ).execute()

#function gets a YouTube service object - For searching using keywords
def search(youtube, **kwargs):
    return youtube.search().list(
        part="snippet",
        **kwargs
    ).execute()


#define a function that takes a response returned from the above get_video_details() function
def video_infos(video_response,video_url):
    items = video_response.get("items")[0]
    # get the snippet, statistics & content details from the video response
    snippet         = items["snippet"]
    statistics      = items["statistics"]

    channel_title = snippet["channelTitle"]
    title         = snippet["title"]
    description   = snippet["description"]
    publish_date  = snippet["publishedAt"]
    # get stats infos
    view_count    = statistics["viewCount"]

    if "commentCount" in statistics:
        comment_count = statistics["commentCount"]
    else:
        comment_count=0
    if "likeCount" in statistics:
        Likes_count = statistics["likeCount"]
    else:
        Likes_count=0

    dictionary=dict(
    Channel_Title=channel_title,
    Title= title,
    Description=description,
    Publish_date=publish_date,
    Number_of_views= view_count,
    Number_of_Likes=Likes_count,
    Number_of_Comments=comment_count,
    Video_url=video_url)
    return dictionary

# search for the query 'ukraine'
response = search(youtube, q="ukrainewar", maxResults=50) #use covid19,etc.
items = response.get("items")
data=[]
for item in items:
    # get the video ID
    video_id = item["id"]["videoId"]
    # easily construct video URL by its ID
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    # get the video details
    video_response = get_video_details(youtube, id=video_id)
    # print the video details
    datas=video_infos(video_response,video_url)
    data.append(datas)

#Convert data into dataframe for further analysis
video_info=pd.DataFrame(data)
print(video_info)

#data types needs to be converted to numeric for sensible columns
video_info['Number_of_views']=pd.to_numeric(video_info['Number_of_views'])
video_info['Number_of_Likes']=pd.to_numeric(video_info['Number_of_Likes'])
video_info['Number_of_Comments']=pd.to_numeric(video_info['Number_of_Comments'])

#get the published date of the video
video_info['Publish_date']=pd.to_datetime(video_info['Publish_date']).dt.date

#Get the data in CSV format
video_info.to_csv('data.csv')


#Same way we can search for any specific keywords and their related videos

#code reference: https://www.thepythoncode.com/article/using-youtube-api-in-python