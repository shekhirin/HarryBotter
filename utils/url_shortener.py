import requests
import json
import os


def shorten(url):
    response = requests.post(
        'https://www.googleapis.com/urlshortener/v1/url?key={}'.format(os.environ['google_api_key']),
        json={"longUrl": url}
    )
    return json.loads(response.text)['id']
