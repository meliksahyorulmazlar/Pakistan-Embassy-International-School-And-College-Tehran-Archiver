import requests
import re
import time
import warnings
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


class WaybackArchive:
    def __init__(self):
        self.start_time = time.time()
        self.found_links = []
        self.request_count = 0
        self.failed_requests = []

        self.find()

    def fetch(self, url):
        self.request_count += 1

        print("\n" + "=" * 70)
        print(f"Request #{self.request_count}")
        print(f"URL: {url}")

        start = time.time()

        try:
            response = requests.get(url, timeout=30)

            print(f"HTTP status: {response.status_code}")
            print(f"Final URL: {response.url}")
            print(f"Response size: {len(response.content)} bytes")
            print(f"Response time: {time.time() - start:.2f}s")
            print(f"Content type: {response.headers.get('Content-Type')}")

            soup = BeautifulSoup(response.text, "lxml")

            print(f"Page title: {soup.title}")

            if response.status_code != 200:
                self.failed_requests.append(
                    (url, response.status_code)
                )
                print(f"WARNING: {response.text[:300]}")

            return str(soup)

        except requests.exceptions.RequestException as error:
            print(f"REQUEST FAILED: {error}")
            self.failed_requests.append((url, str(error)))
            return ""

    def extract_links(self, soup):
        links = re.findall(r'"(.*?)"', soup)

        return [
            link for link in links
            if link.startswith("https://peisctehran")
            and "css" not in link
            and "js" not in link
        ]

    def find(self):
        soup = self.fetch("https://peisctehran.com")
        links = self.extract_links(soup)

        self.found_links.append("https://peisctehran.com/")
        self.found_links.append("https://peisctehran.com")

        print(f"Initial queue size: {len(links)}")

        while links:
            current_link = links[0]

            print(f"\nPending links: {len(links)}")
            print(f"Total discovered: {len(self.found_links)}")

            if current_link not in self.found_links:

                if "wp-content" in current_link:
                    self.found_links.append(current_link)

                else:
                    soup = self.fetch(current_link)
                    new_links = self.extract_links(soup)

                    print(f"Extracted links: {len(new_links)}")
                    print(f"Unique extracted links: {len(set(new_links))}")

                    added = 0

                    for new_link in new_links:
                        if new_link not in self.found_links:
                            if new_link not in links:
                                links.append(new_link)
                                added += 1

                    print(f"New links added to queue: {added}")

                    self.found_links.append(current_link)

            links.pop(0)

        print("\n" + "=" * 70)
        print("CRAWLING SUMMARY")
        print("=" * 70)

        print(f"Total links discovered: {len(self.found_links)}")
        print(f"HTTP requests made: {self.request_count}")
        print(f"Failed requests: {len(self.failed_requests)}")
        print(f"Execution time: {time.time() - self.start_time:.2f}s")

        for url, error in self.failed_requests:
            print(f"FAILED: {url} | {error}")


if __name__ == "__main__":
    wa = WaybackArchive()
