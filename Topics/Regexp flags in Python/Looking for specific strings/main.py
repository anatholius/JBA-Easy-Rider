import re

string = input()
s = re.match('b.*l', string, flags=re.S | re.I)
print(s and s.group() or 'No match')
