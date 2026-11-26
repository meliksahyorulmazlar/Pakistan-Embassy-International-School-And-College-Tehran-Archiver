import requests, lxml, re, time, os, random
from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning
import warnings

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


class WaybackArchive:
    def __init__(self):
        self.start_time = time.time()
        self.found_links = []
        self.request_count = 0

        self.find()
        self.save_all()

    # Check the execution time
    def late_checker(self) -> bool:
        current_time = time.time() - self.start_time
        cutoff = (3 * 3600) + (55 * 60)
        return current_time >= cutoff

    # Retrieve and validate a website page
    def fetch(self, url):
        self.request_count += 1

        print(f"\nRequest #{self.request_count}")
        print(f"Fetching: {url}")

        response = requests.get(url, timeout=30)

        print(f"HTTP status: {response.status_code}")
        print(f"Response size: {len(response.content)} bytes")

        if response.status_code == 429:
            print("\nRATE LIMIT EXCEEDED")
            print("\nResponse headers:")

            for key, value in response.headers.items():
                print(f"{key}: {value}")

            print("\nRetry-After:",
                  response.headers.get("Retry-After"))

            print("\nResponse body:")
            print(response.text[:500])

            raise RuntimeError(
                "Crawling stopped due to server rate limit."
            )

        response.raise_for_status()

        return str(BeautifulSoup(response.text, 'lxml'))

    # Find all valid links
    def find(self):
        soup = self.fetch('https://peisctehran.com')

        links = re.findall(r'"(.*?)"', soup)

        links = [
            link for link in links
            if link.startswith('https://peisctehran')
            and 'css' not in link
            and 'js' not in link
        ]

        self.found_links.append('https://peisctehran.com/')
        self.found_links.append('https://peisctehran.com')

        while links:
            print(f"Pending links: {len(links)}")
            print(f"Discovered links: {len(self.found_links)}")

            if links[0] not in self.found_links:

                if 'wp-content' in links[0]:
                    self.found_links.append(links[0])

                else:
                    time.sleep(5)

                    soup = self.fetch(links[0])

                    new_links = re.findall(r'"(.*?)"', soup)

                    new_links = [
                        link for link in new_links
                        if link.startswith('https://peisctehran')
                        and 'css' not in link
                        and 'js' not in link
                    ]

                    for new_link in new_links:
                        if new_link not in self.found_links:
                            if new_link not in links:
                                print(new_link)
                                links.append(new_link)

                    self.found_links.append(links[0])

            links.pop(0)

        random.shuffle(self.found_links)

        print("\nDone finding links")
        print(f"Total links found: {len(self.found_links)}")
        print(f"Total discovery requests: {self.request_count}")

    # Save all discovered links
    def save_all(self) -> None:
        for link in self.found_links:
            if self.late_checker():
                break

            print(f'saving {link}')
            self.save(link)

            time.sleep(2)

    # Submit a link to the Wayback Machine
    def save(self, site: str) -> None:
        main = 'https://web.archive.org/save/'

        try:
            response = requests.get(main + site, timeout=60)

            print(f"Archive HTTP status: {response.status_code}")

            if response.status_code == 429:
                print("Wayback Machine rate limit exceeded.")
                print("Retry-After:",
                      response.headers.get("Retry-After"))

                raise RuntimeError(
                    "Archiving stopped due to rate limit."
                )

            response.raise_for_status()

        except requests.exceptions.RequestException as error:
            print(f"Archive request failed: {error}")


if __name__ == "__main__":
    wa = WaybackArchive()
