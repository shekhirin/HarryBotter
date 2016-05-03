import wolframalpha
import os
from utils.text_formatter import restrict_len


def get(query, lang='en'):
    client = wolframalpha.Client(os.environ['wolfram_appid'])
    response = client.query(query)
    res = [pod.text for pod in response.pods if pod.title == 'Result' or pod.title == 'Response']
    if len(res) > 0:
        content = '\n'.join(res)
    else:
        content = 'nan'
    url = 'https://www.wolframalpha.com/input/?i=' + query.replace(' ', '+')
    content = restrict_len(content, url)
    return '{}\n{}'.format(content, url)
