import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from main import Browser 
import authorizarion_data


#unittest to test login into linkedin
class TestLinkedIn(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_experimental_option("detach", True)
        driver_path = ChromeDriverManager().install()
        cls.browser = Browser(driver_path)
        cls.browser.open("https://www.linkedin.com/")


    @classmethod
    def tearDownClass(cls):
        cls.browser.close()

    def test_login_and_messaging(self):
        username = authorizarion_data.authorization['username']
        password = authorizarion_data.authorization['password']
        self.browser.login_linkedin(username, password)
        self.browser.go_to_messaging()
        self.assertTrue(self.browser.is_in_messaging_section(), "failed jump to messaging section")

if __name__ == "__main__":
    unittest.main()
