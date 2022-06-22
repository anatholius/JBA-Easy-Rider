import re

string = input()
pattern = r"(?<=@)\w+"
results = re.search(pattern, string)
print(results.group())
