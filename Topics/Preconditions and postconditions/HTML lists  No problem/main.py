import re

string = input()
print(*re.findall('<li>(.*?)</li>', string), sep='\n')
