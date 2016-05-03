import requests
import json


class Facebook:
    def __init__(self, access_token):
        self.access_token = access_token

    def message(self, data):
        if hasattr(data, 'json'):
            data = data.json
        post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(self.access_token)
        data = json.dumps(data)
        response = requests.post(post_url, headers={"Content-Type": "application/json"}, data=data)