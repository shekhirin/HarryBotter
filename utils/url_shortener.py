import requests
import json
import os


def shorten(url):
    response = requests.post(
        'http://api.adf.ly/v1/shorten',
        data={
            "url": url,
            '_api_key': os.environ['adfly_public_key'],
            '_user_id': os.environ['adfly_user_id']
        }
    )
    try:
        return json.loads(response.text)['data'][0]['short_url']
    except KeyError:
        return url