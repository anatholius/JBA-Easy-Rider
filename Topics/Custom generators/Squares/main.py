n = int(input())


def squares():
    yield [str(i ** 2) for i in range(1, n + 1)]


print('\n'.join(next(squares())))
