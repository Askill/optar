import time
from datetime import datetime
from typing import List, Dict, Optional
from deepdiff import DeepDiff

from src.Crawler import Crawler
from src.SiteReader import SiteReader
from src.SiteStore import SiteStore


class Watcher:
    def __init__(self, sites_source_path, keywords_source_path) -> None:
        self.site_store = SiteStore()
        self.site_reader = SiteReader()
        self.keywords_source_path = keywords_source_path
        self.sites_source_path = sites_source_path

    def read_txt_file(self, path):
        with open(path) as f:
            return f.read().splitlines()

    def watch(self, sleep):
        while True:
            keywords = self.read_txt_file(self.keywords_source_path)
            sites = self.read_txt_file(self.sites_source_path)

            crawler = Crawler()
            crawled_sites = []
            for site in sites:
                crawler.run(site, 10)
                crawled_sites += crawler.get_nodes()
                crawler.persist(f"./cache/{self.remove_protocol(site)}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json")

            contents = [self.get_new_content(site) for site in crawled_sites]
            contents = [x for x in contents if x is not None and x is not {}]
            matches = []
            for content in contents:
                for url, c in content.items():
                    matches.append(self.search_sites(url, c, keywords))
            print(matches)
            time.sleep(sleep)

    @staticmethod
    def remove_protocol(site):
        return site.split('/')[2]

    def get_new_content(self, url) -> Dict[str, str]:
        """ get all past iterations of a site by the fully qualified domain name """
        list_of_files = self.site_store.get_site_history(f"./cache/{self.remove_protocol(url)}/")

        if len(list_of_files) >= 2:
            prev_version = self.site_store.get_site_links(f"./cache/{self.remove_protocol(url)}/{list_of_files[-2]}")
            current_version = self.site_store.get_site_links(f"./cache/{self.remove_protocol(url)}/{list_of_files[-1]}")
            news = DeepDiff(prev_version, current_version, ignore_order=True)
        else:
            news = self.site_store.get_site_links(f"./cache/{self.remove_protocol(url)}/{list_of_files[-1]}")

        sites_contents = self.site_reader.get_sites_content_static(list(news.keys()))

        return sites_contents

    @staticmethod
    def search_sites(url, content, keywords: List[str]):
        results = []
        for keyword in keywords:
            if keyword in content:
                results.append((url, keyword))
        return results
