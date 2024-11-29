from PIL import Image, ImageDraw, ImageFont
import json
import os

QRCODES = 'QRCode/'
FOLDER = 'lanyards/'
TEMPLATE_F = 'templates/Participant Front.png'
TEMPLATE_B = 'templates/Participant Back.png'
PEOPLEFILE = 'participants.json'

FONT_PATH = 'Poppins.ttf'
BOLD_FONT_PATH = 'Poppins-Bold.ttf'
FONT_SIZE = 26

with open(PEOPLEFILE, 'r') as file:
    people = json.load(file)['participants']

    
for person in people:
    name = person['name']
    year = person['year']
    school = person['school']
    schedule = person["schedule"]

    qrcodePath = os.path.join(QRCODES, f"{person['id']}.png")
    
    front = Image.open(TEMPLATE_F)
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
    
    lanyard_path = os.path.join("PartFront", f"{person['id']}_lanyard.png")
    front.save(lanyard_path)
    print(f"Lanyard saved for {name} at {lanyard_path}")
    
    back = Image.open(TEMPLATE_B)
    draw = ImageDraw.Draw(back)

    try:
        font = ImageFont.truetype(FONT_PATH, 15)
    except:
        font = ImageFont.load_default()

    draw.text((415, 320), f"{schedule[0]}", fill="black", font=font)
    draw.text((415, 355), f"{schedule[1]}", fill="black", font=font)
    draw.text((415, 430), f"{schedule[2]}", fill="black", font=font)
    draw.text((415, 470), f"{schedule[3]}", fill="black", font=font)

    if os.path.exists(qrcodePath):
        qrcode = Image.open(qrcodePath).resize((275, 275))
        front.paste(qrcode, (680, 305))
    
    lanyard_path = os.path.join("PartBack", f"{person['id']}_lanyard.png")
    back.save(lanyard_path)


