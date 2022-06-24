import re

string = input()
print(re.sub(r'(?<=\w)(ou)(?=\w)', 'o', string))
