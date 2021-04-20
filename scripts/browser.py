from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class WebBrowser:
    def __init__(self):
        self.crm_options = Options()

        self.crm_options.add_argument('--no-sandbox')
        self.crm_options.add_argument('--headless')
        self.crm_options.add_argument('--disable-dev-shm-usage')
        # self.crm_options.add_argument('--disable-gpu')
        # self.crm_options.add_argument('--remote-debugging-port=9515')

        self.browser = webdriver.Chrome('/usr/bin/chromedriver', options=self.crm_options)
