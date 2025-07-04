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
    # a, b, s, t = randint(1, 10), randint(1, 10), randint(0, 10), randint(0, 10)
    # a, b, s, t = 10, 9, 4, 4
    # if s > t:
    #     s, t = t, s
    # print(a, b, s, t)
    a, b, s, t = MI()
    res = 0
    for bval in range(1, b + 1):
        '''
        [0, bval - 1]
        '''
        if s >= bval:
            continue
        else:
            l = s
            r = min(t, bval - 1)
        
        c, d = divmod(a, bval)
        res += c * (r - l + 1)
        # print('bval', bval, l, r, res)
        '''
        [1, d]
        '''
        if d:
            if s >= d + 1:
                continue
            else:
                ll = max(1, s)
                rr = min(d, t)
                res += rr - ll + 1
        # print('bval', bval, res)
    
    # def force(a, b, s, t):
    #     cnt = 0
    #     for j in range(1, b + 1):
    #         tt = 0
    #         for i in range(1, a + 1):
    #             if s <= i % j <= t:
    #                 tt += 1
    #                 cnt += 1
    #         print(j, tt)
    #     return cnt
        
    print(res)
    # print(force(a, b, s, t))
            

for testcase in range(1):
    solve(testcase)