from optar.src.Crawler import Crawler
from optar.src.SiteReader import SiteReader
from optar.src.SiteStoreS3 import SiteStoreS3
from src.Watcher import Watcher

if __name__ == "__main__":
    Watcher(SiteStoreS3("optar-dev-cache"), SiteReader(), "./sites.txt", "./keywords.txt").watch(crawler=Crawler(1))