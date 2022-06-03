There are two aspects to this project. 
To get data from:
# mastodon
Working with the Mastodon social network API. 

The above task is currently on hold while the Youtube API is being used to get the required data. 

For the Youtube API to function properly, the prerequesites are mentioned below: 

Requirements:
 Python 2.7 or Python 3.5+
 The pip package management tool
 The Google APIs Client Library for Python
 pip install --upgrade google-api-python-client
 The google-auth-oauthlib and google-auth-httplib2 libraries for user authorization
 pip install --upgrade google-auth-oauthlib google-auth-httplib2

oauth is not needed at the moment since the project is not going live yet. 

1) Once you make sure the above are installed, you will have to create a google developer account to get access to an API key. 
https://console.cloud.google.com/

2) This is the link for the youtube data API which is used to collect all the data: https://developers.google.com/youtube/v3/docs/
This link includes the documentation for the methods used.

3) The file yt2.py is the main file containing all the methods to get the data. 

4) Comments throughout the file yt2.py help  explaining the methods. 



There are 5 methods as of now: 

video_identification(): This method returns the videoId given a query and maxResults by the user. maxResults specifies the maximum number of items that will be returned. Allowed value are 0 to 50 inclusive at once. 

get_vid_stats(): This method returns all the information regarding a video. Needs the videoId as input. Can be changed to gather more information. 

get_vid_description(): This method returns the entire description section of a video as txt and stores it in a file. 

get_desc_links(): This method uses regex to collect and return links from a file. Input is the file created by get_vid_description() method. 

fetch_comments(): This method returns all the information regarding comments. Returns 'comments', 'like count', 'published date', 'replies', 'published date for reply' and 'total comments'. Input required is videoId and maxResults. maxResults specifies the maximum number of items that will be returned. Allowed values are 0 to 100 inclusive at once. The method runs in loop to cover the entire quota of 10,000 API calls in one day.  




--------------------------------------------------------------------

At present, we are able to fetch all the links from a video in it's description section and store that in a file. 

Next task is to get the links from the comments section of the same video and store it in a seperate column in a dataframe. This way, there will be clear differentiation between links that are from the description section and one's that are from the comments and replies section. 

From trial and error, it has been found that description links are usually way more than links in the comments and replies section. 

--------------------------------------------------------------------