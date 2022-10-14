import json
from time import sleep
from urllib.parse import urljoin
from lxml import html
import requests
import logging


class Crawler:
    url = ""                # the url of the website to be checked
    links = dict()          # dic. with all sites and urls on those sites
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

    def persist(self, path):
        with open(path, 'w') as fp:
            json.dump(self.links, fp)
            
    def load_site(self, path):
        with open(path, 'r') as fp:
            self.links = json.load(fp)
            
    def run(self, root, limit, sleep_time=0):
        self.url = root
        unchecked = [root]

        while unchecked and len(self.links) < limit:
            root = unchecked.pop()
            if root in self.links or self.url.rsplit('/')[2] not in root:
                continue
            if "https" not in root:
                continue

            clean = False
            for element in self.exclude:
                if element in root:
                    clean = False
                    break
                else:
                    clean = True
            if not clean:
                continue

            self.logger.info(f"{len(self.links)} {root}")
            try:
                site = requests.get(root)
                tree = html.fromstring(site.content)
                links = tree.xpath('//a/@href')
            except:
                continue

            nlinks = []
            for link in links:
                if link not in nlinks:
                    if link.startswith("http"):
                        nlinks.append(link)
                    else:
                        nlinks.append(urljoin(site.url, link))

            unchecked += nlinks
            self.links[root] = nlinks
            sleep(sleep_time)

    def getNodesEdges(self):
        nodes = []
        edges = []
        for key, value in self.links.items():
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
