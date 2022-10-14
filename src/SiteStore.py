import os
from typing import List


class SiteStore:
    def __init__(self):
        pass

    @staticmethod
    def get_site_history(fqdn) -> List[str]:
        cache_path = f"./cached/{fqdn}"
        if not os.path.isdir(cache_path):
               return [""]
        return sorted(os.listdir(cache_path))

