from selenium import webdriver
from PIL import Image
from bs4 import BeautifulSoup
import io
import requests
import hashlib
import time, os
import re

from selenium.webdriver.chrome.options import Options
from pathlib import Path

class ImageScraper:
    def __init__(self, search_list:list, target_path:str="./images",
            number_images:int=5, urls_only:bool=False):
        self.search_list = search_list
        self.target_path = target_path
        self.number_images = number_images
        self.urls_only = urls_only
        
        self.driver_path = "./chromedriver"
        self.search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

        self.load_block_list()
        self.search_and_download()

    # Experimentation found a number of sites that produce low-quality images,
    # make the web driver hang, or have restrictions.
    # TODO: add functionality somewhere to more easily add sites to that list.
    def load_block_list(self):
        self.blocked_sites = []
        try:
            with open('blocked.csv', 'r') as filename:
                sites = filename.readlines()
                for site in sites:
                    idx = site[:-1]
                    self.blocked_sites.append(idx)
        # TODO: dialog box here
        # TODO: options for loading other block lists
        except:
            print("Could not open the block list stored at blocked.csv")
            print("Is the file missing or in another directory")
            print("Proceeding with empty block list.")

    def get_image_urls(self, query:str, max_links:str, wd:webdriver, spacer:int=5, log:bool=False):
        def scroll_to_bottom(wd):
            wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(spacer)

        start_time = time.asctime()
        stop_time = str()

        wd.get(self.search_url.format(q=query))

        image_urls = set()
        image_count = 0
        results_start = 0

        while image_count < max_links:
            scroll_to_bottom(wd)

            thumbnails = wd.find_elements_by_css_selector("img.rg_i")
            results_count = len(thumbnails)
            print(f"Getting links from {results_start}:{results_count}")

            for img in thumbnails[results_start:results_count]:
                try:
                    img.click()
                    time.sleep(spacer)
                except Exception:
                    continue

                images = wd.find_elements_by_css_selector("img.n3VNCb")
                print(len(images))
                for image in images:
                    source = image.get_attribute("src")

                    if not source[:10] == "data:image":
                        image_urls.add(image.get_attribute("src"))

                self.unblocked_urls = set()
                ueg = image_urls

                for block in self.blocked_sites:
                    c = re.compile("\w*\.+" + block)
                    ueg = [i for i in ueg if not c.search(i)]

                self.unblocked_urls = set(ueg)
                image_count = len(self.unblocked_urls)

                if image_count >= max_links:
                    print(f"Found {image_count} links.")
                    break

            else:
                print(f"Found {image_count} links. Still searching.")
                time.sleep(20)

                try:
                    load_more = wd.find_element_by_css_selector(".sGx53d")
                    if load_more:
                        ed.execute_script("document.querySelector('.sGx53d').click();")
                except Exception as e:
                    print("Unable to load more images. Please try again later.")

            results_start = len(thumbnails)
        return self.unblocked_urls

    def search_and_download(self):
        for search_term in self.search_list:
            search_term_parse = '_'.join(search_term.lower().split(' '))
            target_folder = os.path.join(self.target_path, '_'.join(search_term.lower().split(' ')))

            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            
            with webdriver.Chrome(executable_path=self.driver_path) as wd:
                res = self.get_image_urls(search_term, self.number_images,
                        wd, spacer=1.0)
            

            with open(target_folder + "/" + search_term_parse + ".csv", "w") as urls_file:
                for r in res:
                    urls_file.write(r + "\n")

            if self.urls_only == False:
                for elem in res:
                    self.persist_image(target_folder, elem)

    def persist_image(self, folder_path:str, url:str):
        try:
            image_content = requests.get(url).content
        except Exception as e:
            print(f"Could not download {url} - {e}")

        try:
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert("RGB")
            file_path = os.path.join(folder_path, hashlib.sha1(image_content).hexdigest()[:10] + ".jpg")

            with open(file_path, "wb") as f:
                image.save(f, "JPEG", quality=85)
            print(f"Success: saved {url} as {file_path}")
        except Exception as e:
            print("Could not save {url} - {e}")

"""
search_terms = ["one", "two"]
imgs = ImageScraper(search_terms)
"""
