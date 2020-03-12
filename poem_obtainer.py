import random
import requests
from bs4 import BeautifulSoup

_prefix = 'http://поэтика.рф'
# random.seed(1)


def grab_random(items):
    item = items[random.randrange(len(items))].find('a')
    return item.get_text().strip(), item.get('href').strip()


def choose_poet(period):
    return grab_random(BeautifulSoup(
        requests.get(_prefix + '/раздел/' + period).content, 'lxml'
    ).find('div', {'id': 'period-authors'}).find_all('li'))


def choose_title(period):
    name, link_postfix = choose_poet(period)
    return name, grab_random(BeautifulSoup(
        requests.get(_prefix + link_postfix + '/сборники-стихов/все').content, 'lxml'
    ).find_all('li', {'class': 'node-item'}))


def scrape_poem(period):
    name, (title, link_postfix) = choose_title(period)
    link = _prefix + link_postfix
    return link, name, title, BeautifulSoup(
        requests.get(link).content, 'lxml'
    ).find('div', {'class': "content clearfix"}).text


def get_poems():
    return [scrape_poem(period) for period in (
        'Поэзия-XVIII-века',
        'Золотой-век-русской-поэзии',
        ('Поэзия-Серебряного-века', 'Поэзия-советского-периода')[random.randrange(3) % 2])]
