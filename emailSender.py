from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains 
from selenium import webdriver

import klembord
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

sleep(7)

driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(USERNAME)
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(PASSWORD)
driver.find_element(By.XPATH, '//*[@id="loginbtn"]').click()

sleep(10)

# Send email
with open('mailmerge.csv', 'r') as file:
	people = [i.strip().split(',') for i in file.readlines()[1:]]

for person in people[:5]:
	email, name = person[:2]
	workshops = person[2:6]
	prerequesites = person[6].strip().split('|')
	ID = person[7]
	
	subject = 'ESF CoCo 2024'
	body = f"""Dear {name},

Thank you for signing up for ESF CoCo this year! It is truly an honor for me to help make this event the best it could possibly be, and we in the Organizing Committee have been working diligently to bring to you a memorable experience which you can hopefully be inspired from.

<b>Your workshops:</b>
Session #1 - {workshops[0]}
Session #2 - {workshops[1]}
Session #3 - {workshops[2]}
Session #4 - {workshops[3]}
{"\nPlease note some of the workshops you have signed up for require the following:\n• "+'\n• '.join(prerequesites) + '\n' if len(prerequesites) > 0 else ""}
Sincerely,
Valentina Banner

On behalf of the ESF CoCo 2024 Organizing Committee

25/F, 1063 King's Rd, Quarry Bay
https://coco.esf.edu.hk/
"""
	
	driver.find_element(By.XPATH, '/html/body/div[7]/div[3]/div/div[2]/div[2]/div[1]/div[1]/div/div').click()
	sleep(2)
 
	driver.find_element(By.XPATH, '/html/body/div[20]/div/div/div/div[1]/div[3]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/form/div[1]/table/tbody/tr[1]/td[2]/div/div/div[1]/div/div[3]/div/div/div/div/div/input').send_keys(email)
	
	driver.find_element(By.XPATH, '/html/body/div[20]/div/div/div/div[1]/div[3]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/form/div[3]/input').send_keys(subject)
 
	driver.find_element(By.XPATH, '/html/body/div[20]/div/div/div/div[1]/div[3]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/div/div[2]/div[2]/div[3]/div/table/tbody/tr/td[2]/div[2]/div/div[1]').click()
	driver.find_element(By.XPATH, '/html/body/div[20]/div/div/div/div[1]/div[3]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/div/div[2]/div[2]/div[3]/div/table/tbody/tr/td[2]/div[2]/div/div[1]').send_keys(body)
	
	driver.find_element(By.XPATH, '/html/body/div[20]/div/div/div/div[1]/div[3]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div/div/div[4]/table/tbody/tr/td[1]/div/div[2]/div[1]').click()
 
	sleep(3)
 
