import yaml


def get(query, config, params={}, lang='en'):
    if lang in config['available_langs']:
        file = yaml.load(open('bot/queries/{}.yml'.format(lang)))
        result = {}
        for (provider, regexes) in sorted(file.items(), reverse=True):
            for regex in regexes:
                if 'example' not in regex:
                    continue
                if provider not in result:
                    result[provider] = ''
                result[provider] += regex['example'] + '\n'
        return {
            'type': 'text',
            'content': '\n\n'.join(['=={}==\n{}'.format(x.upper(), y) for x, y in result.items()])
        }
    else:
        return {
            'content': 'nan'
        }
