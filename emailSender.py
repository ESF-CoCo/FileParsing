from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

import os
from time import sleep

EMAIL = os.environ.get('EMAIL')
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')

driver = webdriver.Firefox()
driver.get('https://mail.google.com/mail/u/0/#inbox')

# Sign in
driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys(EMAIL)
driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button').click()

sleep(3)

driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(USERNAME)
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(PASSWORD)
driver.find_element(By.XPATH, '//*[@id="loginbtn"]').click()

sleep(5)

# Send email
with open('mailmerge.csv', 'r') as file:
	people = [i.strip().split(',') for i in file.readlines()[1:]]

for person in people:
	email,name = person[:2]
	workshops = person[2:5]
	prerequesites = person[6].strip().split('|')
	ID = person[7]
	print(email, name, prerequesites)
	print('\n')
	# driver.find_element(By.XPATH, '/html/body/div[7]/div[3]/div/div[2]/div[2]/div[1]/div[1]/div/div').click()
