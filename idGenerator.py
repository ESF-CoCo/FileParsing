import json
from hashlib import sha256

ORGANIZING = 'organising.json'
SUPPORT = 'supportstaff.json'
WORKSHOPS = 'workshops.json'

MAIN = 'participants.json'

with open(MAIN, 'r') as file:
	main = json.load(file)

with open(ORGANIZING, 'r') as file:
	organizing = json.load(file)['Organising Team']

with open(SUPPORT, 'r') as file:
	support = json.load(file)['Support Staff']

with open(WORKSHOPS, 'r') as file:
	workshop = json.load(file)['Workshop Presenter']

people = [*organizing, *support, *workshop]

for ind, person in enumerate(people):
	hashed = sha256((str(ind) + person['name']).encode('utf-8')).hexdigest()
	uuid = hashed[:8] + '-' + hashed[8:12] + '-' + hashed[12:16] + '-' + hashed[16:20] + '-' + hashed[20:32]
	
	people[ind]['id'] = uuid

with open(MAIN, 'w') as file:    
	main['people'] = people
	main['people'].extend(main['participants'])
	json.dump(main, file, indent='\t')
