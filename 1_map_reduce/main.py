# 
from functools import reduce

arr = [1, 2, 3, 4, 5, 6, 6]

def add_merge_dicts(d1, d2):
    return(
        {key: d1.get(key, tuple()) + d2.get(key, tuple()) for key in {**d1, **d2}.keys()}
    )


a = reduce(
    add_merge_dicts,
    map(
        lambda val: {val: (1,)},
        arr
        ),
    {}
)

b = list(
    map(
        lambda x: (x[0], len(x[1])),
        a.items()
        )
)

print(a)
print(b)

# get unique values 

# for each triplet get the smallest value 

arr = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12)]

res = map(
    lambda triplet: min(triplet),
    arr
)
print(list(res))

# as well min can be calculated with reduce
def min_reduce(iterable):
    return (
        reduce(
            lambda x, y: x if x < y else y,
            iterable,
            float("inf")
        )
    )


res = map(
    lambda triplet: min_reduce(triplet),
    arr
)
print(list(res))