CURRENTPPL = 'currPpl.txt'
EMAILSEND = 'emailSend.txt'

def parseFile(fileName) -> list:
	with open(fileName, 'r') as file:
		return [i.strip() for i in file.readlines()]

exclude = parseFile(CURRENTPPL)
fullTo = parseFile(EMAILSEND)

sendTo = list(set([i for i in fullTo if i not in exclude]))

print(' '.join(sendTo))
