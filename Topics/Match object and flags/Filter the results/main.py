import re

template = "Scaramouch."
string = input()
match = re.match(template, string)
print(match and "Match" or "No match")
