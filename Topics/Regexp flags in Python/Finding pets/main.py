import re 

pets = input()
print(re.findall('(dog|cat|parrot|hamster)', pets, flags=re.I))
