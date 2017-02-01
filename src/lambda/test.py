import main
import sys

miss_you_tests = [
  {
    'expected': 'Andy loves you so much!',
    'slots': {
      'person': { 'value': 'me' },
      'verb': {'value': 'loves'}
    }
  },
  {
    'expected': 'Andy adores you so much!',
    'slots': {
      'person': { 'value': 'you' },
      'verb': {'value': 'adores'}
    }
  },
  {
    'expected': 'Andy misses Melanie so much!',
    'slots': {
      'person': { 'value': 'Melanie' },
      'verb': {'value': 'misses'}
    }
  }
]

failure = False

for test in miss_you_tests:
  expected = test['expected']
  intent = {'slots': test['slots']}
  actual = main.get_miss_you_response(intent)['response']['outputSpeech']['text']
  print(expected == actual, 'expected:', expected, 'actual:', actual)
  if expected != actual:
    failure = True


if failure:
  sys.exit(1)
