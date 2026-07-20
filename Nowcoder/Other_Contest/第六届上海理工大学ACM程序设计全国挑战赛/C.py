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
def solve(testcase):
    n, c, q = MI()
    P = LII()

    NXT = [[-1 for _ in range(n)] for _ in range(30)]
    for i in range(n):
        NXT[0][i] = P[i] - 1
    
    for i in range(1, 30):
        for j in range(n):
            NXT[i][j] = NXT[i - 1][NXT[i - 1][j]]
    

    COST = [
        [
            [[inf for _ in range(c)] for _ in range(c)] for _ in range(n)
            ] for _ in range(30)
    ]

    for room in range(n):
        for i in range(c):
            A = LII()
            for j in range(c):
                COST[0][room][i][j] = A[j]
    
    for i in range(1, 30):
        for j in range(n):
            for prev in range(c):
                for nxt in range(c):
                    for mid in range(c):
                        COST[i][j][prev][nxt] = fmin(COST[i][j][prev][nxt], COST[i - 1][j][prev][mid] + COST[i - 1][NXT[i - 1][j]][mid][nxt])
    
    for _ in range(q):
        x, k, s, t = MI()
        x -= 1

        dist = [inf for _ in range(c)]
        dist[s] = 0
        for i in range(30):
            if k >> i & 1:
                newdist = [inf for _ in range(c)]
                for c1 in range(c):
                    for c2 in range(c):
                        newdist[c2] = fmin(newdist[c2], dist[c1] + COST[i][x][c1][c2])
                x = NXT[i][x]
                dist = newdist
        
        print(dist[t])


for testcase in range(1):
    solve(testcase)