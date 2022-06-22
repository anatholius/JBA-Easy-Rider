import re

string = input()
pattern = "(?<=@)\w+"
results = re.match(pattern, string)
print(results.group())