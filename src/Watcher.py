
from typing import List, Dict

from src.SiteReader import SiteReader
from src.SiteStore import SiteStore


class Watcher:
    def __init__(self) -> None:
        self.site_store = SiteStore()
        self.site_reader = SiteReader()
        self.keywords_source_path = ""
        self.sites_source_path = ""

    def read_txt_file(self, path):
        with open(path) as f:
            return f.read().splitlines()

    def watch(self):
        while True:
            keywords = self.read_txt_file(self.keywords_source_path)
            sites = self.read_txt_file(self.sites_source_path)

            contents = [self.get_new_content(site) for site in sites]
            keywords = [x for x in self.get_new_content(keyword) for keyword in keywords]
            matches = []
            for url, content in contents.items():
                matches.append(self.search_sites(url, content, keywords))
            print(matches)
        
    def get_new_content(self, fqdm) -> List[str]:
        """ get all past iterations of a site by the fully qualified domain name """
        list_of_files = self.site_store.get_site_history(fqdm)
        prev_version = list_of_files[-2]
        current_version = list_of_files[-1]
        news = dict(set(prev_version.items()) ^ set(current_version.items()))
        sites_contents = self.site_reader.get_sites_content_static(sum(news.items()))

        return sites_contents

    def search_sites(self, url, content, keywords: List[str]):
        results = []
        for keyword in keywords:
            if keyword in content.values():
                results.append((url, keyword))
        return results