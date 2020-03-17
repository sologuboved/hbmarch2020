import requests
from bs4 import BeautifulSoup
from time import sleep
from telegram import Bot, ParseMode
from poem_processor import process_poem
from tkn import TOKEN, TRACEBACKS_ID


def see_output(link_postfix, post):
    link = 'https://поэтика.рф/поэты/' + link_postfix
    soup = BeautifulSoup(requests.get(link).content, 'lxml')
    name, title = map(str.strip, soup.find('title').text.split('–'))
    poem = soup.find('div', {'class': "content clearfix"})
    for sup in poem.find_all('sup'):
        sup.replace_with('[{}]'.format(sup.text))
    for note in poem.find_all('div', {'class': 'note'}):
        if note.text == 'Примечания':
            note.replace_with('\n<i>Примечания</i>\n')
    poem = process_poem(link, name, title, poem.text)
    if post:
        bot = Bot(token=TOKEN)
        for chunk in poem:
            bot.send_message(chat_id=TRACEBACKS_ID,
                             text=chunk,
                             parse_mode=ParseMode.HTML)
            sleep(1)
    else:
        print(poem)


if __name__ == '__main__':
    see_output('карамзин/стихи/16243/странность-любви-или-бессонница', True)
    # see_output('ломоносов/стихи/1930/в-тополевой-тени-гуляя-муравей', False)
