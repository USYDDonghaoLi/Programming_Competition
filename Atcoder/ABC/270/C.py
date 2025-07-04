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

class LCA:
    def __init__(self, n) -> None:
        self.n = n
        self.m = int(log(n, 2))

        self.depth = [float('inf') for _ in range(self.n)]
        self.fa = [[-1 for _ in range(self.m)] for _ in range(self.n)]
        self.graph = defaultdict(list)
    
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
            aroute.append(cur + 1)
            cur = self.fa[cur][0]
        broute = []
        cur = b
        while cur != p:
            broute.append(cur + 1)
            cur = self.fa[cur][0]
        
        return aroute + [p + 1] + broute[::-1]

def solve():
    n, x, y = MI()
    lca = LCA(n)
    for _ in range(n - 1):
        a, b = MI()
        lca.addedge(a - 1, b - 1)
    lca.bfs(0)
    print(*lca.routes(x - 1, y - 1))
    # adj = defaultdict(list)
    # for _ in range(n - 1):
    #     u, v = MI()
    #     adj[u].append(v)
    #     adj[v].append(u)
    
    # q = deque()
    # d = [0 for _ in range(n + 1)]
    # v = [False for _ in range(n + 1)]
    # p = [0 for _ in range(n + 1)]
    # q.append(1)
    # v[1] = True
    # depth = 0

    # while q:
    #     k = len(q)
    #     for _ in range(k):
    #         cur = q.popleft()
    #         d[cur] = depth
    #         for e in adj[cur]:
    #             if not v[e]:
    #                 v[e] = True
    #                 p[e] = cur
    #                 q.append(e)
    #     depth += 1
    
    # start, end = [], []

    # while d[x] > d[y]:
    #     start.append(x)
    #     x = p[x]

    # while d[y] > d[x]:
    #     end.append(y)
    #     y = p[y]
    
    # while x != y:
    #     start.append(x)
    #     end.append(y)
    #     x, y = p[x], p[y]
    
    # print(*start, x, *end[::-1])

for _ in range(1):solve()

