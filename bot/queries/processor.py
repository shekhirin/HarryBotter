import re
import yaml
import importlib
import string
import logging

english = 'abcdefghijklmnopqrstuvwxyz'
russian = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

sorries = {
    'en': "Sorry, I don't understand you :(",
    'ru': "Извини, я тебя не понимаю :("
}


def process_text(query):
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
    logging.info('{}.yml loaded'.format(lang))
    for source, regexes in file.items():
        for regex in regexes:
            if re.match(regex['regex'], ex):
                try:
                    logging.info('Using {} provider with regex {}'.format(source, regex))
                    if not regex['eval']:
                        ex = ''.join([x for x in ex if x not in string.punctuation])
                    lib = importlib.import_module('bot.queries.providers.{}'.format(source))
                    if type(regex['query']) is list:
                        request = [re.search(regex['regex'], ex).group(group) for group in regex['query']]
                    else:
                        request = re.search(regex['regex'], ex).group(regex['query'])
                    res = lib.get(request, lang)
                    if res['content'] == 'nan':
                        if type(request) is list:
                            return regex['error'].format(*request) + (res['url'] if 'url' in res else '')
                        else:
                            return regex['error'].format(request) + (res['url'] if 'url' in res else '')
                    return res
                except Exception:
                    return sorries[lang]
    return sorries[lang]
