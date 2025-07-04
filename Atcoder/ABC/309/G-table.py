from itertools import *
n = int(input())
x = int(input())
nums = [i + 1  for i in range(n)]
res = 0
for p in permutations(nums):
    flag = True
    for i, v in enumerate(p):
        if abs(v - i - 1) < x:
            flag = False
            break
    res += flag

print(res)