import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#import your login data
import authorizarion_data

#to prevent prom closing the window
options = Options()
options.add_experimental_option("detach", True)

class Browser:
    def __init__(self, driver_path: str):
        self.service = Service(driver_path)
        self.browser = webdriver.Chrome(service=self.service, options=options)

    #navigate to given url
    def open(self, url: str):
        self.browser.get(url)
    
    #close browser
    def close(self):
        self.browser.close()

    #to type username and password
    def add_inputs(self, by: By, value: str, text: str):
        field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((by, value))
        )
        field.send_keys(text)
        time.sleep(1)

    def click_button(self, by: By, value: str):
        try:
            button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((by, value))
            )
            button.click()
            time.sleep(1)
        except:
            print("\nSubmit button not found")
            self.browser.quit()

    def login_linkedin(self, username: str, password: str):
        try:
            sign_in_button = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-tracking-control-name="guest_homepage-basic_nav-header-signin"]'))
            )
            sign_in_button.click()
        except:
            print("\nMain page sign-in button not found")
            self.browser.quit()
            return

        #type username and password
        self.add_inputs(By.ID, "username", username)
        self.add_inputs(By.ID, "password", password)
        
        #click sign-in button
        self.click_button(By.CSS_SELECTOR, "button[type='submit']")

    #to navigate to messaging section on the feed page
    def go_to_messaging(self):
        try:
            messaging_link = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'messaging')]"))
            )
            messaging_link.click()
        except Exception as e:
            print(f"An error occurred: {e}")


    #for unit testing
    def is_in_messaging_section(self):
        try:
            WebDriverWait(self.browser, 10).until(
                EC.title_contains("Messaging")
            )
            return True
        except:
            return False


        

if __name__ == "__main__":
    # Path for the ChromeDriver
    driver_path = ChromeDriverManager().install()
    browser = Browser(driver_path)

    username = authorizarion_data.authorization['username']
    password = authorizarion_data.authorization['password']

    browser.open("https://www.linkedin.com/")
    browser.login_linkedin(username, password)

    browser.go_to_messaging()
