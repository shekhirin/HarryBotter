import wikipedia
from utils.url_shortener import shorten


def get(query, lang='en'):
    wikipedia.set_lang(lang)
    search = wikipedia.search(query)
    if not search:
        return 'nan'
    result = wikipedia.page(search[0])
    content = result.content
    content = (content[:content.find('(')-1] + content[content[:100].rfind(')')+1:]).split('. ')[0]
    url = shorten(result.url)
    if len(content) + len(url) > 320:
        content = content[:310-len(url)-3].strip() + '...'
    else:
        content += '.'
    return '{}\n{}'.format(content, url)