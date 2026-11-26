# This code is now for finding the links
import requests, lxml, re, time, os, random
from bs4 import BeautifulSoup

from bs4 import XMLParsedAsHTMLWarning
import warnings

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


class WaybackArchive:
    def __init__(self):
        self.start_time = time.time()
        self.found_links = []
        self.find()
        self.update_text()

    # This method checks if it should start recording the last link
    def late_checker(self) -> bool:
        current_time = time.time() - self.start_time
        cutoff = (3 * 3600) + (55 * 60)
        return current_time - cutoff >= 0

    # This will find all the valid links to be archived on the wayback machine
    def find(self):
        soup = BeautifulSoup(requests.get('https://peisctehran.com').text, 'lxml')
        soup = str(soup)
        links = re.findall(r'"(.*?)"', soup)
        links = [link for link in links if link.startswith('https://peisctehran') and 'css' not in link and 'js' not in link]
        self.found_links.append('https://peisctehran.com/')
        self.found_links.append("https://peisctehran.com")
        count=0
        while links:
            print(len(links))
            if links[0] not in self.found_links:
                if 'wp-content' in links[0]:
                    # These are photos,pdfs that have no links
                    self.found_links.append(links[0])
                else:
                    # The link has not been explored-so it finds new links
                    soup = BeautifulSoup(requests.get(links[0]).text, 'lxml')
                    soup = str(soup)
                    new_links = re.findall(r'"(.*?)"', soup)
                    # filters out links that are css or js links
                    new_links = [link for link in new_links if link.startswith('https://peisctehran') and 'css' not in link and 'js' not in link]
                    for new_link in new_links:
                        if new_link not in self.found_links:
                            if new_link not in links:
                                print(new_link)
                                links.append(new_link)
                    self.found_links.append(links[0])
                    count += 1
                    print(f"Links accessed: {count}")
                    time.sleep(61)
            links.pop(0)

        random.shuffle(self.found_links)
        print("done finding links")

    # This method will update the text file 
    def update_text(self):
      def update_text(self):
          for link in self.found_links:
              with open("links.txt", "w") as file:
                  file.write(link + "\n")
      


if __name__ == "__main__":
    wa = WaybackArchive()
