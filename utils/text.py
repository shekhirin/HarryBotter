def restrict_len(content):
    if len(content) > 320:
        content = content[:310].strip() + '...'
    return content


def detect_language(config, langs, word):
    from yandex_translate import YandexTranslate
    translator = YandexTranslate(config['yandex_translate_key'])
    russian = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

    if word[0] in russian:
        lang = 'ru'
    else:
        lang = translator.detect(word)
        if lang not in langs:
            lang = 'en'
    return lang
