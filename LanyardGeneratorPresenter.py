from PIL import Image, ImageDraw, ImageFont
import json
import os

QRCODES = 'QRCode/'
FOLDER = 'lanyards/'
TEMPLATE_F = 'templates/Presenter Front.png'
TEMPLATE_B = 'templates/Presenter Back.png'
PEOPLEFILE = 'workshops.json'

FONT_PATH = 'Poppins.ttf'
BOLD_FONT_PATH = 'Poppins-Bold.ttf'
FONT_SIZE = 26

with open(PEOPLEFILE, 'r') as file:
    people = json.load(file)['Workshop Presenter']

for person in people:
    name = person['Org']
    role = person['Workshop']
    schedule = person['Schedule']

    # Front lanyard
    front = Image.open(TEMPLATE_F)
    draw = ImageDraw.Draw(front)

    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except:
        font = ImageFont.load_default()

    draw.text((105, 230), name, fill="black", font=ImageFont.truetype(BOLD_FONT_PATH, 60))
    draw.text((105, 400), f"{role}", fill="black", font=font)

    lanyard_path = os.path.join("PresenterFront", f"{person['id']}_lanyard.png")
    front.save(lanyard_path)
    print(f"Lanyard saved for {name} at {lanyard_path}")

    # Back lanyard
    back = Image.open(TEMPLATE_B)
    draw = ImageDraw.Draw(back)

    try:
        font = ImageFont.truetype(FONT_PATH, 12)
    except:
        font = ImageFont.load_default()

    draw.text((590, 285), f"{schedule[0]}", fill="black", font=font)
    draw.text((590, 325), f"{schedule[1]}", fill="black", font=font)
    draw.text((590, 405), f"{schedule[2]}", fill="black", font=font)
    draw.text((590, 445), f"{schedule[3]}", fill="black", font=font)

    lanyard_path = os.path.join("PresenterBack", f"{person['id']}_lanyard.png")
    back.save(lanyard_path)