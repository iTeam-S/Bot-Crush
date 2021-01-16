import sys
sys.path.append('../scripts/')

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from getUserId import getUserId
from sendMsg import sendMsg

class SendMsgTest():
    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--remote-debugging-port=9515')

        self.userId = getUserId('landris18')
        sendMsg(webdriver.Chrome(), self.userId, 'Test du jour ! C\'est Ok')


if __name__ == "__main__":
    SendMsgTest()