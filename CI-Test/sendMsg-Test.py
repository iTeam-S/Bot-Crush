import sys
sys.path.append('../scripts/')
from selenium import webdriver
from getUserId import getUserId
from sendMsg import sendMsg

userId = getUserId('landris18')
sendMsg(webdriver.Chrome(), userId, 'Test du jour ! C\'est Ok')


