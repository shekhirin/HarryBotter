import requests
import json
import os


def shorten(url, config):
    response = requests.post(
        'http://api.adf.ly/v1/shorten',
        data={
            "url": url,
            '_api_key': config['adfly_public_key'],
            '_user_id': config['adfly_user_id']
        }
    )
    try:
        return json.loads(response.text)['data'][0]['short_url']
    except KeyError:
        return url