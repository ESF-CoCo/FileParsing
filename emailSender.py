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

sleep(7)

driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(USERNAME)
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(PASSWORD)
driver.find_element(By.XPATH, '//*[@id="loginbtn"]').click()

sleep(15)

# Send email
with open('mailmerge.csv', 'r') as file:
	people = [i.strip().split(',') for i in file.readlines()[1:]]

for ind, person in enumerate(people):
	email, name = person[:2]
	workshops = person[2:6]
	prerequesites = person[6].strip().split('|')
	ID = person[7]
 
	print(f'{name}, #{ind} - {((ind)/len(people))*100}%')
	
	mainBody = f"Dear {name},"
	midBody = f"""</p>
<p>Thank you for signing up for ESF CoCo this year! It is truly an honor for me to help make this event the best it could possibly be, and we in the Organizing Committee have been working diligently to bring to you a memorable experience which you can hopefully be inspired from.</p>
<p/>
<p>With that said, please note that the main event is on the <b>30th of November</b>, meaning <b>this Saturday</b>, from around 9:00AM-4:00PM at <a href="https://maps.app.goo.gl/wuo5M4HAaV5RskVz8">ESF Center</a> <i>(<b>25/F</b>, 1063 King's Rd, Quarry Bay).</i> Please come at around 8:30-9:00AM. Once you arrive, please head directly to the reception desk to collect your lanyard before the opening ceremony begins. See you all then!</p>
<p/>
<p>Please also <b>bring a charged laptop</b>! Note that our venue has WiFi which you can connect to upon arrival. Also, this is a dress-casual event so feel free to wear any form of appropriate attire.</p>
<p/>
<p>For those of you taking public transport, we recommend taking the MTR to Quarry Bay Station and exiting through either exit A1, A2, or exit B.</p>
<p/>
<p><b>Your timetable:</b></p>
<table border="1" cellpadding="5" cellspacing="0">
    <tr>
        <td colspan="2" style="text-align: center;"><b>Timetable</b></td>
    </tr>
    <tr>
        <td>08:30 - 09:00</td>
        <td><i>Doors Open</i></td>
    </tr>
    <tr>
        <td>09:00 - 09:45</td>
        <td><i>Opening Ceremony</i></td>
    </tr>
    <tr>
        <td>09:55 - 10:55</td>
        <td>{workshops[0]}</td>
    </tr>
    <tr>
        <td>11:00 - 12:00</td>
        <td>{workshops[1]}</td>
    </tr>
    <tr>
        <td>12:00 - 13:00</td>
        <td><i>Lunch</i></td>
    </tr>
    <tr>
        <td>13:00 - 14:00</td>
        <td>{workshops[2]}</td>
    </tr>
    <tr>
        <td>14:05 - 15:05</td>
        <td>{workshops[3]}</td>
    </tr>
    <tr>
        <td>15:15 - 16:00</td>
        <td><i>Closing Ceremony</i></td>
    </tr>
</table>
<br/>
 """
 
	subject = 'ESF CoCo 2024'

	endBody = f"""{("\nPlease note some of the workshops you have signed up for require the following:\n• "+'\n• '.join(prerequesites) + '\n') if prerequesites[0] != '' else ""}
Upon arrival, please use the attached QR code for registration. 

We are all excited to see you soon! In the meantime, if you have any questions or concerns, I'd be more than happy to help.

Sincerely,
Valentina Banner

On behalf of the ESF CoCo 2024 Organizing Committee

25/F, 1063 King's Rd, Quarry Bay
https://coco.esf.edu.hk/
"""

	qrcode = os.getcwd() + '\\QRCode\\' + ID + '.png'
	
	driver.find_element(By.XPATH, '/html/body/div[7]/div[3]/div/div[2]/div[2]/div[1]/div[1]/div/div').click()
	sleep(3)
	
	driver.find_element(By.XPATH, '//input[@aria-label="To recipients"]').send_keys(email)
		
	driver.find_element(By.XPATH, '//input[@name="subjectbox"]').send_keys(subject)
	
	bodyField = driver.find_element(By.XPATH, '//div[@aria-label="Message Body"]')
 
	bodyField.click()
	bodyField.send_keys(mainBody)
 
	driver.execute_script("""
    arguments[0].innerHTML += arguments[1];
""", bodyField, midBody)
 
	driver.execute_script("""
		var body = arguments[0];
		var range = document.createRange();
		var sel = window.getSelection();
		range.selectNodeContents(body);
		range.collapse(false);
		sel.removeAllRanges();
		sel.addRange(range);
	""", bodyField)
 
	bodyField.send_keys(Keys.END+endBody)
 
	driver.find_element(By.XPATH, '//input[@type="file"]').send_keys(qrcode)
 
	sleep(3)
 
	driver.find_element(By.XPATH, '//div[@aria-label="Send"]').click()
 
	sleep(3)
 
