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

mod = 998244353

class Matrix:
    def __init__(self, mat=None):
        if mat is None:
            self.mat = [[0, 0], [0, 0]]
        else:
            self.mat = mat

    def identity(self):
        return Matrix([[1, 0], [0, 1]])

    def __mul__(self, other):
        res = [[0, 0], [0, 0]]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    res[i][j] += self.mat[i][k] * other.mat[k][j]
                    res[i][j] %= mod
        return Matrix(res)

    def __pow__(self, power):
        result = self.identity()
        base = self

        while power:
            if power & 1:
                result = result * base
            base = base * base
            power >>= 1

        return result

    def __str__(self):
        ret = ''
        for i in range(2):
            for j in range(2):
                ret += str(self.mat[i][j]) + " \n"[j == 1]
        return ret
                

# @TIME
def solve(testcase):
    n, m = MI()
    if m == 0:
        print(pow(71, n - 1, mod) * 72 % mod)
    else:
        nums = [LII() for _ in range(m)]
        nums.sort()
        # print(nums)
        lp, lc, res = 0, 0, 0
        
        for p, c in nums:
            if lp == 0:
                res = pow(71, p - 1, mod)
                lp = p
                lc = c
                continue
            else:
                M = Matrix()
                M.mat[0][1] = 71
                M.mat[1][0] = 1
                M.mat[1][1] = 70
                # print('M', M, p - lp)
                M = pow(M, p - lp)
                if c == lc:
                    res = M.mat[0][0] * res % mod
                else:
                    res = M.mat[1][0] * res % mod
                lp = p
                lc = c
            # print(p, res)
        
        # print(res)
        print(res * pow(71, n - lp, mod) % mod)

for testcase in range(1):
    solve(testcase)