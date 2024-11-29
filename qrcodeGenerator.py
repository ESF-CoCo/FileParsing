import qrcode
import json

FOLDER = 'QRCode/'
PEOPLEFILE = 'participants.json'

with open(PEOPLEFILE, 'r') as file:
    people = json.load(file)['people']

for person in people:
    qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=10,
		border=4,
	)
    
    qr.add_data(person['id'])
    qr.make(fit=True)
    img = qr.make_image()
    img.save(FOLDER + person['id'] + '.png')
