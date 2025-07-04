from random import *
lst = [i for i in range(1, 11)]
for _ in range(100):
    shuffle(lst)
    print('1', lst)
    res = []
    for i in range(10):
        lst = [lst[-1]] + lst[:9]
        temp = [0]
        for j in range(10):
            temp.append(max(temp[-1], lst[j]))
        res.append(len(set(temp)) - 1)
    print(*res)