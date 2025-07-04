from random import *
n = randint(1, 20)
m = randint(1, 1 << 20)
k = randint(1, n)
lst = [randint(1, 1 << 20) for _ in range(n)]
print(n, m, k)
print(*lst)