from random import randint

def generate(length=6, apikey=''):
	with open('diceware.wordlist.asc.txt', 'r') as f:
		wordlist = dict([map(str.strip, line.split()) for line in f if line.strip() != ''])

	password = []

	while len(password) < length:
		key = None
		while key not in wordlist:
			key = ''.join(map(str, [randint(1, 6) for i in range(5)]))

		password.append(wordlist[key])

	return ' '.join(password)