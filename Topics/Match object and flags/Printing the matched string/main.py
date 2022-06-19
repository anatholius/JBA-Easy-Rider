import re


def say_hello(string):
    greeting = re.match('Good (morning|afternoon|evening)', string)
    print(greeting and greeting.group() or 'No greeting!')


# say_hello('Good morning')
# say_hello('Good afternoon')
# say_hello('Good evening')
# say_hello('Good night')
say_hello(input())
