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
    nums = LII()
    
    mod = 998244353
    dp = [[0 for _ in range(1 << 6)] for _ in range(n + 1)]
    
    for i, v in enumerate(nums[:-1], 1):
        # print('iv', i, v)
        if i == 1:
            if v > 4:
                print(0)
                return
            else:
                for state in range(1 << 6):
                    if state & 1 or state >> 1 & 1:
                        continue
                    cnt = 0
                    for bit in range(2, 6):
                        if state >> bit & 1:
                            cnt += 1
                    if cnt == v:
                        dp[i][state] = 1
        else:
            if v > 6:
                print(0)
                return
            else:
                for state in range(1 << 6):
                    cnt = 0
                    for bit in range(2, 6):
                        if state >> bit & 1:
                            cnt += 1
                    # if i == 2:
                    #     print(state, cnt, v, dp[i - 1][state])
                    if cnt == v:
                        dp[i][state >> 2] += dp[i - 1][state]
                        dp[i][state >> 2] %= mod
                    elif cnt + 1 == v:
                        dp[i][state >> 2 | (1 << 4)] += dp[i - 1][state]
                        dp[i][state >> 2 | (1 << 5)] += dp[i - 1][state]
                        dp[i][state >> 2 | (1 << 4)] %= mod
                        dp[i][state >> 2 | (1 << 5)] %= mod
                    elif cnt + 2 == v:
                        dp[i][state >> 2 | (1 << 4) | (1 << 5)] += dp[i - 1][state]
                        dp[i][state >> 2 | (1 << 4) | (1 << 5)] %= mod
    
    res = 0
    for state in range(1 << 6):
        cnt = 0
        for j in range(2, 6):
            if state >> j & 1:
                cnt += 1
        if cnt == nums[-1]:
            res += dp[n - 1][state]
    
    # for i in range(1, n + 1):
    #     for j in range(1 << 6):
    #         if dp[i][j]:
    #             print('dp', i, j, dp[i][j])
    
    print(res % mod)

for testcase in range(1):
    solve(testcase)