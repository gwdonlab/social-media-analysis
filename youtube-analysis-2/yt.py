#%%
# API client library
import googleapiclient.discovery
# API information
api_service_name = "youtube"
api_version = "v3"
# API key
DEVELOPER_KEY = ""
# API client
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY)
# 'request' variable is the only thing you must change
# depending on the resource and method you need to use
# in your query
req = youtube.search().list(
        part="id, snippet",
        type='video',
        q="ukraine",
        videoDuration='short',
        videoDefinition='high',
        maxResults=15,
        fields="items(id(videoId), snippet(publishedAt, channelId, channelTitle, title, description, thumbnails(high)))"
)
# Query execution
response = req.execute()
# Print the results
print(response)
# %%
for key, value in response.items():
    print(key)
    
# %%