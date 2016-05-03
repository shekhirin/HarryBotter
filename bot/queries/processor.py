import re
import yaml
import importlib
import string

english = 'abcdefghijklmnopqrstuvwxyz'
russian = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

sorries = {
    'en': "Sorry, I don't understand you :(",
    'ru': "Извини, я тебя не понимаю :("
}


def process_text(query):
    if query[0] in english:
        lang = 'en'
    elif query[0] in russian:
        lang = 'ru'
    else:
        lang = 'en'
    try:
        file = yaml.load(open('bot/queries/{}.yml'.format(lang), encoding='utf-8'))
    except FileNotFoundError:
        file = yaml.load(open('{}.yml'.format(lang), encoding='utf-8'))
    query = query.lower()
    for source, regexes in file.items():
        for regex in regexes:
            if not regex['eval']:
                ex = ''.join([x for x in query if x not in string.punctuation])
            else:
                ex = query
            if re.match(regex['regex'], ex):
                lib = importlib.import_module('bot.queries.providers.{}'.format(source))
                request = re.search(regex['regex'], ex).group(regex['query'])
                res = lib.get(request, lang)
                if res == 'nan':
                    return regex['error'].format(request)
                return res
    return sorries[lang]
