from bs4 import BeautifulSoup
from qbittorrent import Client

import requests


class DownloadsManager():
    def search_torrents(self, name: str) -> dict:
        url = f"https://mejortorrent.wtf/busqueda?q={name}"

        response = requests.request("GET", url, headers={}, data={})

        soup = BeautifulSoup(response.text, 'html.parser')

        results = soup.findAll(lambda tag: tag.name == 'a' and tag.findParent('div', attrs={'class': 'flex flex-row mb-2'}))

        quality_results = {}

        for result in results:
            name = result.p.text
            quality = result.strong.text
            href = result.attrs.get('href')

            torrents = self.__get_items_torrent(href)

            if quality not in quality_results:
                quality_results[quality] = []

            quality_results[quality].append({
                "name": name,
                "torrents": torrents
            })
        return quality_results

    def __get_items_torrent(self, href):
        response = requests.request("GET", href, headers={}, data={})
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.select("a[href*='https://server-local']")
        return [dict(
            name=result.attrs.get('href').split('/')[-1],
            href=result.attrs.get('href')
        ) if results else [] for result in results]

    def download_torrent(self, href: str) -> None:
        qb = Client('http://192.168.1.150:9091/')
        qb.login('admin', 'adminadmin')

        return qb.download_from_link(href)
