import pickle
import requests
from bs4 import BeautifulSoup
import datetime
import csv

class EventFightsMetaDataScraper:
    def __init__(self, pickle_file):
        self.pickle_file = pickle_file
        self.urls = self.load_urls()

    def load_urls(self):
        with open(self.pickle_file, 'rb') as file:
            urls = pickle.load(file)
        return urls

    def parse_event_page(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        fight_date = []
        red_fighters = []
        blue_fighters = []
        title_bouts = []
        fight_weights = []
        red_odds = []
        blue_odds = []

        # Scrape BST datetimestamp from page and extract date
        datetimestamp = int(soup.find('div', class_='hero-fixed-bar__description').contents[1].attrs['data-timestamp'])
        fight_date.append(datetime.datetime.fromtimestamp(datetimestamp).strftime('%Y-%m-%d'))

        # Red and Blue fighters' names
        red_fighters_result_set = soup.find_all('div', class_='c-listing-fight__corner-name--red')
        blue_fighters_result_set = soup.find_all('div', class_='c-listing-fight__corner-name--blue')
        red_fighters = self.extract_fighter_names(red_fighters_result_set)
        blue_fighters = self.extract_fighter_names(blue_fighters_result_set)

        # Title bouts


        # Fight weights


        # Red and Blue odds


        return fight_date, red_fighters, blue_fighters, title_bouts, fight_weights, red_odds, blue_odds

        def extract_fighter_names(self, fighters_result_set):
            fighter_names = []

            for fighter in fighters_result_set:
                # Check for given name and family name spans first
                given_name_span = fighter.find('span', class_='c-listing-fight__corner-given-name')
                family_name_span = fighter.find('span', class_='c-listing-fight__corner-family-name')
                
                if given_name_span and family_name_span:
                    given_name = given_name_span.text.strip()
                    family_name = family_name_span.text.strip()
                    fighter_names.append(f'{given_name} {family_name}')
                else:
                    # Fallback to checking the anchor tag's text
                    anchor_tag = fighter.find('a')
                    if anchor_tag and anchor_tag.text.strip():
                        fighter_names.append(anchor_tag.text.strip())
                    else:
                        fighter_names.append('Unknown Unknown')
                        
            return fighter_names

    def scrape_all_events(self):
        fight_dates = []
        all_red_fighters = []
        all_blue_fighters = []
        all_title_bouts = []
        all_fight_weights = []
        all_red_odds = []
        all_blue_odds = []

        for url in self.urls:
            fight_dates, red_fighters, blue_fighters, title_bouts, fight_weights, red_odds, blue_odds = self.parse_event_page(url)
            fight_dates.extend(fight_dates)
            all_red_fighters.extend(red_fighters)
            all_blue_fighters.extend(blue_fighters)
            all_title_bouts.extend(title_bouts)
            all_fight_weights.extend(fight_weights)
            all_red_odds.extend(red_odds)
            all_blue_odds.extend(blue_odds)

        self.write_to_csv(fight_dates, all_red_fighters, all_blue_fighters, all_title_bouts, all_fight_weights, all_red_odds, all_blue_odds)

    def write_to_csv(self, fight_dates, red_fighters, blue_fighters, title_bouts, fight_weights, red_odds, blue_odds):
        with open('ufc_fights_meta_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Fight Date', 'Red Fighter', 'Blue Fighter', 'Title Bout', 'Fight Weight', 'Red Odds', 'Blue Odds'])
            for row in zip(fight_dates, red_fighters, blue_fighters, title_bouts, fight_weights, red_odds, blue_odds):
                writer.writerow(row)

# Example usage:
# scraper = EventFightsMetaDataScraper('event_urls.pickle')
# scraper.scrape_all_events()