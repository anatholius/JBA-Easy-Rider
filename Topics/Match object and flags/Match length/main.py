import re

template = 'are you ready??.?.?'
result = re.match(template, input())
print(len((result or '') and result.group()))
