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

inv6 = pow(6, mod - 2, mod)

# @TIME
def solve(testcase):
    n = II()

    l, r = 1, n + 1

    def f(mid):
        l = 1
        cnt = 0

        while l <= mid:
            d = mid // l
            r = mid // d
            cnt += (r - l + 1) * d
            l = r + 1
        
        return cnt < n

    while l < r:
        mid = l + r >> 1
        if f(mid):
            l = mid + 1
        else:
            r = mid
    
    # print('l_init', l)

    l -= 1
    full = 0
    left = 1
    while left <= l:
        d = l // left
        r = l // d
        full += (r - left + 1) * d
        left = r + 1
    
    res = 0
    left = 1

    def g(k):
        return k * (k + 1) % mod * (2 * k + 1) % mod * inv6 % mod

    # print(left, l)

    while left <= l:
        d = l // left
        r = l // d

        '''
        从l 到 r 的 每个i, (i * 1) ** 2 + (i * 2) ** 2 + ... + (i * d) ** 2 = i ** 2 * (1 ** 2 + ... + d ** 2)
        '''
        # print('lrd', left, r, d, g(d), g(r), g(left - 1))
        res += g(d) * (g(r) - g(left - 1)) % mod
        res %= mod
        left = r + 1
    
    # print('res', res)
    
    not_full = n - full

    # print(full, not_full)

    res += not_full * (l + 1) % mod * (l + 1) % mod
    res %= mod

    print(res)

for testcase in range(1):
    solve(testcase)