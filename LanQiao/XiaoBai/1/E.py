def I():
    return input()
def II():
    return int(input())
def MI():
    return map(int, input().split())
def LI():
    return list(input().split())
def LII():
    return list(map(int, input().split()))
def GMI():
    return map(lambda x: int(x) - 1, input().split())

#------------------------------FastIO---------------------------------

from bisect import *
from heapq import *
from collections import *
from functools import *
from itertools import *
from time import *
from random import *
from math import log, gcd, sqrt, ceil

# '''
# 手写栈防止recursion limit
# 注意要用yield 不要用return
# 函数结尾要写yield None
# '''
# from types import GeneratorType
# def bootstrap(f, stack=[]):
#     def wrappedfunc(*args, **kwargs):
#         if stack:
#             return f(*args, **kwargs)
#         else:
#             to = f(*args, **kwargs)
#             while True:
#                 if type(to) is GeneratorType:
#                     stack.append(to)
#                     to = next(to)
#                 else:
#                     stack.pop()
#                     if not stack:
#                         break
#                     to = stack[-1].send(to)
#             return to
#     return wrappedfunc

# RANDOM = getrandbits(32)
 
# class Wrapper(int):
#     def __init__(self, x):
#         int.__init__(x)

#     def __hash__(self):
#         return super(Wrapper, self).__hash__() ^ RANDOM

# def TIME(f):

#     def wrap(*args, **kwargs):
#         s = perf_counter()
#         ret = f(*args, **kwargs)
#         e = perf_counter()

#         print(e - s, 'sec')
#         return ret
    
#     return wrap


# @TIME
def solve(testcase):
    n = II()
    nums = [0] + LII()

    dp1 = [1 for _ in range(n + 1)]
    dp2 = [1 for _ in range(n + 1)]
    dp1[0] = dp2[0] = 0
    
    for i in range(1, n + 1):
        for j in range(1, i):
            if nums[i] > nums[j]:
                dp1[i] = max(dp1[i], dp1[j] + 1)
    
    for i in range(n, 0, -1):
        for j in range(n, i, -1):
            if nums[i] < nums[j]:
                dp2[i] = max(dp2[i], dp2[j] + 1)
    
    res = 0
    for i in range(n + 1):
        for j in range(i + 2, n + 1):
            if nums[i] + 2 <= nums[j]:
                res = max(res, dp1[i] + 1 + dp2[j])
            if nums[j] > 0:
                res = max(res, dp2[j] + 1)
        if i != n:
            res = max(res, dp1[i] + 1)
    
    print(res)

for testcase in range(1):
    solve(testcase)