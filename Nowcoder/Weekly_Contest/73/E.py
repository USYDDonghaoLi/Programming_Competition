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

# @TIME
def solve(testcase):
    n = II()
    A = LII()

    s = sum(A)
    if s & 1:
        print(-1)
        return

    m = s >> 1

    dp = [[False for _ in range(m + 1)] for _ in range(n + 1)]
    prev = [[None for _ in range(m + 1)] for _ in range(n + 1)]
    dp[0][0] = True

    for i, v in enumerate(A, 1):
        for j in range(v, m + 1):
            if dp[i - 1][j - v]:
                dp[i][j] = True
                prev[i][j] = j - v
        for j in range(m + 1):
            if dp[i - 1][j]:
                dp[i][j] = True
                prev[i][j] = j

        # print('dp', dp[i])

    if not dp[n][m]:
        print(-1)
        return

    else:
        B = [False for _ in range(n)]
        x, y = n, m
        while True:
            if x == 0 and y == 0:
                break
            px, py = x - 1, prev[x][y]

            if py != y:
                B[x - 1] = True
            x, y = px, py

        # print("B", B)

        C = []
        D = []

        for i, v in enumerate(B):
            if v:
                C.append(i)
            else:
                D.append(i)

        # print("C", C)
        # print("D", D)

        ic, id = 0, 0
        res = []
        while ic < len(C) or id < len(D):
            wc, wd = C[ic], D[id]
            nc, nd = A[wc], A[wd]
            # print("ic, id, wc, wd, nc, nd", ic, id, wc, wd, nc, nd)

            if nc > nd:
                for _ in range(nd):
                    res.append((wc + 1, wd + 1))
                A[wc] -= nd
                A[wd] = 0
                id += 1
            elif nc < nd:
                for _ in range(nc):
                    res.append((wc + 1, wd + 1))
                A[wd] -= nc
                A[wc] = 0
                ic += 1
            else:
                for _ in range(nc):
                    res.append((wc + 1, wd + 1))
                A[wc] = 0
                A[wd] = 0
                ic += 1
                id += 1

        assert ic == len(C) and id == len(D)

        print(len(res))
        for x, y in res:
            print(x, y)


for testcase in range(1):
    solve(testcase)