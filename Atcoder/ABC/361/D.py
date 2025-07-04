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


        

# @TIME
def solve(testcase):
    n = II()
    s = 0
    for c in I()[::-1]:
        s <<= 1
        if c == 'W':
            s |= 1
        
    t = 0
    for c in I()[::-1]:
        t <<= 1
        if c == 'W':
            t |= 1
    
    def decode(state, i, j):
        res = []
        for ii in range(n + 2):
            if ii == i or ii == j:
                res.append('.')
            else:
                if state >> ii & 1:
                    res.append('W')
                else:
                    res.append('B')
        return ''.join(res)
    
    dist = [[[inf for _ in range(1 << n + 2)] for _ in range(n + 2)] for _ in range(n + 2)]
    dist[n][n + 1][s] = 0
    
    q = deque()
    q.append((n, n + 1, s))
    while q:
        e1, e2, state = q.popleft()
        for i in range(1, n + 2):
            if i == e1 or i == e2 or i - 1 == e1 or i - 1 == e2:
                continue
            a, b = state >> i & 1, (state >> (i - 1)) & 1
            newstate = state
            newstate ^= a << i
            newstate ^=  b << i - 1
            newstate ^= a << e2
            newstate ^= b << e1
            # print(e1, e2, a, b, state, newstate, decode(state, e1, e2), decode(newstate, i - 1, i))
            if dist[i - 1][i][newstate] > dist[e1][e2][state] + 1:
                dist[i - 1][i][newstate] = dist[e1][e2][state] + 1
                q.append((i - 1, i, newstate))
    
    if dist[n][n + 1][t] == inf:
        print(-1)
    else:
        print(dist[n][n + 1][t])

for testcase in range(1):
    solve(testcase)