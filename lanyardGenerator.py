from PIL import Image, ImageDraw, ImageFont
import json
import os

QRCODES = 'QRCode/'
FOLDER = 'lanyards/'

TEMPLATES = {
	"participant": ('templates/Participant Front.png', 'templates/Participant Back.png'),
	"organizing": ('templates/Organising Front.png', 'templates/Organising Back.png'),
	"support": ('templates/Staff Front.png', 'templates/Staff Back.png'),
	"photographer": ('templates/Staff Front.png', 'templates/Staff Back.png'),
	"presenter": ('templates/Presenter Front.png', 'templates/Presenter Back.png')
}

MAIN = 'participants.json'

FONT_PATH = 'Poppins.ttf'
BOLD_FONT_PATH = 'Poppins-Bold.ttf'
FONT_SIZE = 26

with open(MAIN, 'r') as file:
	people = json.load(file)['people']

	
for person in people:
	TEMPLATE_F, TEMPLATE_B = TEMPLATES[person['role']]
 
	front = Image.open(TEMPLATE_F)
	back = Image.open(TEMPLATE_B)
 
	qrcodePath = os.path.join(QRCODES, f"{person['id']}.png")
	name = person['name']  # Moved name assignment outside match statement
	
	match person['role']:
		case 'participant':
			year = person['year']
			school = person['school']
			schedule = person["schedule"]

			draw = ImageDraw.Draw(front)

			try:
				font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
			except:
				font = ImageFont.load_default()

			draw.text((50, 215), name, fill="black", font=ImageFont.truetype(BOLD_FONT_PATH, 60))
			draw.text((170, 355), f"{school}", fill="black", font=font)
			draw.text((230, 425), f"{year}", fill="black", font=font)

			if os.path.exists(qrcodePath):
				qrcode = Image.open(qrcodePath).resize((275, 275))
				front.paste(qrcode, (680, 305))
			
			draw = ImageDraw.Draw(back)

			try:
				font = ImageFont.truetype(FONT_PATH, 15)
			except:
				font = ImageFont.load_default()

			draw.text((415, 320), f"{schedule[0]}", fill="black", font=font)
			draw.text((415, 355), f"{schedule[1]}", fill="black", font=font)
			draw.text((415, 430), f"{schedule[2]}", fill="black", font=font)
			draw.text((415, 470), f"{schedule[3]}", fill="black", font=font)

			continue

		case 'organizing':
			role = person['title']
			school = person['school']
			
			draw = ImageDraw.Draw(front)

			try:
				font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
			except:
				font = ImageFont.load_default()

			draw.text((50, 215), name, fill="black", font=ImageFont.truetype(BOLD_FONT_PATH, 60))
			draw.text((148, 338), f"{role}", fill="black", font=font)
			draw.text((200, 408), f"{school}", fill="black", font=font)
   
			if os.path.exists(qrcodePath):
				qrcode = Image.open(qrcodePath).resize((275, 275))
				front.paste(qrcode, (685, 305))

		case 'presenter':
			role = person['role'].capitalize()
			workshop = ' '.join(list(map(lambda x: x.lower().capitalize(), person['workshop'].split(' '))))
			schedule = person['schedule']
			
			
			draw = ImageDraw.Draw(front)

			try:
				font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
			except:
				font = ImageFont.load_default()

			draw.text((105, 230), person['name'], fill="black", font=ImageFont.truetype(BOLD_FONT_PATH, 60))
			draw.text((105, 400), f"{workshop}", fill="black", font=font)

			draw = ImageDraw.Draw(back)

			try:
				font = ImageFont.truetype(FONT_PATH, 12)
			except:
				font = ImageFont.load_default()

			draw.text((590, 285), f"{schedule[0]}", fill="black", font=font)
			draw.text((590, 325), f"{schedule[1]}", fill="black", font=font)
			draw.text((590, 405), f"{schedule[2]}", fill="black", font=font)
			draw.text((590, 445), f"{schedule[3]}", fill="black", font=font)
	
		case 'support' | 'photographer':  # Combined cases for similar handling
			role = person['role'].capitalize()
			school = person['school']

			draw = ImageDraw.Draw(front)

			try:
				font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
			except:
				font = ImageFont.load_default()

			draw.text((50, 215), name, fill="black", font=ImageFont.truetype(BOLD_FONT_PATH, 60))
			draw.text((148, 338), f"{role}", fill="black", font=font)
			draw.text((200, 408), f"{school}", fill="black", font=font)
   
			if os.path.exists(qrcodePath):
				qrcode = Image.open(qrcodePath).resize((275, 275))
				front.paste(qrcode, (685, 305))

		case _:
			print(f'ERROR: Unknown role {person["role"]}')
   
	lanyard_path = os.path.join(FOLDER, f"{person['id']}_front.png")
	front.save(lanyard_path)
	lanyard_path = os.path.join(FOLDER, f"{person['id']}_back.png")
	back.save(lanyard_path)

	print(f'Lanyard saved for {person["name"]}')