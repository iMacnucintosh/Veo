from bs4 import BeautifulSoup
from qbittorrent import Client
from tpblite import TPB, CATEGORIES, ORDERS
import requests


class DownloadsManager():
    def __init__(self):
        self.tpb = TPB()

    def search_torrents(self, name: str) -> dict:
        quality_results = {}
        try:
            url = f"https://mejortorrent.wtf/busqueda?q={name}"

            response = requests.request("GET", url, headers={"User-Agent": "Defined"}, data={})

            soup = BeautifulSoup(response.text, 'html.parser')

            results = soup.findAll(lambda tag: tag.name == 'a' and tag.findParent('div', attrs={'class': 'flex flex-row mb-2'}))

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

        except Exception as e:
            raise e
        finally:
            return quality_results

    def __get_items_torrent(self, href):
        response = requests.request("GET", href, headers={"User-Agent": "Defined"}, data={})
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.select("a[href*='https://server-local']")
        return [dict(
            name=result.attrs.get('href').split('/')[-1],
            href=result.attrs.get('href')
        ) if results else [] for result in results]

    def search_torrents_tpb(self, name: str) -> dict:
        torrents = self.tpb.search(name)

        # Get the most seeded torrent based on a filter
        best_torrent = torrents.getBestTorrent(min_seeds=30)

        torrents_find = {"Mejor": [best_torrent], "Otros": torrents.list}

        return torrents_find

    def download_torrent(self, href: str, hash: str) -> None:
        qb = Client('http://192.168.1.150:9091/')
        qb.login('admin', 'adminadmin')

        return qb.download_from_link(href)
