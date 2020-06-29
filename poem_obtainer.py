import random
import requests
from bs4 import BeautifulSoup

_prefix = 'http://поэтика.рф'


# random.seed(21)


def process_sequence(sequence):
    sequence = [item.find('a') for item in sequence]
    sequence = [(item.get_text().strip(), item.get('href').strip()) for item in sequence]
    random.shuffle(sequence)
    return sequence


def get_poets(period):
    return process_sequence(BeautifulSoup(
        requests.get(_prefix + '/раздел/' + period).content, 'lxml'
    ).find('div', {'id': 'period-authors'}).find_all('li'))


def get_titles(poet_postfix):
    return process_sequence(BeautifulSoup(
        requests.get(_prefix + poet_postfix + '/сборники-стихов/все').content, 'lxml'
    ).find_all('li', {'class': 'node-item'}))


def scrape_poem(url):
    poem = BeautifulSoup(requests.get(url).content, 'lxml').find('div', {'class': "content clearfix"})
    for sup in poem.find_all('sup'):
        sup.replace_with('[{}]'.format(sup.text))
    for note in poem.find_all('div', {'class': 'note'}):
        if note.text == 'Примечания':
            note.replace_with('\n<i>Примечания</i>\n')
    return poem.text


def get_poem(period):
    for poet, poet_postfix in get_poets(period):
        if poet in ("Асадов Эдуард", "Грибоедов Александр", "Надсон Семен", "Рубцов Николай"):
            continue
        for title, poem_postfix in get_titles(poet_postfix):
            url = _prefix + poem_postfix
            poem = scrape_poem(url)
            if len(poem) <= 8000:
                return url, poet, title, poem


def get_poems():
    return [get_poem(period) for period in (
        'Поэзия-XVIII-века',
        'Золотой-век-русской-поэзии',
        ('Поэзия-Серебряного-века', 'Поэзия-советского-периода')[random.choice([0] * 4 + [1])])]


if __name__ == '__main__':
    print(get_poems())
