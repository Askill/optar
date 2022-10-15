import json
import os
from typing import List, Optional


class SiteStore:
    def __init__(self):
        pass

    @staticmethod
    def get_site_history(cache_path) -> Optional[list[str]]:
        if not os.path.isdir(cache_path):
            return None
        return sorted(os.listdir(cache_path))

    @staticmethod
    def get_site_links(path):
        with open(path, 'r') as fp:
            return json.load(fp)
