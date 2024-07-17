import os
from optar.src.SiteReader import SiteReader
from optar.src.Watcher import Watcher 
from optar.tests.MockSiteStore import SiteStore

def test_search_sites__found():

    x = Watcher.search_sites("test.com", "dfjgbnsdigubsdofgliusdbgsdiugbTESTfjgnsdgosd\n\nsdfboiuasdgf!0980", ["TEST"])
    assert x == [("test.com", "TEST")]

def test_search_sites__not_found():

    x = Watcher.search_sites("test.com", "dfjgbnsdigubsdofgliusdbgsdiugbfjgnsdgosd\n\nsdfboiuasdgf!0980", ["TEST", "testing"])
    assert x == []

def test_remove_protocol__https():
    res = Watcher.remove_protocol("https://www.google.com")
    assert res == "www.google.com"

def test_remove_protocol__http():
    res = Watcher.remove_protocol("http://www.google.com")
    assert res == "www.google.com"

def test_remove_protocol__none():
    res = Watcher.remove_protocol("www.google.com")
    assert res == "www.google.com"

def test_compare_sites():
    class MockCrawler:
        _links = {}
        def run(self, url):
            self._links[url] = [url]
        def get_nodes(self):
            return self._links
    assert os.path.isdir("./cache/www.patricematz.de")
    assert len(SiteStore.get_site_history("www.patricematz.de")) >= 2
    # the links given in this sites.txt should be to either local files, or a local mock server
    # this is not implemented, as it would be trivial but time consuming
    watcher = Watcher(SiteStore(), SiteReader(), "./sites.txt", "keywords.txt")
    assert [] == watcher.watch(MockCrawler())

