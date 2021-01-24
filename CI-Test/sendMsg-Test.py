import os,sys
sys.path.append(os.path.abspath(''))
from scripts.browser import WebBrowser
from scripts.getUserId import getUserId
from scripts.sendMsg import sendMsg
from datetime import date



if __name__ == "__main__":
    browser = WebBrowser()

    userId = getUserId('gaetan1903')
    message = f'Test du jour ({date.today()}) ! C\'est Ok'

    sendMsg(browser.browser, userId, message)
    print(f"message: {message} envoyee avec success à {userId}")