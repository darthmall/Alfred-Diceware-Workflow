from random import randint

def sysrand(sides=6, rolls=5):
	return ''.join(map(str, [randint(1, sides) for i in range(rolls)]))

def randorg(sides=6, rolls=5):
	raise NotImplemented

def generate(suggestions=1, words=6, apikey=''):
	with open('diceware.wordlist.asc.txt', 'r') as f:
		wordlist = dict([map(str.strip, line.split()) for line in f if line.strip() != ''])

	for i in range(suggestions):
		password = []

		getkey = randorg if apikey else sysrand

		while len(password) < words:
			key = None
			while key not in wordlist:
				key = getkey()

			password.append(wordlist[key])

		yield ' '.join(password)