from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains 
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

sleep(10)

driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(USERNAME)
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(PASSWORD)
driver.find_element(By.XPATH, '//*[@id="loginbtn"]').click()

sleep(20)

# Send email
with open('./certs/certEmail.tsv', 'r') as file:
	people = [i.strip().split('\t') for i in file.readlines()[1:]]

for ind, person in enumerate(people):
	email, name, state = person[1:4]
 
	formattedName = ' '.join(list(map(lambda x: x.lower().capitalize(), name.split(' '))))
	
	if state == 'FALSE': continue
 
	print(f'{formattedName}, #{ind} - {((ind)/len(people))*100}%')
 
	subject = 'ESF CoCo 2024 - Final Words'

	body = f"""Hi {formattedName},

What an incredible day we had at ESF CoCo 2024! On behalf of the entire organizing committee, thank you for joining us and making this event so special. From the inspiring workshops to the engaging sessions, we hope you walked away feeling energized, connected, and full of fresh ideas.

It was an absolute pleasure to host such a vibrant community, and as we start thinking about the next ESF CoCo, we'd love your feedback to help us make it even better. Could you take just a few minutes to fill out our quick feedback form? Your thoughts are invaluable, and will help us immensely:

https://forms.gle/mqQJghFvKBt937NM9

Also, as a token of our appreciation, please find your Certificate of Participation attached to this email. Feel free to download and keep it as a memento of your contribution to ESF CoCo 2024!

Thank you once again for being part of this year's journey. We can't wait to see what the future holds - and we hope to see you at the next ESF CoCo!

Sincerely,
Valentina Banner

On behalf of the ESF CoCo 2024 Organizing Committee

25/F, 1063 King's Rd, Quarry Bay
https://coco.esf.edu.hk/
"""

	certificate = os.getcwd() + '\\certs\\participants\\' + name + '.pdf'
	
	driver.find_element(By.XPATH, '/html/body/div[7]/div[3]/div/div[2]/div[2]/div[1]/div[1]/div/div').click()
	sleep(5)
	
	driver.find_element(By.XPATH, '//input[@aria-label="To recipients"]').send_keys(email)
		
	driver.find_element(By.XPATH, '//input[@name="subjectbox"]').send_keys(subject)
	
	bodyField = driver.find_element(By.XPATH, '//div[@aria-label="Message Body"]')
 
	bodyField.click()
	bodyField.send_keys(body)
 
	driver.find_element(By.XPATH, '//input[@type="file"]').send_keys(certificate)
 
	sleep(5)
 
	driver.find_element(By.XPATH, '//div[@aria-label="Send"]').click()
 
	sleep(5)
 
