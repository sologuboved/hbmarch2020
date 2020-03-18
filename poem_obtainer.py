import random
import requests
from bs4 import BeautifulSoup

_prefix = 'http://поэтика.рф'
# random.seed(1)


def grab_random(items, excluded_names=()):
    if excluded_names:
        acceptable = list()
        for item in items:
            item = item.find('a')
            name = item.get_text().strip()
            if name in excluded_names:
                continue
            acceptable.append((name, item.get('href').strip()))
        return acceptable[random.randrange(len(acceptable))]
    item = items[random.randrange(len(items))].find('a')
    return item.get_text().strip(), item.get('href').strip()


def choose_poet(period):
    return grab_random(BeautifulSoup(
        requests.get(_prefix + '/раздел/' + period).content, 'lxml'
    ).find('div', {'id': 'period-authors'}).find_all('li'),
                       ("Асадов Эдуард", "Надсон Семен"))


def choose_title(period):
    name, link_postfix = choose_poet(period)
    return name, grab_random(BeautifulSoup(
        requests.get(_prefix + link_postfix + '/сборники-стихов/все').content, 'lxml'
    ).find_all('li', {'class': 'node-item'}))


def scrape_poem(period):
    name, (title, link_postfix) = choose_title(period)
    link = _prefix + link_postfix
    poem = BeautifulSoup(requests.get(link).content, 'lxml').find('div', {'class': "content clearfix"})
    for sup in poem.find_all('sup'):
        sup.replace_with('[{}]'.format(sup.text))
    for note in poem.find_all('div', {'class': 'note'}):
        if note.text == 'Примечания':
            note.replace_with('\n<i>Примечания</i>\n')
    return link, name, title, poem.text


def get_poems():
    return [scrape_poem(period) for period in (
        'Поэзия-XVIII-века',
        'Золотой-век-русской-поэзии',
        ('Поэзия-Серебряного-века', 'Поэзия-советского-периода')[random.choice([0] * 4 + [1])])]
