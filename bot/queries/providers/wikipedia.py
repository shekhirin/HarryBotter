import wikipedia
from utils.url_shortener import shorten
from utils.text_formatter import restrict_len


def get(query, lang='en'):
    wikipedia.set_lang(lang)
    search = wikipedia.search(query)
    if not search:
        return 'nan'
    result = wikipedia.page(search[0])
    content = result.content
    content = (content[:content.find('(')-1] + content[content[:100].rfind(')')+1:]).split('. ')[0]
    url = shorten(result.url)
    content = restrict_len(content, url)
    return '{}\n{}'.format(content, url)