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

mod = 10 ** 9 + 7

class Info:
    
    def __init__(self, LEN = 0, l = 0, r = 0, ans = 0) -> None:
        self.LEN = LEN
        self.l = l
        self.r = r
        self.ans = ans
    
    def __add__(self, other):
        if other.LEN == 0:
            return Info(self.LEN, self.l, self.r, self.ans)
        if self.LEN == 0:
            return Info(other.LEN, other.l, other.r, other.ans)
        
        res = Info()
        res.LEN = self.LEN + other.LEN
        res.l = self.LEN + other.l if self.LEN == self.l else self.l
        res.r = self.r + other.LEN if other.LEN == other.r else other.r
        res.ans = (self.ans + other.ans + self.r * other.l % mod) % mod
        
        return res

    def __str__(self) -> str:
        return f"LEN: {self.LEN}, L: {self.l}, R: {self.r}, ANS: {self.ans}"
         
f = [[0 for _ in range(61)] for _ in range(61)]

def get(n, k):
    if k >= 0:
        return f[n][k]
    else:
        return Info(1 << n, 0, 0, 0)

for i in range(61):
    f[0][i] = Info(1, 1, 1, 1)

for i in range(1, 61):
    for j in range(61):
        f[i][j] = get(i - 1, j) + get(i - 1, j - 1)
        # print(i, j, f[i][j])
# print(f[2][1])

# @TIME
def solve(testcase):
    n, k = MI()
    
    res = Info()
    c = 0
    
    for i in range(59, -1, -1):
        if n >> i & 1:
            res = res + get(i, k - c)
            # print(i, k - c, res)
            c += 1
    
    print(res.ans)

for testcase in range(II()):
    solve(testcase)