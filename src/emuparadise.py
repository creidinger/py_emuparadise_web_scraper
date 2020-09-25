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
            r'(japan|Japan|\(j\)|\(J\)|germany|German|\(g\)|\(G\)|\(s\)|\(S\)|\(f\)|\(F\)|Essential_PlayStation|Interactive_CD_Sampler|PlayStation_Underground_|PlayStation_Picks|_Magazine_|Official_PlayStation_|Official_UK_PlayStation_|_Demo_)')
        self.game_ids = []

        self.game_endpoints = []
        self.filtred_endpoints = []
        self.download_endpoints = []

    def main(self):
        """Run all the functions"""
        self.get_data()
        self.filter_endpoints()
        self.get_game_ids()
        self.build_download_links()

    def get_data(self):
        """Get HTML data from a site
        args:
            url: the url to the site we're scraping
        """

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
        """Remove unwanted links from the list
        args:
            endpoints: the list of endpoints received from the scrape
        """

        # iterate over the list of endpoints and check against the regular
        # expression above. If no match is found, add the endpoint to the
        # filtered list.
        for e in self.game_endpoints:
            match = self.trash_reg.search(e.get('href'))
            if not match:
                self.filtred_endpoints.append(e.get('href'))
        return True

    def get_game_ids(self):
        """Split each enpoint down to its unique game id and append
        the ID to a new array
        args:
            endpoints: the filtered list of game endpoints
        """

        for e in self.filtred_endpoints:
            arr = e.split('/')
            self.game_ids.append(arr[-1])

        return True

    def build_download_links(self):
        """Make download links for each game ID
        args:
            game_ids: The list of ids stripped from each endpoint
        """

        for id in self.game_ids:
            download_url = f"{self.server}roms/get-download.php?gid={id}&test=true"
            self.download_endpoints.append(download_url)
        return True


if __name__ == "__main__":
    scrape = ScrapeEmuparadise(
        url='https://www.emuparadise.me/Sony_Playstation_ISOs/List-All-Titles/2')
    scrape.main()
    for e in scrape.download_endpoints:
        print(e)
