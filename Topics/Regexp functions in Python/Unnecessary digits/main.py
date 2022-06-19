import re

names = input()
print(re.split(r'\d+', names))
