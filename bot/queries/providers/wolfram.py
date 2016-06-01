import wolframalpha
from urllib.parse import quote_plus
from .baseprovider import BaseProvider


class WolframProvider(BaseProvider):
    @staticmethod
    def get(query, config, params={}, lang='en'):
        client = wolframalpha.Client(config['wolfram_appid'])
        response = client.query(query)
        res = [pod for pod in response.pods if 'result' in pod.title.lower() or 'response' in pod.title.lower()]
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
        content['url'] = 'https://www.wolframalpha.com/input/?i=' + quote_plus(query)
        return content
