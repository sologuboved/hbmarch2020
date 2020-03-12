def process_poem(link, name, title, poem):
    return '<b>{}</b> - <a href="{}">{}</a>\n\n{}'.format(name, link, title, poem.strip())
