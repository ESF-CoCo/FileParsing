from PIL import Image, ImageDraw, ImageFont
import json
import os

QRCODES = 'QRCode/'
FOLDER = 'lanyards/'
TEMPLATE_F = 'templates/Staff Front.png'
TEMPLATE_B = 'templates/Staff Back.png'
PEOPLEFILE = 'supportstaff.json'

FONT_PATH = 'Poppins.ttf'
BOLD_FONT_PATH = 'Poppins-Bold.ttf'
FONT_SIZE = 26

with open(PEOPLEFILE, 'r') as file:
    people = json.load(file)['Support Staff']

    
for person in people:
    name = person['Name']
    role = person['Role']
    school = person['School']

    #qrcodePath = os.path.join(QRCODES, f"{person['id']}.png")
    
    front = Image.open(TEMPLATE_F)
    draw = ImageDraw.Draw(front)

    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except:
        font = ImageFont.load_default()

    draw.text((50, 215), name, fill="black", font=ImageFont.truetype(BOLD_FONT_PATH, 60))
    draw.text((148, 338), f"{role}", fill="black", font=font)
    draw.text((200, 408), f"{school}", fill="black", font=font)

    '''if os.path.exists(qrcodePath):
        qrcode = Image.open(qrcodePath).resize((275, 275))
        front.paste(qrcode, (680, 305))'''
    
    lanyard_path = os.path.join("SupportFront", f"{person['Name']}_lanyard.png")
    front.save(lanyard_path)
    print(f"Lanyard saved for {name} at {lanyard_path}")
    
    back = Image.open(TEMPLATE_B)
    lanyard_path = os.path.join("SupportBack", f"{person['Name']}_lanyard.png")
    back.save(lanyard_path)
