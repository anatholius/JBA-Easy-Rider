import re

password = input()
is_correct = re.match(r'\w{6,15}', password, re.A)
print(is_correct and 'Thank you!' or 'Error!')
