import re

string = input()
research = re.findall(r'([A-Z][A-z]+)|(\d+)', string)

print("Capitalized words: {}\nDigits: {}".format(
    ', '.join([w[0] for w in research if w[0]]),
    ', '.join([w[1] for w in research if w[1]]),
))
