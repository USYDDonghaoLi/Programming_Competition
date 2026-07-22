'''
Hala Madrid!
https://github.com/USYDDonghaoLi/Programming_Competition
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

mod = 10 ** 9 + 7
INV2 = pow(2, mod - 2, mod)
INV3 = pow(3, mod - 2, mod)
INV4 = pow(4, mod - 2, mod)

# @TIME
def solve(testcase):
    n = II()
    A = LII()

    p1 = p2 = p3 = p4 = 0
    sum_c2 = 0
    sum_c2_sq = 0
    for x in A:
        p1 = (p1 + x) % mod
        x2 = x * x % mod
        p2 = (p2 + x2) % mod
        x3 = x2 * x % mod
        p3 = (p3 + x3) % mod
        x4 = x3 * x % mod
        p4 = (p4 + x4) % mod
        
        # c2 = x*(x-1)/2
        c2 = x * (x - 1) % mod * INV2 % mod
        sum_c2 = (sum_c2 + c2) % mod
        sum_c2_sq = (sum_c2_sq + c2 * c2 % mod) % mod
    
    e1 = p1
    e2 = (e1 * p1 - p2) % mod * INV2 % mod
    e3 = (p3 - e1 * p2 % mod + e2 * p1 % mod) % mod * INV3 % mod
    e4 = (e1 * p3 % mod - e2 * p2 % mod + e3 * p1 % mod - p4) % mod * INV4 % mod

    share = 0
    for x in A:
        s = (p1 - x) % mod
        share = (share + x * s % mod * ((s - 1) % mod) % mod) % mod
    
    contrib2 = (sum_c2 * sum_c2 - sum_c2_sq) % mod
    
    sum_a2 = p2
    contrib3 = 0
    for x in A:
        c2 = x * (x - 1) % mod * INV2 % mod
        sa = (p1 - x) % mod
        sa2 = (sum_a2 - x * x % mod) % mod
        contrib3 = (contrib3 + c2 * ((sa * sa - sa2) % mod) % mod) % mod
    
    # 4条边
    contrib4 = 2 * e4 % mod
    
    res = (share + contrib2 + contrib3 + contrib4) % mod
    print(res)

for testcase in range(1):
    solve(testcase)