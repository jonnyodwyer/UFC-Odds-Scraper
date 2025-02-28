import pickle
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd

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
        weights_and_title_bouts_result_set = soup.find_all('div', class_='c-listing-fight__class-text')
        # Title bouts are marked with the word "Title" in the text. There are two fighters in each bout, so only take odd numbered indices
        weights_and_title_bouts_result_set = [weight_and_title.text.strip() for weight_and_title in weights_and_title_bouts_result_set[1::2]]
        title_bouts = [True if 'Title' in weight_and_title else False for weight_and_title in weights_and_title_bouts_result_set]

        # Extract the fight weight strings from the text.
        fight_weights = self.extract_fight_weights(weights_and_title_bouts_result_set)

        # Red and Blue odds
        odds_result_set = soup.find_all('span', class_='c-listing-fight__odds-amount')
        red_odds = [odds.text.strip() for odds in odds_result_set[0::2]]
        blue_odds = [odds.text.strip() for odds in odds_result_set[1::2]]

        # Replicate fight date for each fight in the event
        fight_date = fight_date * len(red_fighters)

        # Make pandas data frame from the lists
        df = pd.DataFrame(list(zip(fight_date, red_fighters, blue_fighters, title_bouts, fight_weights, red_odds, blue_odds)),
                          columns =['Fight Date', 'Red Fighter', 'Blue Fighter', 'Title Bout', 'Fight Weight', 'Red Odds', 'Blue Odds'])
        
        # Only take complete rows from the data frame. Remove rows with odds = "-"
        df = df[(df['Red Odds'] != '-') | (df['Blue Odds'] != '-')]

        return df

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
        
    def extract_fight_weights(self, weights_and_title_bouts_result_set):
        fight_weights = []
        for weight_and_title in weights_and_title_bouts_result_set:
            words = weight_and_title.split()
            if not words:
                fight_weights.append('Unknown')
                continue

            if "Women's" in words:
                index = words.index("Women's")
                if index + 1 < len(words):
                    fight_weights.append(f"Women's {words[index + 1]}")
            elif "Light" in words:
                index = words.index("Light")
                if index + 1 < len(words) and words[index + 1] == "Heavyweight":
                    fight_weights.append("Light Heavyweight")
            else:
                # Take only the first word as the weight
                fight_weights.append(words[0])
        return fight_weights

    def scrape_all_events(self):
        all_events_data = pd.DataFrame()
        
        for url in self.urls:
            try:
                # Parse individual event page into a DataFrame
                event_df = self.parse_event_page(url)
                # Concatenate the event data into our overall DataFrame
                all_events_data = pd.concat([all_events_data, event_df], ignore_index=True)
            except Exception as e:
                print(f"Error scraping {url}: {str(e)}")
                continue

        # Save aggregated data with a timestamped filename
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"ufc_fights_data_{timestamp}.csv"
        all_events_data.to_csv(output_file, index=False)
        
        return all_events_data

# Example usage:
# scraper = EventFightsMetaDataScraper('urls.pickle')
# scraper.scrape_all_events()