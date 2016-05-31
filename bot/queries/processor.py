import re
import yaml
import importlib
import string
import logging
from utils.url_shortener import shorten

english = 'abcdefghijklmnopqrstuvwxyz'
russian = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

sorries = {
    'en': ["Sorry, I don't understand you :(", "An error occurred, sorry"],
    'ru': ["Извини, я тебя не понимаю :(", "Произошла ошибка, извините"]
}


def process_text(query, params={}):
    if query is 'sendsorryplease':
        return sorries['en'][0]
    ex = query.lower()
    if ex[0] in english:
        lang = 'en'
    elif ex[0] in russian:
        lang = 'ru'
    else:
        lang = 'en'
    try:
        file = yaml.load(open('bot/queries/{}.yml'.format(lang), encoding='utf-8'))
    except FileNotFoundError:
        file = yaml.load(open('{}.yml'.format(lang), encoding='utf-8'))
    for source, regexes in file.items():
        for i, regex in enumerate(regexes):
            if 'priority' not in regex:
                regex['priority'] = 0
            regexes[i] = regex
        regexes = sorted(regexes, key=lambda x: x['priority'], reverse=True)
        for regex in regexes:
            if re.match(regex['regex'], ex):
                try:
                    logging.info('{} provider: {}'.format(source, regex))
                    if not regex['eval']:
                        ex = ''.join([x for x in ex if x not in string.punctuation])
                    lib = importlib.import_module('bot.queries.providers.{}'.format(source))
                    if type(regex['query']) is list:
                        request = [re.search(regex['regex'], ex).group(group) for group in regex['query']]
                    else:
                        request = re.search(regex['regex'], ex).group(regex['query'])
                    res = lib.get(request, params, lang)
                    if 'url' in res:
                        res['url'] = shorten(res['url'])
                    if res['content'] == 'nan':
                        if type(request) is list:
                            return regex['error'].format(*request) + (res['url'] if 'url' in res else '')
                        else:
                            return regex['error'].format(request) + (res['url'] if 'url' in res else '')
                    return res
                except Exception:
                    return sorries[lang][1]
    return sorries[lang][0]
