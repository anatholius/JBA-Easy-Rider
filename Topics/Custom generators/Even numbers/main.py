n = int(input())


def even():
    # yield [i for i in range(n * 2) if not i % 2]
    # yield [i for i in range(0, n * 2, 2)]
    yield list(range(0, n * 2, 2))


print(*next(even()), sep='\n')
