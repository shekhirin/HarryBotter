def get(query, lang='en'):
    if lang is 'ru':
        return {
            'type': 'text',
            'content':
                """
                Скоро здесь будет помощь!
                """
        }
    else:
        return {
            'type': 'text',
            'content':
                """
                Help will be there soon!
                """
        }