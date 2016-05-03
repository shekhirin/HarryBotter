def restrict_len(content, url):
    if len(content) + len(url) > 320:
        content = content[:310 - len(url) - 3].strip() + '...'
    else:
        content += '.'
    return content
