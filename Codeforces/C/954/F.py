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

from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def find_bridges(self):
        bridges = []
        discovery = [-1] * self.V
        low = [-1] * self.V
        parent = [-1] * self.V
        stack = []

        # Timer for the discovery time
        time = [0]

        for i in range(self.V):
            if discovery[i] == -1:
                stack.append((i, iter(self.graph[i])))
                while stack:
                    node, neighbors = stack[-1]
                    if discovery[node] == -1:
                        discovery[node] = low[node] = time[0]
                        time[0] += 1

                    for neighbor in neighbors:
                        if discovery[neighbor] == -1:
                            parent[neighbor] = node
                            stack.append((neighbor, iter(self.graph[neighbor])))
                            break
                        elif neighbor != parent[node]:
                            low[node] = min(low[node], discovery[neighbor])
                    else:
                        if parent[node] != -1:
                            low[parent[node]] = min(low[parent[node]], low[node])
                            if low[node] > discovery[parent[node]]:
                                bridges.append((parent[node], node))
                        stack.pop()

        return bridges

class UnionFind:
    def __init__(self, n: int):
        self.parent = [x for x in range(n)]
        self.size = [1 for _ in range(n)]
        self.n = n
        self.setCount = n
    
    def Find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.Find(self.parent[x])
        return self.parent[x]
    
    def Union(self, x: int, y: int) -> bool:
        root_x = self.Find(x)
        root_y = self.Find(y)
        if root_x == root_y:
            return False
        if self.size[root_x] > self.size[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_x] = root_y
        self.size[root_y] += self.size[root_x]
        self.setCount -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.Find(x) == self.Find(y)

    def members(self, x):
        root = self.Find(x)
        return [i for i in range(self.n) if self.Find(i) == root]
    
    def roots(self):
        return [i for i, x in enumerate(self.parent) if i == x]
    
    def group_count(self):
        return len(self.roots())
    
    def all_group_members(self):
        mp = defaultdict(list)
        for member in range(self.n):
            mp[self.Find(member)].append(member)
        return mp

# @TIME
def solve(testcase):
    n, m = MI()
    adj = defaultdict(list)
    G = Graph(n + 10)
    uf = UnionFind(n + 10)
    # deg = [0 for _ in range(n)]
    
    for _ in range(m):
        u, v = MI()
        u -= 1
        v -= 1
        adj[u].append(v)
        adj[v].append(u)
        G.add_edge(u, v)
        # deg[u] += 1
        # deg[v] += 1
    
    depth = [0 for _ in range(n + 10)]
    vis = [False for _ in range(n + 10)]
    q = deque()
    q.append(0)
    vis[0] = True
    
    while q:
        cur = q.popleft()
        for o in adj[cur]:
            if not vis[o]:
                vis[o] = True
                depth[o] = depth[cur] + 1
                q.append(o)
        
    
    bridges = G.find_bridges()
    
    k = len(bridges)
    edges = []
    for i in range(k):
        u, v = bridges[i]
        if depth[u] < depth[v]:
            edges.append((v, u))
        else:
            edges.append((u, v))
    
    res = 0
    
    edges.sort(key = lambda x: -depth[x[0]])
    # print(bridges)
    
    vis = [False for _ in range(n + 10)]
    
    @bootstrap
    def dfs(cur, fa):
        vis[cur] = True
        for o in adj[cur]:
            if o == fa:
                continue
            else:
                uf.Union(o, cur)
                if not vis[o]:
                    yield dfs(o, cur)
        yield None
    
    for u, v in edges:
        dfs(u, v)
        rt = uf.Find(u)
        res = max(res, uf.size[rt] * (n - uf.size[rt]))
    
    print(n * (n - 1) // 2 - res)

for testcase in range(II()):
    solve(testcase)