# NOTICE: Make sure to delete the Food Restrictions and Allergies sections before exporting as a TSV
# Also make sure to export as a TSV instead of a CSV

from collections import defaultdict
from hashlib import sha256
import json


PATHNAME = "signups.tsv" # modify based on your file path
EXCLUDEPATHNAME = "exclude.txt"

PARTICIPANTSFILE = "participants.json"

MAXPEOPLE = 25 # max people per session

CSVDELIMITER = '\t'

# Parse file
with open(PATHNAME) as file:
	signups = [[j.strip() for j in i.strip().split(CSVDELIMITER)[1:] if j.strip() != ''] for i in file.readlines()[1:]]

with open(EXCLUDEPATHNAME, 'r') as file:
	exclude = defaultdict(list)

	for i in file.readlines():
		person = tuple(i.strip().split(' '))[:2] 
		exclude[person[0].lower()].extend(person[1].split(','))

with open(PARTICIPANTSFILE, 'r') as file:
	participants = json.load(file)

CLASSES = [
	[
		'Introduction to Large Language Models',
		'Generative AI Short Clip Creation Workshop',
		'Space Game Creation with Phaser',
		'Create an AI being and bring it to Earth',
		'Programming Browser Extensions'
	], # Session 1
	[
		'Raspberry Pi Basics',
		'Generative AI Short Clip Creation Workshop',
		'Java Object Oriented Programming',
		'Create an AI being and bring it to Earth',
		'How Algorithms Influence Consumerism'
	], # Session 2
	[
		'Fun with AI: Face Detection with Javascript',
		'Minecraft Mastery: Crafting Your Own Adventure',
		'Robotics',
		'Advanced Introduction to C++',
		'Building Low-Code Apps'
	], # Session 3
	[
		'Fun with AI: Face Detection with Javascript',
		'Puzzle Prodigy: Code Your Wordle Game with Python',
		'Java Object Oriented Programming',
		'Level Up Your Brain with Google AI',
		'Tech Entrepreneurship Essentials'
	]  # Session 4
]

schedule = [defaultdict(list) for _ in range(4)]
people = []

for ID, person in enumerate(signups):
	email, name = person[:2]

	name = ' '.join(list(map(lambda x: x.lower().capitalize(), name.split(' '))))
	
	choices = [
		person[6:9],
		person[9:12],
		person[12:15],
		person[15:18]
	]

	# Deal with name changes
	for y, i in enumerate(choices):
		for x, j in enumerate(i):
			if j == 'Game Development with Python':
				choices[y][x] = 'Puzzle Prodigy: Code Your Wordle Game with Python'
			elif j == 'Game Development with Minecraft':
				choices[y][x] = 'Minecraft Mastery: Crafting Your Own Adventure'
			elif j == 'Automate your Tasks with Google Gemini':
				choices[y][x] = 'Level Up Your Brain with Google AI'

	arrangement = []
	
	for ind, session in enumerate(choices):
		if str(ind+1) in exclude[email.lower()]:
			arrangement.append('')
			break

		sessSched = schedule[ind] # current session's schedule

		chosen = [i for i in session 
					if len(sessSched[i]) < MAXPEOPLE and  # Check if class full
					i not in arrangement and # Make sure not previously selected
					i in CLASSES[ind] # Make sure valid class
				]

		if len(chosen) == 0: # chosen sessions are full
			for sessName, sessPeople in sessSched.items():
				if len(sessPeople) < MAXPEOPLE:
					chosen = sessName
					break

		else:
			chosen = chosen[0] # set to first/top choice
		
		schedule[ind][chosen].append(name)
		arrangement.append(chosen)
	
	hashed = sha256((str(ID)).encode('utf-8')).hexdigest()
	uuid = hashed[:8] + '-' + hashed[8:12] + '-' + hashed[12:16] + '-' + hashed[16:20] + '-' + hashed[20:32]
	
	personData = {
		'id': uuid,
		'email': email,
		'name': name,
		'role': 'participant',
		'schedule': arrangement
	}

	people.append(personData)

from pprint import pprint
print('-- SCHEDULE --')
pprint(schedule)

print('\n' * 5)

print('-- PEOPLE --')
pprint(people)

# Exporting data
participants["people"].extend(people)

with open(PARTICIPANTSFILE, 'w') as file:
	json.dump(participants, file, indent='\t')
