from telegram import constants


def process_poem(link, name, title, poem):
    print(link)
    poem = '<b>{}</b> - <a href="{}">{}</a>\n\n{}'.format(name, link, title, poem.strip())
    if len(poem) > constants.MAX_MESSAGE_LENGTH:
        return split(poem)
    return [poem]


def split(poem):
    chunks = list()
    chunk = str()
    for line in poem.split('\n'):
        line += '\n'
        if len(chunk) + len(line) > constants.MAX_MESSAGE_LENGTH:
            chunks.append(chunk)
            chunk = line
        else:
            chunk += line
    chunks.append(chunk)
    return chunks
