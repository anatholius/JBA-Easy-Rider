import re

string = input()
print(re.search('<START>(.*)<END>', string).groups()[0])
