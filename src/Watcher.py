import time
from datetime import datetime
from typing import List, Dict, Optional

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
            contents = [x for x in contents if x is not None]
            matches = []
            for url, content in contents.items():
                matches.append(self.search_sites(url, content, keywords))
            print(matches)
            time.sleep(sleep)

    @staticmethod
    def remove_protocol(site):
        return site.split('/')[2]

    def get_new_content(self, url) -> Optional[List[str]]:
        """ get all past iterations of a site by the fully qualified domain name """
        list_of_files = self.site_store.get_site_history(f"./cache/{self.remove_protocol(url)}/")
        if not len(list_of_files) >= 2:
            return None
        prev_version = self.site_store.get_site_links(f"./cache/{self.remove_protocol(url)}/{list_of_files[-2]}")
        current_version = self.site_store.get_site_links(f"./cache/{self.remove_protocol(url)}/{list_of_files[-2]}")
        news = dict(set(prev_version.items()) ^ set(current_version.items()))
        sites_contents = self.site_reader.get_sites_content_static(sum(news.items()))

        return sites_contents

    def search_sites(self, url, content, keywords: List[str]):
        results = []
        for keyword in keywords:
            if keyword in content.values():
                results.append((url, keyword))
        return results
