import re


string = input()
template = 'never gonna let you down...'
match = re.match(template, string, flags=re.I)
