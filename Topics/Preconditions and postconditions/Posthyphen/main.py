import re

string = input()
print(re.search(r'(?<=-)\w+', string).group())
