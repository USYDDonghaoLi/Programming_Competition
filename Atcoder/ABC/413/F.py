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

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

d = ((0, 1), (1, 0), (0, -1), (-1, 0))

# @TIME
def solve(testcase):
    n, m, k = MI()
    A = [[0 for _ in range(m)] for _ in range(n)]

    for _ in range(k):
        r, c = GMI()
        A[r][c] = 1
    
    res = 0

    @lru_cache(None)
    def calc(x, y, step):        
        for lim in range(4):
            for i in range(4):
                if i == lim:
                    continue
                d = d[x]
                
    # def calc(x, y, lim, step):
    #     if step > 4:
    #         return inf
    #     # if x == 0 and y == 1:
    #     #     print('debug', A[x][y])
    #     if A[x][y]:
    #         return 0
        
    #     if lim == -1:
    #         res = 0
    #     else:
    #         res = inf
        
    #     for i in range(4):
    #         if i == lim:
    #             continue
    #         dx, dy = d[i]
    #         nx, ny = x + dx, y + dy
    #         if 0 <= nx < n and 0 <= ny < m:
    #             # if x == 0 and y == 0 and lim == -1 and step == 0:
    #             #     print('debug x=0 y=0', nx, ny, calc(nx, ny, i, step + 1) + 1)
    #             if lim == -1:
    #                 res = fmax(res, calc(nx, ny, i, step + 1) + 1)
    #             else:
    #                 res = fmin(res, calc(nx, ny, -1, step + 1) + 1)
    #         else:
    #             if lim == -1:
    #                 res = fmax(res, calc(x, y, i, step + 1) + 1)
    #             else:
    #                 res = fmin(res, calc(x, y, -1, step + 1) + 1)
        
    #     return res

    for i in range(n):
        for j in range(m):
            if not A[i][j]:
                ans = calc(i, j, -1, 0)
                print(i, j, ans)
                if ans != inf:
                    res += ans
    
    print(res)


for testcase in range(1):
    solve(testcase)