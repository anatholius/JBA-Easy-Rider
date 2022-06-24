import re

match = re.match(r'[A-Za-z]\w+', input())
ok = 'Thank you!'
nope = 'Oops! The username has to start with a letter.'
print(match and ok or nope)
