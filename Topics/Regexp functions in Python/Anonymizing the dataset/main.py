import re

string = input()
string = re.sub(r'@\w+', '<AUTHOR>', string, count=1)
string = re.sub(r'@\w+', '<HANDLE>', string)
print(string)
