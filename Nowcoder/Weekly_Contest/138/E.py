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
def LGMI():
    return list(map(lambda x: int(x) - 1, input().split()))

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




# def f(x, y, z):
#     return x ^ y, y ^ z, z ^ x

# def g(x):
#     b = x & 1
#     x >>= 1
#     a = x & 1
#     x >>= 1
#     return a, b

# def h(x, y):
#     return x << 1 | y

# for a in range(2):
#     for b in range(2):
#         for c in range(2):
#             aa, bb, cc = a, b, c
#             for _ in range(10):
#                 if aa == 1 and bb == 1 and cc == 0:
#                     print('ok', a, b, c)
#                     break
#                 else:
#                     aa, bb, cc = f(aa, bb, cc)

# @TIME
def solve(testcase):
    n = II()
    A = I()

    if A == '1' * n:
        print(n)
    elif A == '0' * n:
        print(0)
    else:
        print(n - 1)
    # A = []

    # for c in I():
    #     A.append(int(c))
    
    # dp = [[-inf for _ in range(4)] for _ in range(n + 1)]
    # res = [0 for _ in range(n + 1)]

    # res[0] = 0
    # res[1] = A[0]
    # res[2] = A[0] + A[1]

    # for j in range(4):
    #     dp[0][j] = 0
    
    # dp[1][A[0]] = A[0]
    # dp[2][A[0] << 1 | A[1]] = A[0] + A[1]

    # for i in range(3, n + 1):
    #     val = A[i - 1]
    #     for j in range(4):
    #         if dp[i - 1][j] == -inf:
    #             continue
    #         a, b = g(j)

    #         print(i, a, b, val, 'iabv')

    #         dp[i][h(b, val)] = fmax(dp[i][h(b, val)], dp[i - 1][j] + val)

    #         aa, bb, cc = a, b, val
    #         for _ in range(8):
    #             aa, bb, cc = f(aa, bb, cc)
    #             print('hi', aa, bb, cc)
    #             dp[i][h(bb, cc)] = fmax(dp[i][h(bb, cc)], res[i - 3] + aa + bb + cc)
    #     res[i] = max(dp[i])

    # print(res[n])

    # for i in range(1, n + 1):
    #     print(i, res[i], dp[i])            

for testcase in range(II()):
    solve(testcase)