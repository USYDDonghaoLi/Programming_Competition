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

class Dijkstra:
    """有权图上的单源最短路模板，适合边权非负的情况。"""

    def __init__(self, n) -> None:
        self.n = n
        self.graph = defaultdict(list)

    def add_edge(self, u, v, weight=1):
        self.graph[u].append((v, weight))

    def _pack(self, dist, node):
        return (dist << 20) ^ node

    def shortest_path(self, src):
        self.prev = [-1 for _ in range(self.n)]
        self.distance = [float('inf') for _ in range(self.n)]
        pq = []
        self.distance[src] = 0
        heappush(pq, self._pack(0, src))

        while pq:
            packed = heappop(pq)
            cost, cur = packed >> 20, packed & 0xfffff
            if cost > self.distance[cur]:
                continue
            for nxt, w in self.graph[cur]:
                new_cost = cost + w
                if new_cost < self.distance[nxt]:
                    heappush(pq, self._pack(new_cost, nxt))
                    self.distance[nxt] = new_cost
                    self.prev[nxt] = cur

    def query(self, start, end, need_path=False):
        self.shortest_path(start)
        routes = []
        if need_path:
            routes = self.get_path(end)
        return self.distance[end], routes

    def get_path(self, end):
        cur = end
        routes = []
        while cur != -1:
            routes.append(cur)
            cur = self.prev[cur]
        return routes[::-1]

# @TIME
def solve(testcase):
    n, m = MI()
    A = [[] for _ in range(n)]
    B = [[] for _ in range(n)]

    D1 = Dijkstra(n)

    for _ in range(m):
        u, v, d, r = MI()
        u -= 1
        v -= 1
        A[u].append((v, d, r))
        B[v].append((u, d, r))
        D1.add_edge(u, v, d)

    D1.shortest_path(0)

    if D1.distance[n - 1] == inf:
        print(-1, -1)
        return

    pq = []
    heappush(pq, (0, 0))
    # vis = [False for _ in range(n)]
    # vis[0] = True
    dist = [inf for _ in range(n)]
    dist[0] = 0

    while pq:
        cost, u = heappop(pq)
        if dist[u] != cost:
            continue

        for v, d, r in A[u]:
            if D1.distance[v] == D1.distance[u] + d:
                nc = cost + r
                if nc < dist[v]:
                    dist[v] = nc
                    heappush(pq, (nc, v))

    print(D1.distance[n - 1], dist[n - 1])
    

for testcase in range(1):
    solve(testcase)