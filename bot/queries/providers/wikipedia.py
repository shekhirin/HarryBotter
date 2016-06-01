import wikipedia
from .baseprovider import BaseProvider


class WikipediaProvider(BaseProvider):
    @staticmethod
    def get(query, config, params={}, lang='en'):
        wikipedia.set_lang(lang)
        search = wikipedia.search(query)
        if not search:
            return {
                'content': 'nan'
            }
        try:
            result = wikipedia.page(search[0])
        except wikipedia.DisambiguationError:
            return {
                'type': 'text',
                'content': 'https://{}.wikipedia.org/wiki/{}'.format(lang, query)
            }
        content = {
            'type': 'text',
            'content': result.content.split('\n')[0],
            'url': result.url
        }
        return content
