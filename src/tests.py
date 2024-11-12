import unittest
from unittest.mock import patch, Mock
from scrape_event_links import EventScraper
from scrape_event_fights_meta_data import EventFightsMetaDataScraper

class TestEventScraper(unittest.TestCase):
    def test_scrape_event_links(self):
        scraper = EventScraper()
        scraper.scrape_event_links()

        # Assert that the URLs list is not empty
        self.assertTrue(scraper.urls)

        # Assert that the scraped URLs are valid
        for url in scraper.urls:
            self.assertTrue(url.startswith("https://www.ufc.com/event/"))
            self.assertTrue("#" in url)

if __name__ == "__main__":
    unittest.main()
