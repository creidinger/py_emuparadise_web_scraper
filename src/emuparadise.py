import re

import requests
from bs4 import BeautifulSoup


class ScrapeEmuparadise():
    """Web Scraper for emu paradise.
    Feed the scraper the 'List-All-Titles' link for a platform and the scraper
    will make download links for all US and Eruopean games.
    """

    def __init__(self, url):
        self.url = url
        # self.server = 'http://50.7.189.186/'
        self.server = 'http://www.emuparadise.me/'
        self.trash_reg = re.compile(
            r'(japan|Japan|\(j\)|\(J\)|germany|German|\(g\)|\(G\)|\(s\)|\(S\)|\(f\)|\(F\)|Essential_PlayStation|Interactive_CD_Sampler|PlayStation_Underground_|PlayStation_Picks|_Magazine_|Official_PlayStation_|Official_UK_PlayStation_|_Demo_|Demo_|_\(Demo\)|Baseball|FIFA|Soccer|Madden|Boxing|Golf|ESPN_|MLB_|NASCAR_|NBA_|NCAA_|NFL_|NHL_|PGA_|WCW_|WWF_|radicalgames|Timeless_Math|Pizza_Hut|Math_on_the_Move|GameShark|Fisherman|Formula_One|Formula_1|Fox_Sports|Barbie|Fishing|Tennis)')
        self.game_endpoints = []
        self.filtered_endpoints = []
        self.games_meta = []

    def main(self):
        """Run all the functions"""
        self.get_data()
        self.filter_endpoints()
        self.build_game_meta()

    def get_data(self):
        """Scrape HTML data from emuparadise and return a list of games"""

        try:
            r = requests.get(self.url)
        except Exception as e:
            raise e
            return False
        else:
            print('Scrape success')

        try:
            # convert html to a BeautifulSoup Object
            bs = BeautifulSoup(r.text, 'html.parser')
        except Exception as e:
            raise e
            return False

        try:
            # find all <a> tages that link to a game
            self.game_endpoints = bs.find_all('a', {'class', 'gamelist'})
        except AttributeError as e:
            raise AttributeError('Invalid attribute')
            return False
        except Exception as e:
            raise e
            return False

        return True

    def filter_endpoints(self):
        """Remove unwanted links from the list of scraped endpoints"""

        # iterate over the list of endpoints and check against the regular
        # expression above. If no match is found, add the endpoint to the
        # filtered list.
        for e in self.game_endpoints:
            link = e.get('href')
            match = self.trash_reg.search(link)
            if not match:
                self.filtered_endpoints.append(link)
        return True

    def build_game_meta(self):
        """Turn each filtered enpoint into a dict"""

        for e in self.filtered_endpoints:
            arr = e.split('/')
            download_endpoint = f"{self.server}roms/get-download.php?gid={arr[-1]}&test=true"
            meta = {'system': arr[1], 'name': arr[2], 'id': arr[3], 'download_endpoint': download_endpoint}
            self.games_meta.append(meta)

    def download_game(self, game_dict, chunk_size=128):

        url = game_dict.get('download_endpoint')
        headers = {'referer': self.server}
        save_path = f"./files/{game_dict.get('name')}.7z"

        try:
            r = requests.get(url, stream=True, headers=headers)
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
        except Exception as e:
            raise e


if __name__ == "__main__":
    scrape = ScrapeEmuparadise(
        url='https://www.emuparadise.me/Sony_Playstation_ISOs/List-All-Titles/2')
    scrape.main()

    i = 0
    for m in scrape.games_meta:
        print(m)
        if i == 100:
            scrape.download_game(m)
        i += 1
