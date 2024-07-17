import time
from datetime import datetime
from typing import List, Dict
from deepdiff import DeepDiff

class Watcher:
    # there should be a type hint for site_store and site_reader, referencing interfaces, which these implement, for better auto complete and DX
    def __init__(self, site_store, site_reader, sites_source_path, keywords_source_path) -> None:
        self.site_store = site_store
        self.site_reader = site_reader
        self.keywords_source_path = keywords_source_path
        self.sites_source_path = sites_source_path

    def read_txt_file(self, path):
        with open(path) as f:
            return f.read().splitlines()

    def watch(self, crawler, sleep=-1):
        """start the watcher with the given interval

        :param arg: seconds between runs, -1 for single run
        :type arg: int
        :return: None
        :rtype: None	
        """
        while True:
            keywords = self.read_txt_file(self.keywords_source_path)
            sites = self.read_txt_file(self.sites_source_path)

            
            for site in sites:
                crawler.run(site)
                self.site_store.persist(f"{self.remove_protocol(site)}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json", crawler.get_nodes())
                # do NOT overload the target
                time.sleep(1)

            contents = [self.get_new_content(site) for site in sites]
            # TODO: improve handleing of None
            contents = [x for x in contents if x is not None and x is not {}]
            matches = []
            for content in contents:
                for url, c in content.items():
                    matches.append(self.search_sites(url, c, keywords))
            print(matches)
            
            if sleep == -1:
                return matches
            time.sleep(sleep)

    @staticmethod
    def remove_protocol(site):
        # every protocol should have // 
        if "//" not in site:
            return site
        return site.split('/')[2]

    def get_new_content(self, url) -> Dict[str, str]:
        """ get all past iterations of a site by the fully qualified domain name """
        list_of_files = self.site_store.get_site_history(f"{self.remove_protocol(url)}/")

        if len(list_of_files) >= 2:
            prev_version = self.site_store.get_site_links(f"{self.remove_protocol(url)}/{list_of_files[-2]}")
        else:
            prev_version = {url: []}
        current_version = self.site_store.get_site_links(f"{self.remove_protocol(url)}/{list_of_files[-1]}")
        news = DeepDiff(prev_version, current_version, ignore_order=True)

        if news:
            sites_contents = self.site_reader.get_sites_content_static(self.get_added_urls(news))
            return sites_contents
        return {}

    @staticmethod
    def get_added_urls( news):
        return [z.split("'")[1] for z in list(news["iterable_item_added"])]

    @staticmethod
    def search_sites(url, content, keywords: List[str]):
        if content is None:
            return []
        results = []
        for keyword in keywords:
            if keyword in content:
                results.append((url, keyword))
        return results
