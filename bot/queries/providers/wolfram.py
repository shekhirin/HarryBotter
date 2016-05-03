import wolframalpha
import os


def get(query, lang='en'):
    client = wolframalpha.Client(os.environ['wolfram_appid'])
    res = [pod.text for pod in client.query(query).pods if 'result' in pod.title.lower()]
    if len(res) > 0:
        return '\n'.join(res)
    else:
        return 'nan'
