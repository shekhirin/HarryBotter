def restrict_len(content):
    if len(content) > 320:
        content = content[:310].strip() + '...'
    return content
