import requests
import pickle
from bs4 import BeautifulSoup

class EventScraper:
    """
    A class used to scrape event links from the UFC website.

    Attributes:
        base_url (str): The base URL of the UFC website.
        dynamic_query_text (str): The dynamic query text used to construct the URL for pagination.
        index (int): The index used for pagination.
        urls (list): A list to store the scraped event URLs.

    Methods:
        scrape_event_links(): Scrapes event links from the UFC website that have odds data and saves
        them to a pickle file.
    """

    def __init__(self):
        self.base_url = "https://www.ufc.com"
        self.dynamic_query_text = "/events?page="
        self.index = 0
        self.urls = []

    def scrape_event_links(self):
        """
        Scrapes event links from the UFC website and saves them to a pickle file.

        The method iterates through the event pages on the UFC website and extracts the event links.
        It stops when it reaches the event link "/event/ufc-fight-night-august-01-2020#984".
        The scraped event links are then stored in a pickle file named "urls.pickle".
        """
        while "/event/ufc-fight-night-august-01-2020#984" not in self.urls:
            if self.index == 0:
                url = "https://www.ufc.com/events#events-list-past"
            else:
                url = self.base_url + self.dynamic_query_text + str(self.index)

            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            anchor_tags = soup.find_all("a", href=True)
            self.urls += [tag["href"] for tag in anchor_tags if tag["href"].startswith("/event/") and "#" in tag["href"]]
            self.index += 1

        self.urls = [self.base_url + url for url in self.urls]

        urls_end_index = self.urls.index("https://www.ufc.com/event/ufc-fight-night-august-01-2020#984") + 1
        self.urls = self.urls[:urls_end_index]

        with open("urls.pickle", "wb") as file:
            pickle.dump(self.urls, file)
