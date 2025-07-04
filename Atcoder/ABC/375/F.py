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

class Dijkstra:
    def __init__(self, n) -> None:
        self.n = n
        self.graph = defaultdict(list)
    
    
    def addedge(self, e1, e2, weight = 1):
        self.graph[e1].append((e2, weight))
        # self.graph[e2].append((e1, weight))
    
    def f(self, u, v):
        return u << 20 ^ v
    
    def sol(self, src):
        self.prev = [-1 for _ in range(self.n)]
        self.distance = [float('inf') for _ in range(self.n)]
        pq = []
        self.distance[src] = 0
        heappush(pq, self.f(0, src))
        
        while pq:
            z = heappop(pq)
            cost, cur = z >> 20, z & 0xfffff
            if cost > self.distance[cur]:
                continue
            for o, c in self.graph[cur]:
                if cost + c < self.distance[o]:
                    heappush(pq, self.f(cost + c, o))
                    self.distance[o] = cost + c
                    self.prev[o] = cur

    def check(self, start, end, flag = False):
        self.sol(start)
        routes = []
        if flag:
            routes = self.checkroute(end)
        return self.distance[end], routes
    
    def checkroute(self, end):
        cur = end
        routes = []
        while cur != -1:
            routes.append(cur)
            cur = self.prev[cur]
        return routes[::-1]

# @TIME
def solve(testcase):
    n, m, q = MI()
    D = Dijkstra(n)

    edges = []

    for _ in range(m):
        a, b, c = MI()
        edges.append((a - 1, b - 1, c))
    
    dist = [[inf for _ in range(n)] for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    
    queries = []
    S = set()

    for _ in range(q):
        ops = LII()
        if ops[0] == 1:
            queries.append((1, ops[1] - 1))
            S.add(ops[1] - 1)
        else:
            queries.append((2, ops[1] - 1, ops[2] - 1))
    
    for i in range(m):
        if i not in S:
            a, b, c = edges[i]
            dist[a][b] = fmin(dist[a][b], c)
            dist[b][a] = fmin(dist[b][a], c)
            # D.addedge(a, b, c)
            # D.addedge(b, a, c)
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = fmin(dist[i][j], dist[i][k] + dist[k][j])
    
    res = []

    for query in reversed(queries):
        if query[0] == 1:
            a, b, c = edges[query[1]]
            dist[a][b] = fmin(dist[a][b], c)
            dist[b][a] = fmin(dist[b][a], c)

            for i in range(n):
                for j in range(n):
                    dist[i][j] = fmin(dist[i][j], fmin(dist[i][a] + dist[b][j], dist[i][b] + dist[a][j]) + dist[a][b])
            # D.addedge(a, b, c)
            # D.addedge(b, a, c)
        else:
            _, x, y = query
            ans = dist[x][y]
            res.append(-1 if ans == inf else ans)
            # D.sol(x)
            # ans = D.distance[y]
            # res.append(-1 if ans == inf else ans)
    
    for r in reversed(res):
        print(r)

for testcase in range(1):
    solve(testcase)