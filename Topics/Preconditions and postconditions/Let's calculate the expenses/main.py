import re

string = input()
o = re.findall(r'\d* \w+ .?(\d+)', string)
print('This week you have spent: {} dollars'.format(sum(map(int, o))))
