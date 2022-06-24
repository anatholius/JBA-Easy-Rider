import re

w_1 = input()
w_2 = input()
if re.match(w_1, w_2):
    print(len(w_2) * 2)
else:
    print('no matching')
