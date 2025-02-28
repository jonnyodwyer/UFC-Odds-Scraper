import unittest
from unittest.mock import patch
from src.scrape_event_fights_meta_data import EventFightsMetaDataScraper

class TestEventFightsMetaDataScraper(unittest.TestCase):
    def test_parse_event_page(self):
        scraper = EventFightsMetaDataScraper('dummy.pickle')
        fight_date, red_fighters, blue_fighters, title_bouts, fight_weights, red_odds, blue_odds = scraper.parse_event_page('https://www.ufc.com/event/ufc-281#1114')

        self.assertEqual(fight_date, ['2022-11-13'])
        self.assertEqual(red_fighters, ['Israel Adesanya', 'Carla Esparza', 'Dustin Poirier', 'Frankie Edgar', 'Dan Hooker',
                                        'Brad Riddell', 'Dominick Reyes', 'Erin Blanchfield', 'Andre Petroski', 'Matt Frevola',
                                        'Karolina Kowalkiewicz', 'Michael Trizano', 'Julio Arce', 'Carlos Ulberg'])
        self.assertEqual(blue_fighters, ['Alex Pereira', 'Zhang Weili', 'Michael Chandler', 'Chris Gutierrez', 'Claudio Puelles',
                                         'Renato Moicano', 'Ryan Spann', 'Molly McCann', 'Wellington Turman', 'Ottman Azaitar',
                                         'Silvana Gomez Juarez', 'Seungwoo Choi', 'Montel Jackson', 'Nicolae Negumereanu'])
        self.assertEqual(title_bouts, [True, True, False, False, False, False, False, False, False, False, False, False, False, False])
        self.assertEqual(fight_weights, ['Middleweight', "Women's Strawweight", 'Lightweight', 'Bantamweight', 'Lightweight', 'Lightweight',
                                       'Light Heavyweight', "Women's Flyweight", 'Middleweight', 'Lightweight', "Women's Strawweight",
                                       'Featherweight', 'Bantamweight', 'Light Heavyweight'])
        self.assertEqual(red_odds, ['-165', '-', '-175', '+175', '-155', '+105', '-215', '-380', '-205', '-145', '-115', '+135', '-', '-125'])
        self.assertEqual(blue_odds, ['+140', '-', '+150', '-210', '+135', '-125', '+175', '+290', '+175', '+125', '-115', '-160', '-', '+105'])                     

if __name__ == '__main__':
    unittest.main()