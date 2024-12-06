# NOTICE: Make sure to delete the Food Restrictions and Allergies sections before exporting as a TSV
# Also make sure to export as a TSV instead of a CSV

from collections import defaultdict
from hashlib import sha256
import json
from pprint import pprint


PATHNAME = "signups.tsv" # modify based on your file path
EXCLUDEPATHNAME = "exclude.txt"
SUPPORTPATHNAME = "support.txt"

PARTICIPANTSFILE = "participants.json"

MAXPEOPLE = 25 # max people per session

CSVDELIMITER = '\t'

# Parse file
with open(PATHNAME) as file:
	signups = [[j.strip() for j in i.strip().split(CSVDELIMITER)[1:] if j.strip() != ''] for i in file.readlines()[1:]]

AMTPEOPLE = len(signups)

with open(EXCLUDEPATHNAME, 'r') as file:
	exclude = defaultdict(list)

	for i in file.readlines():
		person = tuple(i.strip().split(' '))[:2] 
		exclude[person[0].lower()].extend(person[1].split(','))

with open(PARTICIPANTSFILE, 'r') as file:
	participants = json.load(file)

with open(SUPPORTPATHNAME, 'r') as file:
	SUPPORT = [i.strip().lower() for i in file.readlines()]

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

workshopLimits = defaultdict(lambda: MAXPEOPLE)

workshopLimits['Java Object Oriented Programming'] = 15
workshopLimits['Raspberry Pi Basics'] = 20
workshopLimits['Advanced Introduction to C++'] = 10
workshopLimits['Robotics'] = 20
workshopLimits['Puzzle Prodigy: Code Your Wordle Game with Python'] = 20
workshopLimits['How Algorithms Influence Consumerism'] = 15

LIMIT = [defaultdict(lambda: MAXPEOPLE, {wClass:workshopLimits[wClass] for wClass in CLASSES[i]}) for i in range(4)]

LIMIT[3]['Java Object Oriented Programming'] = 0

for y, session in enumerate(LIMIT):
	if sum(list(session.values())) < AMTPEOPLE:
		for workshop, val in session.items():
			if val == MAXPEOPLE:
				LIMIT[y][workshop] = abs(AMTPEOPLE - sum(list(session.values()))) + MAXPEOPLE
				break

schedule = [{workshop:[] for workshop in CLASSES[i]} for i in range(4)]
people = []

amtSupport = 0
supportAttending = []

workshopPrerequesites = defaultdict(list, {
	'Minecraft Mastery: Crafting Your Own Adventure': [
		'Download Minecraft Education Edition on either a tablet or your laptop (Accounts provided during the workshop)'
	],
	'Puzzle Prodigy: Code Your Wordle Game with Python': [
		'Python installed prior to the day',
		'PyCharm Edu installed prior to the day'
	],
	'Java Object Oriented Programming': [
		'Code editor/IDE installed prior to the day (Recommended to install VS Code)',
  		'Java SDK installed prior to the day'
	],
	'Raspberry Pi Basics': [
		'Thonny installed prior to the day',
  		'Python installed prior to the day'
	],
	'Programming Browser Extensions': [
		'Code editor/IDE installed prior to the day (Recommended to install VS Code)'
	],
	'Advanced Introduction to C++': [
		'Code editor/IDE installed prior to the day (Recommended to install VS Code)'
	],
	'Level Up Your Brain with Google AI': [
		'Please bring a mobile device or tablet as well to the day'
	]
})

for ID, person in enumerate(signups):
	email, name = person[:2]

	name = ' '.join(list(map(lambda x: x.lower().capitalize(), name.split(' '))))
 
	if email.lower() in SUPPORT: 
		amtSupport+=1
		supportAttending.append(email)
	
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
			continue

		sessSched = schedule[ind] # current session's schedule

		chosen = [i for i in session 
					if i in CLASSES[ind] and # Check if class full
					i not in arrangement and # Make sure not previously selected
					len(sessSched[i]) < LIMIT[ind][i] # Make sure valid class
				]

		if len(chosen) == 0: # chosen sessions are full
			selected = False
			for sessName, sessPeople in sessSched.items():
				if len(sessPeople) < LIMIT[ind][sessName] and (sessName not in arrangement):
					chosen = sessName
					selected = True
					break
			
			if not selected:
				raise SystemError(f'No workshop available for {name} in session {ind+1}')
		else:
			chosen = chosen[0] # set to first/top choice
		
		schedule[ind][str(chosen)].append(name)
		arrangement.append(chosen)
	
	hashed = sha256((str(ID)).encode('utf-8')).hexdigest()
	uuid = hashed[:8] + '-' + hashed[8:12] + '-' + hashed[12:16] + '-' + hashed[16:20] + '-' + hashed[20:32]
	
	workshopRequirements = []
 
	for workshop in arrangement:
		workshopRequirements.extend(workshopPrerequesites[workshop])

	workshopRequirements = list(set(workshopRequirements))
 
	personData = {
		'id': uuid,
		'email': email,
		'name': name,
		'role': 'participant',
		'schedule': arrangement,
		'prerequesites': workshopRequirements
	}
 

	people.append(personData)
 
 
workshopNumbers = [[len(schedule[sess][workshop]) for workshop in CLASSES[sess]] for sess in range(4) ]

print('-- SCHEDULE --')
pprint(schedule)

print('\n' * 5)

print('-- PEOPLE --')
pprint(people)

print()

print('-- WORKSHOP NUMBERS --')
pprint(workshopNumbers)

print()

print(f'{amtSupport=}')
pprint(supportAttending)


# Exporting data
participants["participants"] = people

with open(PARTICIPANTSFILE, 'w') as file:
	json.dump(participants, file, indent='\t')

EXPORTCSV = 'mailmerge.csv'

with open(EXPORTCSV, 'w') as file:
	file.write('Email,Name,Session 1,Session 2,Session 3,Workshop Requirements,ID\n')

	for ID, person in enumerate(people):
		prerequesites = '|'.join(person['prerequesites'])
		file.write(','.join([person['email'],person['name'],*person['schedule'],prerequesites,person['id']]) + '\n')


# Output

print()

print("-- CONSOLE --")

while True:
	cmd = input('> ').lower().strip()
	
	match cmd:
		case 'exit':
			exit()
		case 'workshop_names':
			wrkshp = input('Workshop Name: ')
			while wrkshp not in [i for a in CLASSES for i in a]:
				print('Invalid workshop. Please re-enter')
				wrkshp = input('Workshop Name: ')
			
			for ind, session in enumerate(schedule):
				if wrkshp in session.keys():
					print(f'Session #{ind+1}: \n- {'\n- '.join(sorted(session[wrkshp]))}')
		case 'person_workshops':
			name = ' '.join(list(map(lambda x: x.capitalize(), input('Student Name: ').lower().strip().split(' '))))
   
			for person in people:
				if person['name'] == name:
					pprint(person['schedule'])
					break