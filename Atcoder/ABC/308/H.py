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
def solve(testcase):
    n, m = MI()
    G = [[float('inf') for _ in range(n)] for _ in range(n)]
    for _ in range(m):
        a, b, c = MI()
        a -= 1
        b -= 1
        G[a][b] = G[b][a] = c
    
    def shortest_cycle(G, r):
        n = len(G)
        dist = [float('inf') for _ in range(n)]
        p = [-1 for _ in range(n)]
        g = [0 for _ in range(n)]
        seen = [False for _ in range(n)]
        dist[r] = 0
        g[r] = r

        for _ in range(n):
            mn = float('inf')
            pos = -1
            for i in range(n):
                if not seen[i] and dist[i] < mn:
                    mn = dist[i]
                    pos = i

            seen[pos] = True
            for i in range(n):
                if dist[i] > dist[pos] + G[pos][i]:
                    dist[i] = dist[pos] + G[pos][i]
                    p[i] = pos
                    g[i] = i if pos == r else g[pos]
        
        mn = float('inf')
        for i in range(n):
            for j in range(i + 1, n):
                if p[i] == j or p[j] == i:
                    continue
                if g[i] == g[j]:
                    continue
                mn = min(mn, dist[i] + dist[j] + G[i][j])
                # print('mn', mn, i, j)
        
        for i in range(n):
            for j in range(i + 1, n):
                if p[i] == j or p[j] == i:
                    continue
                if g[i] == g[j]:
                    continue
                if mn != dist[i] + dist[j] + G[i][j]:
                    continue
                res = []
                a, b = i, j
                while a != r:
                    res.append(a)
                    a = p[a]
                res.append(a)
                res = res[::-1]
                while b != r:
                    res.append(b)
                    b = p[b]
                return mn, res
        
        # print('mn', mn)
        assert False
    
    res = float('inf')
    for a in range(n):
        LEN, CYCLE = shortest_cycle(G, a)
        adj = (CYCLE[1], CYCLE[-1])
        assert len(CYCLE) >= 3
        for i in range(n):
            if i == a or i == adj[0] or i == adj[1]:
                continue
            res = min(res, LEN + G[a][i])
        for i in range(2):
            ori = G[a][adj[i]]
            G[a][adj[i]] = G[adj[i]][a] = float('inf')
            # print(ori, shortest_cycle(G, a))
            res = min(res, shortest_cycle(G, a)[0] + ori)
            G[a][adj[i]] = G[adj[i]][a] = ori
        # print(a, res)
    
    print(res if res != float('inf') else -1)

for testcase in range(1):
    solve(testcase)