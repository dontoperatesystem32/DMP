from dataclasses import dataclass
from bs4 import BeautifulSoup

def export_main_div(soup):
    with open("main_div.txt", "w", encoding="utf-8") as file:
        file.write(soup.prettify())

def export_main_div_cut_ends(soup):
    with open("main_div_cut_ends.txt", "w", encoding="utf-8") as file:
        file.write(soup.prettify())

def open_file_dot_txt():
    with open("file.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        soup = BeautifulSoup("".join(lines), "html.parser")
        return soup
    
#cut first and last line of the file
def open_file_cut_ends(file_name: str):
    with open(file_name, "r", encoding="utf-8") as file:
        lines = file.readlines()
        soup = BeautifulSoup("".join(lines[1:-1]), "html.parser")
        return soup
    

soup = open_file_dot_txt()

#create a huge div that contains all the cards
main_div = soup.find('div', class_="grid-module_grid__YJTic grid-module_grid--cols-2__-UOm2 grid-module_grid--gap-3__Hw0zh comparison-grid_pEFBVWdW")

export_main_div(main_div)

#cut first and last line of the file
soup_of_divs = open_file_cut_ends("main_div.txt")

#split the soup into divs
list_of_divs = soup_of_divs.split('</div>')

#filter dummy divs
filtered_divs = []
for i in range(len(list_of_divs)):
    if i % 2 == 0:
        filtered_divs.append(list_of_divs[i])
    
print(main_div)

#at this point we have a list of divs that contain 2 cards each
#in total there are 16 divs and there will be 32 cards


# list_of_card_dives = []
# for div in filtered_divs:
#     card1 = [div[]]
