import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup


#to prevent prom closing the window
options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--log-level=1")

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

    def get_page_source(self):
        return self.browser.page_source
    
    def get_soup(self):
        html_source_code = self.browser.execute_script("return document.body.innerHTML;")
        html_soup: BeautifulSoup = BeautifulSoup(html_source_code, 'html.parser')
        return html_soup

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
            print("\nbutton not found")
            self.browser.quit()
        
    
    def accept_cookies(self):
        try:
            accept_cookies_button = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler'))
            )
            accept_cookies_button.click()
        except Exception as e:
            print(f"An error occurred: {e}")

    def press_later_to_reveal_loadmore(self):
        try:
            press_later = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "d-flex")]//cat-button[contains(text(), "Later")]'))
            )
            press_later.click()
        except Exception as e:
            print(f"An error occurred: {e}")

    def load_cat_pages(self):
        try:
            load_more_button = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[text()="Load More"]'))
            )
            time.sleep(1)
            load_more_button.click()
        except Exception as e:
            print(f"An error occurred: {e}")

    def is_fully_loaded(self):
        try:
            count_indicator = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'data-testid="item-count"'))
            )
            count_indicator.split()
            if count_indicator[1] == count_indicator[3]:
                return True
            else:
                return False
        except Exception as e:
            print(f"An error occurred: {e}")

    


        

if __name__ == "__main__":

    # Path for the ChromeDriver
    driver_path = ChromeDriverManager().install()
    browser = Browser(driver_path)

    browser.open("https://parts.cat.com/en/catcorp/shop-by-attachment#sortBy=0")
    time.sleep(0.5)
    browser.accept_cookies()
    time.sleep(0.5)
    browser.press_later_to_reveal_loadmore()


    #if this line is uncommented the program will run till it parses all the products
    #while(not browser.is_fully_loaded()):
    browser.load_cat_pages()

    with open("file.txt", "w", encoding="utf-8") as file:
        file.write(browser.get_soup().prettify())


