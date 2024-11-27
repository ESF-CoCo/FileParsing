from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

import os

EMAIL = os.environ.get('EMAIL')
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')

driver = webdriver.Firefox()
driver.get('https://mail.google.com/mail/u/0/#inbox')

# Sign in
enterAddressField = driver.find_element(By.XPATH, '//*[@id="identifierId"]')

COMPOSEEMAIL = driver.find_element(By.XPATH, '/html/body/div[7]/div[3]/div/div[2]/div[2]/div[1]/div[1]/div/div')
