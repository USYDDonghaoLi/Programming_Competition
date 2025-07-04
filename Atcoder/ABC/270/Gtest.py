from random import *
a = randint(1, 1000)
b = randint(1, 1000)
p = randint(1, 10 ** 9)
s = randint(1, 1000)
s %= p
S = set()
g = s
S.add(g)

for _ in range(1, 1000):
    g = (a * g + b) % p
    S.add(g)

ans = []
t = []

for i in range(1000, 1010):
    g = (a * g + b) % p
    if g not in S:
        t.append([p, a, b, s, g])
        ans.append(i)

print(len(t))
for i in range(len(t)):
    print(*t[i])
print(ans)
