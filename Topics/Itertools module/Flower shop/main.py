import itertools

bucket_max_count = 3
print(*[flowers
        for i in range(bucket_max_count)
        for flowers in itertools.combinations(flower_names, i + 1)
        ], sep='\n')
