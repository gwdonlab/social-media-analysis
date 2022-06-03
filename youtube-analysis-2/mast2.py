from socket import timeout
import requests

url = 'https://mastodon.social/api/v1/statuses'
auth = {'authorization': 'Bearer BEARER_TOKEN'}
stat = {'status': "From py!!", 'sensitive': True}
response = requests.post(url, headers = auth, data = stat)

import requests

url = 'https://mastodon.social/api/v2/search'
auth = {'authorization': 'Bearer BEARER_TOKEN'}
stat = {'q': "cat", 'limit': 2}
response = requests.get(url, headers = auth, params= stat).json()

toot_note = []
for i in range(len(response['accounts'])):
    toot_note.append(response['accounts'][i]['note'])

date_created = []
for i in range(len(response['accounts'])):
    lt.append(response['accounts'][i]['created_at'])