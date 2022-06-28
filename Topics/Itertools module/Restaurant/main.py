import itertools

dishes = itertools.product(main_courses, desserts, drinks)
prices = itertools.product(price_main_courses, price_desserts, price_drinks)
wallet = 30

print(*[' '.join([*d, str(sum(p))])
        for d, p in zip(dishes, prices)
        if sum(p) <= wallet],
      sep='\n')
