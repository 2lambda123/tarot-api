# For reference only. Not using anymore.
# A first effort at scraping with Python.
# Use at your own risk. :)

import json
import re
import requests
from bs4 import BeautifulSoup

base_url = 'http://www.sacred-texts.com/tarot/pkt/pkt'
majors_url = 'http://www.sacred-texts.com/tarot/pkt/pkt0303.htm'

cards = []
minorText = []
majorText = []

class Card:
    def __init__(self, value, value_int, name, name_short, meaning_up, meaning_rev):
        """Initialize the function with given values.
        Parameters:
            - value (str): Value to be stored in lowercase.
            - value_int (int): Integer value to be stored.
            - name (str): Name to be stored in title case.
            - name_short (str): Short name to be stored in lowercase.
            - meaning_up (str): Meaning of value in uppercase.
            - meaning_rev (str): Reverse meaning of value in uppercase.
        Returns:
            - None: No return value.
        Processing Logic:
            - Convert value to lowercase.
            - Convert name to title case.
            - Convert name_short to lowercase."""
        
        self.value = value.lower()
        self.value_int = value_int
        self.name = name.title()
        self.name_short = name_short.lower()
        self.meaning_up = meaning_up
        self.meaning_rev = meaning_rev

class Major(Card):
    def __init__(self, *args):
        """Initializes a Major object with a type attribute set to "major".
        Parameters:
            - args (list): A list of arguments that can be passed to the Major object.
        Returns:
            - None: This function does not return anything.
        Processing Logic:
            - Sets the type attribute to "major"."""
        
        super(Major, self).__init__(*args)
        self.type = "major"

    def to_JSON(self):
        """Function to convert an object to JSON format.
        Parameters:
            - self (object): The object to be converted to JSON.
        Returns:
            - dict: A dictionary containing the object's attributes in JSON format.
        Processing Logic:
            - Convert object attributes to JSON format.
            - Return a dictionary with the converted attributes.
            - The dictionary will have the following keys: 'name', 'name_short', 'value', 'value_int', 'meaning_up', 'meaning_rev', 'type'.
        Example:
            to_JSON(card)
            # where card is an object of class Card
            # returns {'name': 'The Fool', 'name_short': 'FOOL', 'value': '0', 'value_int': 0, 'meaning_up': 'New beginnings, optimism, trust in the universe', 'meaning_rev': 'Recklessness, taken advantage of, inconsideration', 'type': 'Major Arcana'}"""
        
        return {
            'name': self.name,
            'name_short': self.name_short,
            'value': self.value,
            'value_int': self.value_int,
            'meaning_up': self.meaning_up,
            'meaning_rev': self.meaning_rev,
            'type': self.type
        }

class Minor(Card):
    def __init__(self, suit, desc, *args):
        """Creates a Minor Arcana card with a specified suit and description.
        Parameters:
            - suit (str): The suit of the card.
            - desc (str): The description of the card.
            - *args (str): Optional additional arguments.
        Returns:
            - Minor: A Minor Arcana card object.
        Processing Logic:
            - Inherits from a parent class.
            - Sets the type and name of the card.
            - Sets the description and suit of the card."""
        
        super(Minor, self).__init__(*args)
        self.type = "minor"
        self.name = self.value.capitalize() + ' of ' + suit.capitalize()
        self.desc = desc
        self.suit = suit.lower()

    def to_JSON(self):
        """Converts a Tarot card object to a JSON format.
        Parameters:
            - self (TarotCard): The Tarot card object to be converted.
        Returns:
            - dict: A dictionary containing the Tarot card's attributes in JSON format.
        Processing Logic:
            - Converts Tarot card object to dictionary.
            - Each key represents an attribute.
            - Each value represents the attribute's value.
            - Used for storing and transferring Tarot card data."""
        
        return {
            'value': self.value,
            'value_int': self.value_int,
            'name': self.name,
            'name_short': self.name_short,
            'suit': self.suit,
            'meaning_up': self.meaning_up,
            'meaning_rev': self.meaning_rev,
            'type': self.type,
            'desc': self.desc
        }

