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
from math import log
#dfs - stack#
#check top!#

'''
手写栈防止recursion limit
注意要用yield 不要用return
函数结尾要写yield None
'''
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

class Spfa:
    def __init__(self, n) -> None:
        self.n = n
        self.graph = defaultdict(list)
        self.prev = [-1 for _ in range(self.n)]
        self.distance = [float('inf') for _ in range(self.n)]
    
    def addegde(self, e1, e2, weight = 1):
        self.graph[e1].append((e2, weight))
        self.graph[e2].append((e1, weight))
    
    def sol(self, start):
        '''
        用很多次的话就初始化一下
        '''
        for i in range(self.n):
            self.distance[i] = float('inf')
        
        q = deque()
        q.append(start)
        self.distance[start] = 0
        while q:
            cur = q.popleft()
            for e, w in self.graph[cur]:
                weight = self.distance[cur] + w
                if weight < self.distance[e]:
                    self.distance[e] = weight
                    q.append(e)
                    self.prev[e] = cur
        

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

class LCA:
    def __init__(self, n) -> None:
        self.n = n
        self.m = n.bit_length()

        self.depth = [float('inf') for _ in range(self.n)]
        self.fa = [[-1 for _ in range(self.m)] for _ in range(self.n)]
        self.graph = defaultdict(list)
        self.child = defaultdict(list)

    
    def addedge(self, a, b):
        self.graph[a].append(b)
        self.graph[b].append(a)
    
    def bfs(self, root):
        self.depth[root] = 0
        q = deque()
        q.append(root)
        for k in range(self.m):
            self.fa[root][k] = root

        while q:
            k = len(q)
            for _ in range(k):
                cur = q.popleft()
                for e in self.graph[cur]:
                    if self.depth[e] > self.depth[cur] + 1:
                        self.child[cur].append(e)
                        self.depth[e] = self.depth[cur] + 1
                        q.append(e)
                        self.fa[e][0] = cur
                        for i in range(1, self.m):
                            self.fa[e][i] = self.fa[self.fa[e][i - 1]][i - 1]

    def sol(self, a, b):
        if self.depth[a] < self.depth[b]:
            a, b = b, a
        
        for k in range(self.m - 1, -1, -1):
            if self.depth[self.fa[a][k]] >= self.depth[b]:
        
                a = self.fa[a][k]
        if a == b:
            return a
        else:
            for k in range(self.m - 1, -1, -1):
                if self.fa[a][k] != self.fa[b][k]:
                    a, b = self.fa[a][k], self.fa[b][k]
        return self.fa[a][0]
    
    def routes(self, a, b):
        p = self.sol(a, b)
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
    
    def addedge(self, a, b):
        self.graph[a].append(b)
        self.graph[b].append(a)
    
    @bootstrap
    def dfs(self, node, fa = -1):
        self.tin[node] = self.T
        self.T += 1
        if fa == -1:
            self.fa[node][0] = 0
        else:
            self.fa[node][0] = fa
        
        for i in range(1, self.m):
            self.fa[node][i] = self.fa[self.fa[node][i - 1]][i - 1]
        for o in self.graph[node]:
            if o == fa:
                continue
            else:
                yield self.dfs(o, fa)
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
                

def solve():
    pass

for _ in range(II()):solve()
