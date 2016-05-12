from yandex_translate import YandexTranslate
import os
from pycountry import languages


def get(query, lang='en'):
    translator = YandexTranslate(key=os.environ['yandex_translate_key'])
    to_translate = query[0]
    try:
        to_lang = languages.get(name=translator.translate(query[1], 'en')['text'][0].replace('in ', '').capitalize()).iso639_1_code
    except KeyError:
        return 'nan'
    return ' '.join(translator.translate(to_translate, '{}-{}'.format(lang, to_lang))['text'])
