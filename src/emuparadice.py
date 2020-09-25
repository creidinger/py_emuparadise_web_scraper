import re

import requests
from bs4 import BeautifulSoup


def get_data(url):
    """Get HTML data from a site
    args:
        url: the url to the site we're scraping
    """

    try:
        r = requests.get(url)
    except Exception as e:
        raise e
    else:
        print('Scrape success')

    try:
        bs = BeautifulSoup(r.text, 'html.parser')
    except Exception as e:
        raise e

    try:
        endpoints = bs.find_all('a', {'class', 'gamelist'})
    except AttributeError as e:
        raise AttributeError('Invalid attribute')
    except Exception as e:
        raise e

    # for e in endpoints:
    #     print(e.get('href'))

    return endpoints


def filter_endpoints(endpoints):
    """Remove unwanted links from the list
    args:
        endpoints: the list of endpoints received from the scrape
    """
    filtered = []
    trash_reg = re.compile(r'(japan|Japan|\(j\)|\(J\)|germany|German|\(g\)|\(G\)|\(s\)|\(S\)|\(f\)|\(F\)|Essential_PlayStation|Interactive_CD_Sampler|PlayStation_Underground_|PlayStation_Picks|_Magazine_|Official_PlayStation_|Official_UK_PlayStation_|_Demo_)')

    for e in endpoints:
        match = trash_reg.search(e.get('href'))
        if not match:
            filtered.append(e.get('href'))
            # print(e.get('href'))

    return filtered


def get_game_ids(endpoints):
    """Split each enpoint down to its game id and append
    the ID to a new array
    args:
        endpoints: the filtered list of game endpoints
    """

    ids = []

    for e in endpoints:
        arr = e.split('/')
        ids.append(arr[-1])

    return ids


def build_download_links(game_ids):
    """ make download links for each game ID
    args:
        game_ids: The list of ids stripped from each endpoint
    """

    site = 'http://50.7.189.186/'
    site = 'http://www.emuparadise.me/'

    dl_links = []

    for id in game_ids:
        dl_url = f"{site}roms/get-download.php?gid={id}&test=true"
        dl_links.append(dl_url)

    return dl_links


games = get_data(
    url='https://www.emuparadise.me/Sony_Playstation_ISOs/List-All-Titles/2')

filtered = filter_endpoints(endpoints=games)
for f in filtered:
    print(f)
print(f"total: {len(filtered)}")

game_ids = get_game_ids(endpoints=filtered)
print(game_ids)

links = build_download_links(game_ids=game_ids)
print(links)
