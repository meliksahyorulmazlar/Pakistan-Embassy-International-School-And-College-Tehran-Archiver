import requests, lxml, re, time, os, random
from bs4 import BeautifulSoup

from bs4 import XMLParsedAsHTMLWarning
import warnings

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


class WaybackArchive:
    def __init__(self):
        self.start_time = time.time()
        self.found_links = []
        self.read()
        self.save_all()

    # This method checks if it should start recording the last link
    def late_checker(self) -> bool:
        current_time = time.time() - self.start_time
        cutoff = (3 * 3600) + (55 * 60)
        return current_time - cutoff >= 0

    # This will read all the valid links to be archived on the wayback machine
    def read(self):
        with open("links.txt", "r") as f:
            self.found_links = f.read().splitlines()

        random.shuffle(self.found_links)
        print(f"Loaded {len(self.found_links)} links")

    # This method will save all the links on the wayback machine
    def save_all(self) -> None:
        for link in self.found_links:
            print(f'saving {link}')
            self.save(link)
            # the code stops working if it has passed 3 hours and 55 minutes
            if self.late_checker():
                break
            time.sleep(2)

    # This method will save a given website link on the wayback machine
    def save(self, site: str) -> None:
        main = 'https://web.archive.org/save/'
        try:
            requests.get("https://web.archive.org/save/" + site)
        except requests.exceptions.ConnectionError:
            print('connection error')


if __name__ == "__main__":
    wa = WaybackArchive()