def get_majors():
    """Function:
    def get_majors():
        Retrieves a list of majors from a specified URL and parses the HTML content to extract the value, name, and meaning of each major.
        Parameters:
            - None
        Returns:
            - list: A list of dictionaries containing the short name, full name, text, and value of each major.
        Processing Logic:
            - Retrieve the HTML content from the specified URL.
            - Parse the HTML content using BeautifulSoup.
            - Loop through each paragraph tag in the HTML content.
            - Use regular expressions to extract the value, name, and meaning of each major.
            - Create a Major object using the extracted information.
            - Add the major's information to a list of dictionaries.
            - Convert the Major object to JSON format and add it to a list of cards.
            - Print a message indicating that the major card has been added."""
    
    majs = requests.get(majors_url, timeout=60)
    soup = BeautifulSoup(majs.content, 'html.parser')
    for p in soup.find_all('p'):
        line = p.text
        m = re.match(r'([0-9]+|(ZERO))(\..+?(?=\.))', line)
        if m:
            value = m[1]
            value_int = 0 if value == 'ZERO' else int(value)
            name = m[3][2:]
            name_short = 'ar' + '{:02}'.format(value_int)
            meaning_up = line[len(m[0])+3:line.find("Reversed")]
            meaning_rev = line[line.find("Reversed")+len("Reversed"):]
            c = Major(value, value_int, name, name_short, meaning_up, meaning_rev)
            entry = {'name_short': name_short, 'name': name, 'text': line, 'value': value}
            majorText.append(entry)
            cards.append(c.to_JSON())
            print('Added major card', c.name)

def get_minors():
    """Returns:
        - None: This function does not return any value, it simply adds data to the global variables 'minorText' and 'cards'.
    Processing Logic:
        - Creates a list of tuples containing suit abbreviations and full names.
        - Creates a list of tuples containing minor arcana abbreviations, full names, and corresponding numerical values.
        - Iterates through each suit and value, creates a URL based on the abbreviations, and scrapes data from the webpage.
        - Uses the scraped data to create a dictionary and an instance of the Minor class, which is then added to the global variables.
        - Prints a message for each card added."""
    
    suits_tup = [["wa", "wands"], ["cu", "cups"], ["pe", "pentacles"], ["sw", "swords"]]
    mins_tup = [["pa", "page", 11], ["kn", "knight", 12], ["qu", "queen", 13], ["ki", "king", 14], ["ac", "ace", 1], ["02", "Two", 2], ["03", "Three", 3], ["04", "Four", 4], ["05", "Five", 5], ["06", "Six", 6], ["07", "Seven", 7], ["08", "Eight", 8], ["09", "Nine", 9], ["10", "Ten", 10]]

    for suit in suits_tup:
        for value in mins_tup:
            page_url = base_url + suit[0] + value[0] + ".htm"
            card_page = requests.get(page_url, timeout=60)
            soup = BeautifulSoup(card_page.content, 'html.parser')
            res = soup.select_one("p:nth-of-type(3)")
            if(res):
                value_long = value[1]
                value_int = value[2]
                suit_long = suit[1]
                name_short = suit[0] + value[0]
                name_long = value_long + ' of ' + suit_long
                line = res.text
                entry = {'name_short': name_short, 'text': line, 'value_long': value_long, 'value_int': value_int, 'name': name_long}
                minorText.append(entry)
                desc = line[:line.find("Divinatory Meanings")]
                meaning_up = line[line.find("Divinatory Meanings")+len("Divinatory Meanings"):line.find("Reversed")]
                meaning_rev = line[line.find("Reversed")+len("Reversed"):]
                c = Minor(suit_long, desc, value_long, value_int, name_long, name_short, meaning_up, meaning_rev)
                cards.append(c.to_JSON())
                print('Added minor card ', c.name)

get_majors()
get_minors()


with open('card_data_tmp.json', mode='w', encoding='utf-8') as f:
    entry = {'count': len(cards), 'cards': cards}
    json.dump(entry, f)

with open('min_text.json', mode='w', encoding='utf-8') as f:
    json.dump(minorText, f)

with open('maj_text.json', mode='w', encoding='utf-8') as f:
    json.dump(majorText, f)
