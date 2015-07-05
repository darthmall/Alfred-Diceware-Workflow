from __future__ import print_function

from httplib import HTTPSConnection
from random import randint
from uuid import uuid4

import json, sys


def sysrand(suggestions, words, rolls=5, sides=6, **kwargs):
    print('sysrand', file=sys.stderr)

    for i in range(suggestions):
        yield [''.join(map(str, [randint(1, sides) for i in range(rolls)])) for j in range(words)]


def randorg(suggestions, words, rolls=5, sides=6, apiKey=''):
    conn = HTTPSConnection('api.random.org')

    body = json.dumps({
        'jsonrpc': '2.0',
        'id': str(uuid4()),
        'method': 'generateIntegers',
        'params': {
            'apiKey': apiKey,
            'n' : rolls * words * suggestions,
            'min': 1,
            'max': sides
        }
    })

    headers = {
        'Content-Type': 'raw'
    }

    conn.request('POST', '/json-rpc/1/invoke', body, headers)
    resp = conn.getresponse()
    data = json.loads(resp.read())

    conn.close()

    digits = map(str, data['result']['random']['data'])

    for i in range(suggestions):
        # Base offset into the data for this suggestion
        start = i * words * rolls

        # Build an array of strings. Each string is the key used for a single
        # word in the diceware wordlist. `rolls` corresponds to the number of
        # digits in each key. So each key can be extracted by slicing from
        # the suggestion offset + the word offset within the suggestion. The
        # word offset is equal to the word's index times the number of rolls.
        yield [''.join(digits[start + (j * rolls):start + ((j + 1) * rolls)]) for j in range(words)]


def generate(suggestions=1, words=5, apikey=''):
    with open('diceware.wordlist.asc.txt', 'r') as f:
        wordlist = dict([map(str.strip, line.split()) for line in f if line.strip() != ''])

    getkey = randorg if apikey else sysrand

    for keys in getkey(suggestions, words, apiKey=apikey):
        yield ' '.join([wordlist[k] for k in keys])
