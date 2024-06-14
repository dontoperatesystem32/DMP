from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import unittest
import page

#in braces - inheriting the class unittest.TestCase
class PythonOrgSearch(unittest.TestCase):


    # setUp is a method which is run before each test
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get("http://www.python.org")

    # if starts with test then it will be executed
    def test_example(self):
        assert True
    
    #test correspons to MainPage in page.py
    def test_title(self):
        mainPage = page.MainPage(self.driver)
        assert mainPage.is_title_matches()


    def test_search_python(self):
        mainPage = page.MainPage(self.driver)
        assert mainPage.is_title_matches()
        mainPage.search_text_element = "pycon"
        mainPage.click_go_button()
        search_result_page = page.SearchResultsPage(self.driver)
        assert search_result_page.is_results_found()


    def tearDown(self):
        self.driver.close() # close the browser window



if __name__ == "__main__":
    unittest.main()