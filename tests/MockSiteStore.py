import json
import os
from pathlib import Path
from typing import List, Optional


class SiteStore:
    def __init__(self):
        pass

    @staticmethod
    def get_site_history(in_path) -> Optional[list[str]]:
        cache_path = "./cache/" + in_path
        if not os.path.isdir(cache_path):
            return []
        return sorted(os.listdir(cache_path))

    @staticmethod
    def get_site_links(in_path):
        cache_path = "./cache/" + in_path
        with open(cache_path, 'r') as fp:
            return json.load(fp)
        
    @staticmethod
    def persist(self, data):
        return