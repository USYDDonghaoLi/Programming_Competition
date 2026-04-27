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

d = ((2, 1), (-2, -1), (2, -1), (-2, 1), (1, 2), (-1, -2), (1, -2), (-1, 2))

# @TIME
def solve(testcase):
    n, m, k = MI()
    x1, y1, x2, y2 = GMI()
    q = deque()
    vis = [[[False for _ in range(2)] for _ in range(m)] for _ in range(n)]
    prev = [[[None for _ in range(2)] for _ in range(m)] for _ in range(n)]

    q.append((x1, y1, 0))
    vis[x1][y1][0] = True

    while q:
        x, y, state = q.popleft()
        for dx, dy in d:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and not vis[nx][ny][state ^ 1]:
                vis[nx][ny][state ^ 1] = True
                prev[nx][ny][state ^ 1] = (x, y, state)
                q.append((nx, ny, state ^ 1))
    
    # print('prev', prev)
    
    if not vis[x2][y2][k & 1]:
        print("No")
        return
    
    res = [(x2, y2)]
    x, y, s = x2, y2, k & 1
    while x != x1 or y != y1 or s:
        # print(x, y, s, prev[x][y][s])
        # if not prev[x][y][s]:
        #     break
        x, y, s = prev[x][y][s]
        res.append((x, y))
    
    # print("res", res)

    if len(res) - 1 > k:
        print("No")
        return

    res = res[::-1]
    if k & 1 == len(res) & 1:
        print("No")
        return
    
    m2 = k - len(res) + 1 >> 1
    xx, yy = -1, -1
    for dx, dy in d:
        nx, ny = x2 + dx, y2 + dy
        if 0 <= nx < n and 0 <= ny < m:
            xx, yy = dx, dy
            break
    
    if xx == -1:
        print("No")
        return
    
    for _ in range(m2):
        nx, ny = x2 + xx, y2 + yy
        res.append((nx, ny))
        res.append((x2, y2))
    
    print("Yes")
    for x, y in res[1:]:
        print(x + 1, y + 1)

for testcase in range(1):
    solve(testcase)