# Emuparadise Web Scraper & Rom Download

> Note: Nintendo targeted Emuparadise, forcing them to disable all download links. I am not suggesting that you use this repo to download games; however, this repo does give you the ability to do so.

This repo will find a full list of games from a given page from [https://www.emuparadise.me/](https://www.emuparadise.me/). After the list of games is scraped, they are stored as a list of dictionaries.

> Example dictionary:
```python
{
    system: 'Playstation',
    name: 'Crash',
    id: '12345',
    download_endpoint: 'www.gamelink.com/donwload/<id>'
}
```

## How to use

Feed the script a link on line 98. The link below lists all available PS1 games.

> ['https://www.emuparadise.me/Sony_Playstation_ISOs/List-All-Titles/2']('https://www.emuparadise.me/Sony_Playstation_ISOs/List-All-Titles/2')

This will print out the games meta to the screen.

The ability to download the games is commented out by default on line 104.

## Things to know...
I've filtered this list to exclude:
1. most foreign games.
1. sports games
1. demos
1. Much more. See the **self.trash_reg** for the list of things being filtered.
