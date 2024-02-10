# For reference only. Not using anymore.
# A first effort at scraping with Python.
# Use at your own risk. :)

import json
import re
import requests
from bs4 import BeautifulSoup
from security import safe_requests

base_url = 'http://www.sacred-texts.com/tarot/pkt/pkt'
majors_url = 'http://www.sacred-texts.com/tarot/pkt/pkt0303.htm'

cards = []
minorText = []
majorText = []

class Card:
    def __init__(self, value, value_int, name, name_short, meaning_up, meaning_rev):
        """Initializes the object with provided values.
        Parameters:
            - value (str): The value of the object in lowercase.
            - value_int (int): The integer value of the object.
            - name (str): The name of the object in title case.
            - name_short (str): The shortened name of the object in lowercase.
            - meaning_up (str): The meaning of the object in the upright position.
            - meaning_rev (str): The meaning of the object in the reversed position.
        Returns:
            - None: This function does not return any value.
        Processing Logic:
            - Converts the value and name to lowercase and title case respectively.
            - Stores the provided values in the object's attributes.
            - The meanings are stored for both the upright and reversed positions.
            - The meanings are not modified in any way."""
        
        self.value = value.lower()
        self.value_int = value_int
        self.name = name.title()
        self.name_short = name_short.lower()
        self.meaning_up = meaning_up
        self.meaning_rev = meaning_rev

class Major(Card):
    def __init__(self, *args):
        """Creates a new instance of the Major class.
        Parameters:
            - args (tuple): Optional arguments to be passed to the parent class.
        Returns:
            - None: This function does not return anything.
        Processing Logic:
            - Create new instance of Major class.
            - Pass optional arguments to parent class.
            - Set type attribute to "major"."""
        
        super(Major, self).__init__(*args)
        self.type = "major"

    def to_JSON(self):
        """Converts the given data into a JSON format.
        Parameters:
            - self (object): The object to be converted into JSON.
        Returns:
            - dict: A dictionary containing the converted data in JSON format.
        Processing Logic:
            - Creates a dictionary with the given data.
            - Uses the object's attributes as keys.
            - Returns the dictionary."""
        
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
        """"""
        
        super(Minor, self).__init__(*args)
        self.type = "minor"
        self.name = self.value.capitalize() + ' of ' + suit.capitalize()
        self.desc = desc
        self.suit = suit.lower()

    def to_JSON(self):
        """"""
        
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
    """"""
    
    majs = requests.get(majors_url)
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
    """"""
    
    suits_tup = [["wa", "wands"], ["cu", "cups"], ["pe", "pentacles"], ["sw", "swords"]]
    mins_tup = [["pa", "page", 11], ["kn", "knight", 12], ["qu", "queen", 13], ["ki", "king", 14], ["ac", "ace", 1], ["02", "Two", 2], ["03", "Three", 3], ["04", "Four", 4], ["05", "Five", 5], ["06", "Six", 6], ["07", "Seven", 7], ["08", "Eight", 8], ["09", "Nine", 9], ["10", "Ten", 10]]

    for suit in suits_tup:
        for value in mins_tup:
            page_url = base_url + suit[0] + value[0] + ".htm"
            card_page = safe_requests.get(page_url)
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
