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

class Mobius:

    def __init__(self, n) -> None:
        self.n = n
        self.mu = [1] * (n + 1)
        self.primes = []
        self.vis = [False] * (n + 1)

        for i in range (2, n + 1):
            if not self.vis[i]:
                self.primes.append(i)
                self.mu[i] = -1
            for prime in self.primes:
                if i * prime > n:
                    break
                self.vis[i * prime] = True
                if i % prime == 0:
                    self.mu[i * prime] = 0
                    break
                else:
                    self.mu[i * prime] = -self.mu[i]
    
    def get(self, i):
        return self.mu[i]

M = Mobius(100)

pw = [1 << i for i in range(61)]

def floor_log(n):
    l, r = 0, 60
    while l < r:
        mid = l + r >> 1
        if pw[mid] < n:
            l = mid + 1
        else:
            r = mid
    return l

def mypow(num, k):
    res = num
    for _ in range(k - 1):
        res *= num
        if res > 10 ** 18:
            return -1
    return res

def my_sqrt(n, k):
    l, r = 1, n + 1
    while l < r:
        mid = l + r >> 1
        p = mypow(mid, k)
        if p == -1:
            r = mid
        else:
            if p <= n:
                l = mid + 1
            else:
                r = mid
    return l - 1

# @TIME
def solve(testcase):
    n = II()
    res = n
    for i in range(1, floor_log(n) + 1):
        res -= M.get(i) * (my_sqrt(n, i) - 1)
    print(res)

for testcase in range(1):
    solve(testcase)