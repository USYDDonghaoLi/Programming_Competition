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

# @TIME
def solve(testcase):
    n, m, k = MI()
    A = [(1, 0)]
    for _ in range(n - 1):
        a, b = MI()
        A.append((a, b))
    A.append((1, 0))

    B = [[-inf for _ in range(n + 1)] for _ in range(101)]
    B[k][0] = 0

    adj = [[] for _ in range(n + 1)]
    adj[0].append((1, 0))
    for _ in range(m):
        u, v, w = MI()
        adj[u].append((v, w))
    # print('adj', adj)

    q = deque()
    q.append((k, 0))

    while q:
        # print('q', q)
        num, u = q.popleft()
        strength = B[num][u]
        for v, w in adj[u]:
            if num >= w:
                # print('uv', u, v)
                a, b = A[v]
                if a == 1:
                    newnum = num - w
                    newstrength = strength + b
                    if newstrength >= 0 and newstrength > B[newnum][v]:
                        B[newnum][v] = newstrength
                        q.append((newnum, v))
                elif a == 2:
                    newnum = num - w
                    newstrength = strength
                    for c in range(newnum + 1):
                        if newstrength > B[newnum - c][v]:
                            B[newnum - c][v] = newstrength
                            q.append((newnum - c, v))
                            newstrength += b
                else:
                    # print('3', u, v)
                    newnum = fmin(num - w + b, 100)
                    newstrength = strength
                    # print(newstrength)
                    if newstrength > B[newnum][v]:
                        B[newnum][v] = newstrength
                        q.append((newnum, v))
    
    res = -inf
    for i in range(101):
        res = fmax(res, B[i][n])
    
    print(-1 if res == -inf else res)

for testcase in range(1):
    solve(testcase)