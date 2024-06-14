from locator import *
from element import BasePageElement

class SearchTextElement(BasePageElement):
    locator = "q"

#will be interited by all page classes
class BasePage(object):
    def __init__(self, driver): #constructor
        self.driver = driver #initializing the driver

#MainPage inherit BasePage class
class MainPage(BasePage):

    search_text_element = SearchTextElement()

    #assert the title of the page
    def is_title_matches(self):
        return "Python" in self.driver.title
    
    def click_go_button(self):
        element = self.driver.find_element(*MainPageLocators.GO_BUTTON)
        element.click()


#SearchResultsPage inherit BasePage class
class SearchResultsPage(BasePage):
    def is_results_found(self):
        return "No results found." not in self.driver.page_source