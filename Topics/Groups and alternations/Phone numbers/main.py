import re


def show(t):
    match = re.match(r'\+(\d+)[-\s]?(\d{3})[-\s]?(\d{3}([-\s]?\d{2}){2})', t)

    country = match and match.group(1)
    area = match and match.group(2)
    number = match and match.group(3)

    print(*(match and [
        f'Full number: {t}\n',
        f'Country code: {country}\n',
        f'Area code: {area}\n',
        f'Number: {number}\n',
    ]) or 'No match', sep='')


show(input())
