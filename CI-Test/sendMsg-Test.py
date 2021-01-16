import sys, os
sys.path.append('../scripts/')

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from getUserId import getUserId
from sendMsg import sendMsg

class SendMsgTest():
    def __init__(self):
        print(os.environ)

        self.crm_options = Options()
        self.crm_options.add_argument('--headless')
        self.crm_options.add_argument('--no-sandbox')
        self.crm_options.add_argument('--disable-dev-shm-usage')
        self.crm_options.add_argument('--remote-debugging-port=9515')

        self.userId = getUserId('landris18')
        print("ID => ",self.userId)
        sendMsg(webdriver.Chrome('/usr/bin/chromedriver',options=self.crm_options), self.userId, 'Test du jour ! C\'est Ok')


if __name__ == "__main__":
    SendMsgTest()