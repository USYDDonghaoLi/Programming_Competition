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

mod = 998244353

A = [
    [1,2,3,5,6,7],  # 0
    [3,6],  # 1
    [1,3,4,5,7],  # 2
    [1,3,4,6,7],  # 3
    [2,3,4,6],  # 4
    [1,2,4,6,7],  # 5
    [1,2,4,5,6,7],  # 6
    [1,3,6],  # 7
    [1,2,3,4,5,6,7],  # 8
    [1,2,3,4,6,7]   # 9
]

# @TIME
def solve(testcase):
    
    n = II()
    B = [0] + LII()
    C = [0 for _ in range(10)]

    for d in range(10):
        val = 1
        flag = [False for _ in range(8)]
        for a in A[d]:
            flag[a] = True
        for i in range(1, 8):
            if flag[i]:
                val = val * B[i] % mod
            else:
                val = val * ((100 - B[i]) % mod) % mod
        C[d] = val
    
    D = [0 for _ in range(10000)]
    for d3 in range(10):
        for d2 in range(10):
            for d1 in range(10):
                for d0 in range(10):
                    num = d3 * 1000 + d2 * 100 + d1 * 10 + d0
                    val = C[d3] * C[d2] % mod * C[d1] % mod * C[d0] % mod
                    D[num] = val
    
    s = 0
    for a in range(10000):
        b = n - a
        if 0 <= b < 10000:
            s = (s + D[a] * D[b] % mod) % mod
    
    inv100 = pow(100, mod - 2, mod)
    tmp = pow(inv100, 56, mod)
    res = s * tmp % mod

    print(res)

for testcase in range(II()):
    solve(testcase)