import itertools

print(*[
    f'{f} {m}' for f, m in itertools.product(first_names, middle_names)
], sep='\n')
