# the list with classes; please, do not modify it
groups = ['1A', '1B', '1C', '2A', '2B', '2C', '3A', '3B', '3C']

c = int(input())
print({v: int(input(' ')) if i < c else None for i, v in enumerate(groups)})

# explanation: `' '` in `input(' ')` allows comprehension to ask about value
