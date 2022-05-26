from googleapiclient.discovery import build

api_key='APIKEY'
channel_id='UCnz-ZXXER4jOvuED5trXfEA'
youtube = build(
        'youtube','v3', developerKey=api_key)


#Function for scraping channel stats

def channel_statistics(youtube,channel_id):
    request=youtube.channels().list(part='snippet,contentDetails,statistics',id=channel_id
                                    )
    response=request.execute()
    print(response)
    print('*'*100)
    data=dict(channel_name=response['items'][0]['snippet']['title'],
              subscribers=response['items'][0]['statistics']['subscriberCount'],
              views=response['items'][0]['statistics']['viewCount'],
              videos=response['items'][0]['statistics']['videoCount'])
    return data

print(channel_statistics(youtube,channel_id))


