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

class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)  # Index 0 is unused; tree[1] to tree[n] for positions 1 to n
    
    def fill(self, a):
        # Assumes a is 1-based list: a[0] unused or ignored, a[1] to a[n]
        for i in range(1, self.n + 1):
            self.update(i, a[i])

    def lowbit(self, x):
        return x & (-x)

    def update(self, pos, x):
        # pos is 1-based (1 to n)
        while pos <= self.n:
            self.tree[pos] += x
            pos += self.lowbit(pos)

    def query(self, pos):
        # Prefix sum from 1 to pos (inclusive)
        to_ret = 0
        while pos > 0:
            to_ret += self.tree[pos]
            pos -= self.lowbit(pos)
        return to_ret

    def query_sum(self, l, r):
        if l > r:
            return 0
        # Range sum from l to r (inclusive, 1-based)
        return self.query(r) - self.query(l - 1)

    def lower_bound(self, val):
        # Find the smallest index (1-based) where prefix sum >= val
        ret, su = 0, 0
        for i in reversed(range((self.n + 1).bit_length())):
            ix = ret + (1 << i)
            if ix <= self.n and su + self.tree[ix] < val:
                su += self.tree[ix]
                ret += 1 << i
        return ret + 1  # Adjust to 1-based if ret is 0-based internally
    
    def upper_bound(self, val):
        # Find the smallest index (1-based) where prefix sum > val
        ret, su = 0, 0
        for i in reversed(range((self.n + 1).bit_length())):
            ix = ret + (1 << i)
            if ix <= self.n and su + self.tree[ix] <= val:
                su += self.tree[ix]
                ret += 1 << i
        return ret + 1  # Adjust to 1-based

STRINGS = [
    "",
    "red",
    "rde",
    "dre",
    "der",
    "erd",
    "edr"
]

# @TIME
def solve(testcase):
    n, q = MI()
    s = list(" " + I())

    FS = [FenwickTree(n + 10) for _ in range(7)]

    for i in range(1, n + 1):
        for j in range(1, 7):
            FS[j].update(i, s[i] != STRINGS[j][i % 3])
    
    for _ in range(q):
        ops = LI()
        op = ops[0]

        if op == "1":
            x, c = int(ops[1]), ops[2]
            for j in range(1, 7):
                FS[j].update(x, -(s[x] != STRINGS[j][x % 3]))
            s[x] = c
            for j in range(1, 7):
                FS[j].update(x, s[x] != STRINGS[j][x % 3])
        else:
            l, r = int(ops[1]), int(ops[2])
            res = inf
            for j in range(1, 7):
                res = fmin(res, FS[j].query_sum(l, r))
            print(res)

for testcase in range(1):
    solve(testcase)