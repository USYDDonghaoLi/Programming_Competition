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

# @TIME
MOD = 10 ** 9 + 7
def solve(testcase):
    n, m, k= MI()
    mp = {}
    for _ in range(k):
        x, y = MI()
        mp[y] = x
    ed = mp.pop(m, None)
    arr = sorted(mp.items())
    kind = p = a = b = u = 0
 
    def adv(g):
        nonlocal kind, p, a, b, u

        if g == 0:
            return
        
        if kind == 0:
            kind = 1
            u = pow(n, g - 1, MOD)
            p = a = b = 0
        elif kind == 1:
            u = u * pow(n, g, MOD) % MOD
        else:
            s = ((p - 1) * a+(n - p) * b) % MOD
            kind = 1
            u = s * pow(n, g - 1, MOD) % MOD
            p = a = b = 0
 
    def go(r):
        nonlocal kind, p, a, b, u
        if kind == 0:
            ta = 1 if r > 1 else 0
            tb = 0
        elif kind == 1:
            ta = (r - 1) * u % MOD
            tb = (n - r) * u % MOD
        else:
            if r < p:
                ta = (r - 1) * a % MOD
                tb = ((p - r - 1) * a +(n - p) * b) % MOD
            elif r > p:
                ta = ((p - 1) * a+(r - p - 1) * b) % MOD
                tb = (n - r) * b % MOD
            else:
                ta = (p - 1) * a % MOD
                tb = (n - p) * b % MOD
        kind = 2
        p = r
        a = ta
        b = tb
 
    def qry(r, up):
        if kind == 0:
            if up:
                return 1 if r > 1 else 0
            return 0
        if kind == 1:
            return ((r - 1) if up else (n - r)) * u % MOD
        if up:
            if r < p:
                return (r - 1) * a % MOD
            if r > p:
                return ((p - 1) * a + (r - p - 1) * b) % MOD
            return (p - 1) * a % MOD
        if r < p:
            return ((p - r - 1) * a + (n - p) * b) % MOD
        if r > p:
            return (n - r) * b % MOD
        return (n - p) * b % MOD
 
    def tot():
        if kind == 0:
            return 1
        if kind == 1:
            return n * u % MOD
        return ((p - 1) * a + (n - p) * b) % MOD
 
    pre = 0
    for c, r in arr:
        adv(c - pre - 1)
        go(r)
        pre = c
    adv(m - pre - 1)
    if ed is None:
        ans = tot()
    else:
        ans = qry(ed, n < ed)
    print(ans)

for testcase in range(1):
    solve(testcase)