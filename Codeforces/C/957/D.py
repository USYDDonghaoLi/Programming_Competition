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
    n, m, k = MI()
    s = I()
    
    q = deque()
    vis = [False for _ in range(n + 1)]
    dist = [inf for _ in range(n + 1)]
    
    for i in range(m):
        if i == n:
            print('YES')
            return
        if i < n:
            if s[i] == 'W':
                q.append(i)
                dist[i] = 1
                vis[i] = True
            elif s[i] == 'L':
                q.append(i)
                dist[i] = 0
                vis[i] = True
    
    while q:
        # print('q', q, dist, m)
        cur = q.popleft()
        if cur + 1 == n:
            dist[cur + 1] = min(dist[cur + 1], dist[cur])
        else:
            if s[cur] == 'W':
                if dist[cur + 1] > dist[cur] + (s[cur + 1] == 'W') and s[cur + 1] != 'C':
                    dist[cur + 1] = dist[cur] + (s[cur + 1] == 'W')
                    if not vis[cur + 1]:
                        vis[cur + 1] = True
                        q.append(cur + 1)
            elif s[cur] == 'L':
                for i in range(1, m + 1):
                    if cur + i == n:
                        dist[cur + i] = min(dist[cur + i], dist[cur])
                    if cur + i < n and dist[cur + i] > dist[cur] + (s[cur + i] == 'W') and s[cur + i] != 'C':
                        # print(cur, cur + i, dist[cur] + (dist[cur + i] == 'W'), dist[cur], (dist[cur + i] == 'W'))
                        dist[cur + i] = dist[cur] + (s[cur + i] == 'W')
                        if not vis[cur + i]:
                            vis[cur + i] = True
                            q.append(cur + i)
    
    # print(dist)
    
    print('YES' if dist[n] <= k else 'NO')
    
for testcase in range(II()):
    solve(testcase)