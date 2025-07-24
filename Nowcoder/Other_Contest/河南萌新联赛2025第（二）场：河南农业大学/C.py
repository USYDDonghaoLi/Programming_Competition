'''
Hala Madrid!
https://www.zhihu.com/people/li-dong-hao-78-74
'''

import sys
import os
from io import BytesIO, IOBase
BUFSIZE = 8192
class FastIO(IOBase):
    newlines = 0
    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None
    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()
    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()
    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)
class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")
sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")

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

# seed(19981220)
# RANDOM = getrandbits(64)
 
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

inf = float('inf')

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

mod = 10 ** 9 + 7

# @TIME
def solve(testcase):
    x, p, q, m = MI()
    # prob = p * pow(q, mod - 2, mod)
    # noprob = (1 - prob) % mod

    n = II()
    A = []
    B = []

    for _ in range(n):
        a, b = MI()
        A.append(a)
        B.append(b)
    
    dp = [inf for _ in range(70001)]
    dp[0] = 0

    for i in range(n):
        for g in range(50000 - B[i], -1, -1):
            ng = g + B[i]
            if dp[g] < inf:
                ng = fmin(70000, ng)
            dp[ng] = fmin(dp[ng], dp[g] + A[i])
    
    mi = inf
    C = [inf for _ in range(m * x + 1)]

    for g in range(70000, -1, -1):
        if dp[g] < inf:
            mi = fmin(mi, dp[g])
        if g <= m * x:
            C[g] = mi
    
    D = [0 for _ in range(m + 1)]

    for k in range(1, m + 1):
        D[k] = C[k * x]
    
    fail = q - p
    succ = p
    val = q

    res = 0

    for k in range(1, m + 1):
        if k < m:
            a = pow(fail, k - 1, mod)
            b = pow(val, k, mod)
            invb = pow(b, mod - 2, mod)
            prob = a * succ % mod * invb % mod
        else:
            a = pow(fail, m - 1, mod)
            b = pow(val, m - 1, mod)
            invb = pow(b, mod - 2, mod)
            prob = a * invb % mod
        
        res += prob * D[k] % mod
        res %= mod
    
    print(res)

    # pw = [1 for _ in range(m + 1)]
    # for i in range(1, m + 1):
    #     pw[i] = pw[i - 1] * noprob % mod
    
    # # print(prob, noprob)

    # n = II()
    # A = []

    # for _ in range(n):
    #     a, b = MI()
    #     A.append((a, b))
    
    # if p == q:
    #     res = inf
    #     for a, b in A:
    #         res = fmin(res, a)
    #     print(res)
    #     return
    
    # def compare(p1, p2):
    #     a1, b1 = p1
    #     a2, b2 = p2
    #     if b1 * a2 > b2 * a1:
    #         return -1
    #     elif b1 * a2 < b2 * a1:
    #         return 1
    #     else:
    #         if a1 < a2:
    #             return -1
    #         elif a1 > a2:
    #             return 1
    #         else:
    #             return 0
    
    # A.sort(key = cmp_to_key(compare))

    # money = 0
    # cur = 0
    # res = 0
    # cost = 0

    # for a, b in A:
    #     cost += a
    #     money += b

    #     t, rest = divmod(money, x)

    #     if cur + t < m:
    #         for i in range(cur + 1, cur + t + 1):
    #             # print(i, pw[i - 1], 'debug')
    #             p = pw[i - 1] * prob % mod
    #             res += cost * p % mod
    #         cur += t
    #         money = rest
    #         res %= mod
    #     else:
    #         res += cost * pw[cur] % mod
    #         res %= mod
    #         break

    #     # print(a, b, res)
    
    # print(res)


for testcase in range(1):
    solve(testcase)