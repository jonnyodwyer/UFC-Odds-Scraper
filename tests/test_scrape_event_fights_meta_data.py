import unittest
from unittest.mock import patch, Mock
from src.scrape_event_fights_meta_data import EventFightsMetaDataScraper

class TestEventFightsMetaDataScraper(unittest.TestCase):
    def test_parse_event_page(self):
        scraper = EventFightsMetaDataScraper('dummy.pickle')
        fight_date, red_fighters, blue_fighters, title_bouts, fight_weights, red_odds, blue_odds = scraper.parse_event_page('https://www.ufc.com/event/ufc-281#1114')

        self.assertEqual(fight_date, ['2022-11-13'])

if __name__ == '__main__':
    unittest.main()