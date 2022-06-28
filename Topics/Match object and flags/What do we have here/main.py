import re

template = '... Jude'
match = re.match(template, input())
print(match and match.group() or None)
