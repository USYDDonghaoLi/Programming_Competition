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

# '''
# 手写栈防止recursion limit
# 注意要用yield 不要用return
# 函数结尾要写yield None
# '''
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

# RANDOM = getrandbits(32)
 
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

# @TIME
def solve(s, n, m):
    if s & 1:
        print('NO')
        return
    dist = [[float('inf') for _ in range(m + 1)] for _ in range(n + 1)]
    dist[0][0] = 0
    q = deque()
    q.append((0, 0))

    while q:
        a, b = q.popleft()
        c = s - a - b
        if a + b < m + 1:
            if dist[0][a + b] > dist[a][b] + 1:
                dist[0][a + b] = dist[a][b] + 1
                q.append((0, a + b))
        else:
            if dist[a + b - m][m] > dist[a][b] + 1:
                dist[a + b - m][m] = dist[a][b] + 1
                q.append((a + b - m, m))

        if a + b < n + 1:
            if dist[a + b][0] > dist[a][b] + 1:
                dist[a + b][0] = dist[a][b] + 1
                q.append((a + b, 0))
        else:
            if dist[n][a + b - n] > dist[a][b] + 1:
                dist[n][a + b - n] = dist[a][b] + 1
                q.append((n, a + b - n))

        if dist[0][b] > dist[a][b] + 1:
            dist[0][b] = dist[a][b] + 1
            q.append((0, b))

        if a + c < n + 1:
            if dist[a + c][b] > dist[a][b] + 1:
                dist[a + c][b] = dist[a][b] + 1
                q.append((a + c, b))
        else:
            if dist[n][b] > dist[a][b] + 1:
                dist[n][b] = dist[a][b] + 1
                q.append((n, b))
        
        if dist[a][0] > dist[a][b] + 1:
            dist[a][0] = dist[a][b] + 1
            q.append((a, 0))

        if b + c < m + 1:
            if dist[a][b + c] > dist[a][b] + 1:
                dist[a][b + c] = dist[a][b] + 1
                q.append((a, b + c))
        else:
            if dist[a][m] > dist[a][b] + 1:
                dist[a][m] = dist[a][b] + 1
                q.append((a, m))
    
    res = float('inf')
    try:
        res = min(res, dist[s >> 1][s >> 1])
    except:
        pass
    try:
        res = min(res, dist[s >> 1][0])
    except:
        pass
    try:
        res = min(res, dist[0][s >> 1])
    except:
        pass
    
    if res == float('inf'):
        print('NO')
    else:
        print(res)

while True:
    s, n, m = MI()
    if s == 0 and n == 0 and m == 0:
        break
    solve(s, n, m)