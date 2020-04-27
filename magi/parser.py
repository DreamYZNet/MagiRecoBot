from bs4 import BeautifulSoup
import requests
import re
from timer import time_function, Timer

symbols_to_stars = {
    '1️⃣': '★',
    '2️⃣': '★★',
    '3️⃣': '★★★',
    '4️⃣': '★★★★',
    '5️⃣': '★★★★★',
    }

stars_to_symbols = {v: k for k, v in symbols_to_stars.items()}

@time_function
def find_girl(keywords, listing = False):
    domain = 'https://magireco.fandom.com'
    with Timer() as time:
        # page = requests.get(domain+'/wiki/Magical_Girl_Stats_List_NA')
        page = requests.get(domain+'/wiki/Magical_Girl_Stats_List')
    soup = BeautifulSoup(page.content, 'html.parser')

    girl_url = None
    girl_list = []  # Only used when listing is true

    # Search through the page to find a matching girl and link
    table = soup.find(id='mw-content-text').table  # full of tds which are the rows
    for row in table.find_all('tr', recursive=False)[1:]:
        a = row.p.a
        found = True
        for kw in keywords:
            if not re.compile(kw, re.IGNORECASE).search(a['title']):
                found = False
                break
        if found:
            girl_url = domain + a['href']
            if listing:
                girl_list.append({'url': girl_url, 'name': a['title']})
            else:
                break

        # a_tag = table.find(title=re.compile(keywords, re.IGNORECASE))  # turns out this is basically as fast as the above
    if len(girl_list) > 0:
        return girl_list
    elif girl_url:
        return girl_url


@time_function
def parse_girl(url):

    with Timer() as time:
        page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    content = soup.find(id='mw-content-text')
    table = content.find(class_='wikitable')
    current_tag = table

    data = {}

    # URL
    data['url'] = url

    # Elemental type
    try:
        elemental = table.find(alt=re.compile('AttributeIcon'))
        data['element'] = elemental['alt'].split()[1]
        data['element_icon'] = elemental['data-src']
        current_tag = elemental
    except:
        print('Parser Exception: elemental')

    # English and Japanese names
    try:
        name_tag = current_tag.find_next('p')
        data['name'] = ''.join(name_tag.find_all(text=True)).rstrip(' \n')
        current_tag = name_tag
    except:
        print('Parser Exception: names')

    # Base stars
    try:
        rarity = current_tag.find_next('p')
        data['rarity'] = rarity.text.rstrip(' \n')
        current_tag = rarity
    except:
        print('Parser Exception: rarity')

    # Images
    try:
        data['images'] = {}
        char_info = table.find(class_='char-info')
        char_images = char_info.find_all(class_="image")
        for img in char_images:
            stars = img.find_parent(class_='tabbertab')['title']
            href = img['href']
            data['images'][stars] = href
        current_tag = char_images[-1]
    except:
        print('Parser Exception: images')

    # Discs and disc images
    try:
        data['discs'] = []
        data['disc_icons'] = []
        disc_images = table.find(title='Discs').find_next('td').find_all('a')
        for a in disc_images:
            data['disc_icons'].append(a.img['data-src'])
            data['discs'].append(a.img['alt'])
        current_tag = disc_images[-1]
        print(current_tag)
    except:
        print('Parser Exception: discs')

    # Seiyuu
    try:
        artist = current_tag.find_next(title='Artists').find_next('p')
        seiyuu = ''.join(artist.find_all(text=True)).rstrip(' \n')
        data['seiyuu'] = seiyuu
        current_tag = artist
    except:
        print('Parser Exception: seiyuu')

    try:
        data['stats'] = {}
        # print(current_tag)
        stats = current_tag.find_next('a', title='Spirit Enhancement')
        if not stats:
            for i in range(5, 0, -1):
                stats = current_tag.find_next('td', text=f'{i}★')
                if stats:
                    break
        if stats:
            hp_tag = stats.find_next('td')
            data['stats']['hp'] = hp_tag.text.split()[2]
            atk_tag = hp_tag.find_next('td')
            data['stats']['atk'] = atk_tag.text.split()[2]
            def_tag = atk_tag.find_next('td')
            data['stats']['def'] = def_tag.text.split()[2]
        current_tag = stats
    except:
        print('Parser Exception: max-stats')

    # END OF MAIN PAGE
    # QUOTES
    try:
        page = requests.get(url+'/Quotes')
        soup = BeautifulSoup(page.content, 'html.parser')
        content = soup.find(id='mw-content-text')

        # quotes = content.find(title='Regular Quotes')
        quote = content.find('b', text='[NA]').find_next('td').text.strip()####quotes is none
        data['quotes'] = [quote]
    except:
        print('Parser Exception: quotes')

    # TODO
    # max stats, summary, lines


    return data

    #print(json.dumps(data, indent=2))

def parse_girl_images(url):
    with Timer() as time:
        page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    content = soup.find(id='mw-content-text')
    table = content.find(class_='wikitable')

    data = {}

    # Images
    data['images'] = {}
    char_info = table.find(class_='char-info')
    char_images = char_info.find_all(class_="image")
    for img in char_images:
        stars = img.find_parent(class_='tabbertab')['title']
        href = img['href']
        data['images'][stars] = href

    return data
