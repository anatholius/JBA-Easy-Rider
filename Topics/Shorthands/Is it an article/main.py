import re

word = input()
print(bool(re.match(r'^the\b', word)))
