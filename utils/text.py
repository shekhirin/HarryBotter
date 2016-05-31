def restrict_len(content):
    if len(content) > 320:
        content = content[:310].strip() + '...'
    return content


def detect_language(word):
    from langdetect import detect
    russian = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

    if word[0] in russian:
        lang = 'ru'
    else:
        lang = detect(word)
    return lang
