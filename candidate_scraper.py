from selenium import webdriver
from PIL import Image
from bs4 import BeautifulSoup
import io
import requests
import hashlib
import time, os
import argparse
import re

from selenium.webdriver.chrome.options import Options
from pathlib import Path

class NeighborNodeFinder:
    def __init__(self, query:str, wd:webdriver, max_layers:int=2, max_nodes:int=5):
        self.search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
        self.query = query
        self.wd = wd
        self.max_layers = max_layers
        self.max_nodes = max_nodes

        self.get_neighbors()

    def get_neighboring_nodes(self, nodes):
        node_set = set()
        for node in nodes:
            if len(node_set) < self.max_nodes:
                node_set.add(self.query + " " + node.text)
            else:
                break
        return node_set

    def get_neighbors(self):
        self.wd.get(self.search_url.format(q=self.query))
        layer = 1
        node_tag = "span.hIOe2"

        node_candidates = self.wd.find_elements_by_css_selector(node_tag)
        nodes = self.get_neighboring_nodes(node_candidates)

        next_layer = set()
        while layer <= self.max_layers:
            [next_layer.add(i) for i in nodes]

            for node in nodes:
                self.wd.get(self.search_url.format(q=node))
                new_neighbors = self.wd.find_elements_by_css_selector(node_tag)
                new_nodes = self.get_neighboring_nodes(new_neighbors)

                [next_layer.add(node + " " + i) for i in new_nodes]

                next_layer = set([' '.join(set(node.split(' '))) for node in next_layer])
                print(next_layer)

            layer += 1
            nodes = next_layer.copy()

        next_layer.add(self.query)

        self.final_node_list = list(next_layer)

"""
wd = webdriver.Chrome(executable_path="./chromedriver")
ueg = NeighborNodeFinder("ducks", wd, max_nodes=5, max_layers=1)
nodes = ueg.final_node_list
wd.close()
print(nodes)
"""
