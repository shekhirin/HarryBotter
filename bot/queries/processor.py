import re
import yaml
import importlib
import string
import logging
from utils.url_shortener import shorten
from utils.text import detect_language

sorries = {
    'en': ["Sorry, I don't understand you :(", "An error occurred, sorry"],
    'ru': ["Извини, я тебя не понимаю :(", "Произошла ошибка, извините"]
}


def process_text(query, config, params={}):
    if query is 'sendsorryplease':
        return sorries['en'][0]
    ex = query.lower()
    lang = detect_language(config, config['available_langs'], ex)
    try:
        file = yaml.load(open('bot/queries/languages/{}.yml'.format(lang), encoding='utf-8'))
    except FileNotFoundError:
        file = yaml.load(open('languages/{}.yml'.format(lang), encoding='utf-8'))
    for source, regexes in file.items():
        for i, regex in enumerate(regexes):
            if 'priority' not in regex:
                regex['priority'] = 0
            regexes[i] = regex
        regexes = sorted(regexes, key=lambda x: x['priority'], reverse=True)
        for regex in regexes:
            if re.match(regex['regex'], ex):
                try:
                    logging.getLogger('app').log(logging.INFO, '{} provider: {}'.format(source, regex))
                    if not regex['eval']:
                        ex = ''.join([x for x in ex if x not in string.punctuation])
                    lib = importlib.import_module('bot.queries.providers.{}'.format(source))
                    if type(regex['query']) is list:
                        request = [re.search(regex['regex'], ex).group(group) for group in regex['query']]
                    else:
                        request = re.search(regex['regex'], ex).group(regex['query'])
                    res = getattr(lib, '{}Provider'.format(source.capitalize())).get(request, config, params, lang)
                    if 'url' in res:
                        res['url'] = shorten(res['url'], config)
                    if res['content'] == 'nan':
                        if type(request) is list:
                            return regex['error'].format(*request) + (res['url'] if 'url' in res else '')
                        else:
                            return regex['error'].format(request) + (res['url'] if 'url' in res else '')
                    return res
                except Exception:
                    return sorries[lang][1]
    return sorries[lang][0]
