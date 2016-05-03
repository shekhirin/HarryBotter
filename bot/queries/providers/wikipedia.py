import wikipedia
from utils.url_shortener import shorten
from utils.text_formatter import restrict_len


def get(query, lang='en'):
    wikipedia.set_lang(lang)
    search = wikipedia.search(query)
    if not search:
        return 'nan'
    try:
        result = wikipedia.page(search[0])
    except wikipedia.DisambiguationError:
        return 'Too broad query "{}"\n{}'.format(query, 'https://{}.wikipedia.org/wiki/{}'.format(lang, query))
    content = result.content.split('\n')[0]
    url = shorten(result.url)
    content = restrict_len(content, url)
    return '{}\n{}'.format(content, url)
