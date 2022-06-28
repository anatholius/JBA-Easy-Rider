n = int(input())


def squares():
    yield [i ** 2 for i in range(1, n + 1)]


print(*next(squares()), sep='\n')
