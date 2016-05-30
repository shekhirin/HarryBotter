import wolframalpha
import os


def get(query, lang='en'):
    client = wolframalpha.Client(os.environ['wolfram_appid'])
    response = client.query(query)
    res = [pod for pod in response.pods if pod.title == 'Result' or pod.title == 'Response']
    if len(res) > 0 and not any(v is None for v in res):
        if res[0].img is not None:
            content = {
                'type': 'image',
                'content': res[0].img
            }
        elif res[0].text is not None:
            content = {
                'type': 'text',
                'content': '\n'.join(res),
            }
        else:
            content = {
                'content': 'nan'
            }
    else:
        content = {
            'content': 'nan'
        }
    content['url'] = 'https://www.wolframalpha.com/input/?i=' + query.replace(' ', '+')
    return content
