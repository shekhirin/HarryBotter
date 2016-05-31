import requests
import json
import logging


class Facebook:
    def __init__(self, access_token):
        self.access_token = access_token

    def message(self, data):
        def process_item(data_item):
            post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(self.access_token)
            content = json.dumps(data_item)
            response = requests.post(post_url, headers={"Content-Type": "application/json"}, data=content)
            logging.info('Facebook response: ' + response.content)

        if type(data) is list:
            for item in data:
                if hasattr(item, 'json'):
                    item = item.json
                    process_item(item)
        else:
            if hasattr(data, 'json'):
                data = data.json
            process_item(data)
