#pseudocode for scraping a website and storing the data in dataclasses


import dataclasses

@dataclasses
class Card(object):
    
    def __init__(self, name, description):
        self.name =name
        self.description = description
        self.div_class = css_class
    
    
    
list_of_cards= []
a  = soup.find_all('div', class_='card')

for i in a:
    name = i.find('h2').text
    description = i.find('p').text
    card = Card(name, description)
    list_of_cards.append(card)