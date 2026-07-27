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


# ------------------------------FastIO---------------------------------

from bisect import *
from heapq import *
from collections import *
from functools import *
from itertools import *
from time import *
from random import *
from math import log

# dfs - stack
# check top!

"""
手写栈防止 recursion limit。
注意：这里保留 bootstrap 方案，并保持生成器式写法。
"""
from types import GeneratorType


def bootstrap(f, stack=[]):
    def wrappedfunc(*args, **kwargs):
        if stack:
            return f(*args, **kwargs)
        else:
            to = f(*args, **kwargs)
            while True:
                if type(to) is GeneratorType:
                    stack.append(to)
                    to = next(to)
                else:
                    stack.pop()
                    if not stack:
                        break
                    to = stack[-1].send(to)
            return to

    return wrappedfunc


class SPFA:
    """无负权图上的最短路，适合做单源最短路径的通用模板。"""

    def __init__(self, n) -> None:
        self.n = n
        self.graph = defaultdict(list)
        self.prev = [-1 for _ in range(self.n)]
        self.distance = [float('inf') for _ in range(self.n)]

    def add_edge(self, u, v, weight=1):
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))

    def shortest_path(self, start):
        """从 start 出发求所有点的最短路。"""
        for i in range(self.n):
            self.distance[i] = float('inf')

        q = deque()
        q.append(start)
        self.distance[start] = 0
        while q:
            cur = q.popleft()
            for nxt, w in self.graph[cur]:
                new_dist = self.distance[cur] + w
                if new_dist < self.distance[nxt]:
                    self.distance[nxt] = new_dist
                    q.append(nxt)
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


class UnionFind:
    """并查集模板，适合维护连通性和合并操作。"""

    def __init__(self, n: int):
        self.parent = [x for x in range(n)]
        self.size = [1 for _ in range(n)]
        self.n = n
        self.component_count = n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False
        if self.size[root_x] > self.size[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_x] = root_y
        self.size[root_y] += self.size[root_x]
        self.component_count -= 1
        return True

    def is_connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)

    def count(self):
        return self.component_count


class LCA:
    """倍增法 LCA 模板，适合离线预处理后快速求公共祖先。"""

    def __init__(self, n) -> None:
        self.n = n
        self.m = n.bit_length()

        self.depth = [float('inf') for _ in range(self.n)]
        self.fa = [[-1 for _ in range(self.m)] for _ in range(self.n)]
        self.graph = defaultdict(list)
        self.child = defaultdict(list)

    def add_edge(self, a, b):
        self.graph[a].append(b)
        self.graph[b].append(a)

    def build(self, root):
        self.depth[root] = 0
        q = deque()
        q.append(root)
        for k in range(self.m):
            self.fa[root][k] = root

        while q:
            k = len(q)
            for _ in range(k):
                cur = q.popleft()
                for nxt in self.graph[cur]:
                    if self.depth[nxt] > self.depth[cur] + 1:
                        self.child[cur].append(nxt)
                        self.depth[nxt] = self.depth[cur] + 1
                        q.append(nxt)
                        self.fa[nxt][0] = cur
                        for i in range(1, self.m):
                            self.fa[nxt][i] = self.fa[self.fa[nxt][i - 1]][i - 1]

    def query(self, a, b):
        if self.depth[a] < self.depth[b]:
            a, b = b, a

        for k in range(self.m - 1, -1, -1):
            if self.depth[self.fa[a][k]] >= self.depth[b]:
                a = self.fa[a][k]
        if a == b:
            return a

        for k in range(self.m - 1, -1, -1):
            if self.fa[a][k] != self.fa[b][k]:
                a, b = self.fa[a][k], self.fa[b][k]
        return self.fa[a][0]

    def get_path(self, a, b):
        p = self.query(a, b)
        aroute = []
        cur = a
        while cur != p:
            aroute.append(cur)
            cur = self.fa[cur][0]
        broute = []
        cur = b
        while cur != p:
            broute.append(cur)
            cur = self.fa[cur][0]
        return aroute + [p] + broute


class LCA2:
    """DFS + 递归式 LCA 模板，适合需要时间戳/祖先判断的场景。"""

    def __init__(self, n) -> None:
        self.n = n
        self.m = n.bit_length()

        self.depth = [float('inf') for _ in range(self.n)]
        self.fa = [[-1 for _ in range(self.m)] for _ in range(self.n)]
        self.graph = defaultdict(list)
        self.child = defaultdict(list)

        self.tin = [0 for _ in range(self.n)]
        self.tout = [0 for _ in range(self.n)]
        self.T = 0

    def add_edge(self, a, b):
        self.graph[a].append(b)
        self.graph[b].append(a)

    @bootstrap
    def dfs(self, node, fa=-1):
        self.tin[node] = self.T
        self.T += 1
        if fa == -1:
            self.fa[node][0] = 0
        else:
            self.fa[node][0] = fa

        for i in range(1, self.m):
            self.fa[node][i] = self.fa[self.fa[node][i - 1]][i - 1]

        for nxt in self.graph[node]:
            if nxt == fa:
                continue
            yield from self.dfs(nxt, node)

        self.tout[node] = self.T
        self.T += 1
        yield None

    def is_ancestor(self, u, v):
        return self.tin[u] <= self.tin[v] and self.tout[u] >= self.tout[v]

    def LCA(self, x, y):
        pass


class Topsort_Directed:
    def __init__(self, n) -> None:
        self.n = n
        self.graph = defaultdict(set)
        self.rgraph = defaultdict(set)
        self.degree = [0 for _ in range(self.n)]
    
    def add_edge(self, a, b):
        self.graph[a].add(b)
        self.rgraph[b].add(a)
        self.degree[a] += 1

    def sort(self):
        self.d = self.degree[:]
        graphlist = []
        q = deque()
        for i in range(1, self.n):
            if not self.d[i]:
                q.append(i)
        while q:
            cur = q.popleft()
            graphlist.append(cur)
            for e in self.rgraph[cur]:
                self.d[e] -= 1
                if not self.d[e]:
                    q.append(e)
        
        return graphlist

class TopSort_Tree:
    def __init__(self, n) -> None:
        self.n = n
        self.graph = defaultdict(set)
        self.parent = [n + 1 for _ in range(self.n)]
    
    def add_edge(self, a, b):
        self.graph[a].add(b)
        self.graph[b].add(a)
    
    def sort(self, root):
        graphlist = []
        q = deque()
        q.append((root, -1))
        while q:
            cur, fa = q.popleft()
            graphlist.append(cur)
            for e in self.graph[cur]:
                if e == fa:
                    continue
                else:
                    self.parent[e] = cur
                    q.append((e, cur))
        return graphlist[::-1]
                
def shortest_cycle(G, r):
        n = len(G)
        dist = [float('inf') for _ in range(n)]
        p = [-1 for _ in range(n)]
        g = [0 for _ in range(n)]
        seen = [False for _ in range(n)]
        dist[r] = 0
        g[r] = r

        for t in range(n):
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


# @TIME
def solve(testcase):
    n, m, s, t, q = MI()

    DIJ = Dijkstra(n)

    for _ in range(m):
        u, v, w = MI()
        DIJ.add_edge(u - 1, v - 1, w)
        DIJ.add_edge(v - 1, u - 1, w)

    DIJ.shortest_path(s - 1)

    res = DIJ.distance[t - 1]

    k = 0
    while res:
        k += 1
        res >>= 1
    
    if k <= q:
        print('YES')
    else:
        print('NO')
        print(k)

for testcase in range(II()):
    solve(testcase)