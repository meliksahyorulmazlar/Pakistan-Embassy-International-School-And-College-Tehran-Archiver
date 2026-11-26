import requests
import re
from bs4 import BeautifulSoup

urls = [
    "https://peisctehran.com/",
    "https://peisctehran.com/index.php/courses/",
    "https://peisctehran.com/index.php/news-events/",
    "https://peisctehran.com/index.php/gallery/",
    "https://peisctehran.com/index.php/about-our-school/",
]

for url in urls:
    print("\n" + "=" * 70)
    print(f"Requesting: {url}")

    try:
        response = requests.get(url, timeout=30)

        print(f"Status code: {response.status_code}")
        print(f"Final URL: {response.url}")
        print(f"Response size: {len(response.content)} bytes")
        print(f"Content type: {response.headers.get('Content-Type')}")

        soup = BeautifulSoup(response.text, "lxml")

        print(f"Page title: {soup.title}")

        links = re.findall(r'"(.*?)"', str(soup))

        links = [
            link for link in links
            if link.startswith("https://peisctehran")
            and "css" not in link
            and "js" not in link
        ]

        print(f"Links found: {len(set(links))}")
        print(f"Response preview: {response.text[:300]}")

    except requests.exceptions.RequestException as error:
        print(f"Request failed: {error}")
