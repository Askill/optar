import json
from time import sleep
from urllib.parse import urljoin
from lxml import html
import requests
import logging
from pathlib import Path

class Crawler:
    url = ""                # the url of the website to be checked
    _links = dict()          # dic. with all sites and urls on those sites
    header_values = {
        'Connection:': 'Keep-alive',
        'name': 'Michael Foord',
                'location': 'Northampton',
                'language': 'English',
                'User-Agent': 'Mozilla 4/0'}

    exclude = [
    ]

    def __init__(self,  logger=None, exclude=None):
        if exclude:
            self.exclude += exclude
        if logger:
            self.logger = logger
        else:
            self.logger = logging.Logger(
                name="star_crawler", level=logging.INFO)

    def get_nodes(self):
        return self._links

    def persist(self, path):
        Path("/".join(path.split("/")[:-1])).mkdir(parents=True, exist_ok=True)
        with open(path, 'w+') as fp:
            json.dump(self._links, fp)
            
    def load_site(self, path):
        with open(path, 'r') as fp:
            self._links = json.load(fp)
            
    def run(self, root, limit, sleep_time=0):
        self.url = root
        unchecked = [root]

        while unchecked and len(self._links) < limit:
            root = unchecked.pop()
            if root in self._links or self.url.rsplit('/')[2] not in root:
                continue
            if "https" not in root:
                continue

            clean = True
            for element in self.exclude:
                if element in root:
                    clean = False
                    break
                else:
                    clean = True
            if not clean:
                continue

            self.logger.info(f"{len(self._links)} {root}")
            try:
                site = requests.get(root)
                tree = html.fromstring(site.content)
                _links = tree.xpath('//a/@href')
            except:
                continue

            n_links = []
            for link in _links:
                if link not in n_links:
                    if link.startswith("http"):
                        n_links.append(link)
                    else:
                        n_links.append(urljoin(site.url, link))

            unchecked += n_links
            self._links[root] = n_links
            sleep(sleep_time)

    def getNodesEdges(self):
        nodes = []
        edges = []
        for key, value in self._links.items():
            nodes.append(key)
            for edge in value:
                edges.append([key, edge])

        return nodes, edges

    def makeGraph(self, g):
        nodes, edges = self.getNodesEdges()
        for node in nodes:
            g.add_node(node)
        for f, t in edges:
            g.add_edge(f, t)
