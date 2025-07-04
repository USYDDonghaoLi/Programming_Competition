# '''
# Hala Madrid!
# https://www.zhihu.com/people/li-dong-hao-78-74
# '''

# import sys
# import os
# from io import BytesIO, IOBase
# BUFSIZE = 8192
# class FastIO(IOBase):
#     newlines = 0
#     def __init__(self, file):
#         self._fd = file.fileno()
#         self.buffer = BytesIO()
#         self.writable = "x" in file.mode or "r" not in file.mode
#         self.write = self.buffer.write if self.writable else None
#     def read(self):
#         while True:
#             b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
#             if not b:
#                 break
#             ptr = self.buffer.tell()
#             self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
#         self.newlines = 0
#         return self.buffer.read()
#     def readline(self):
#         while self.newlines == 0:
#             b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
#             self.newlines = b.count(b"\n") + (not b)
#             ptr = self.buffer.tell()
#             self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
#         self.newlines -= 1
#         return self.buffer.readline()
#     def flush(self):
#         if self.writable:
#             os.write(self._fd, self.buffer.getvalue())
#             self.buffer.truncate(0), self.buffer.seek(0)
# class IOWrapper(IOBase):
#     def __init__(self, file):
#         self.buffer = FastIO(file)
#         self.flush = self.buffer.flush
#         self.writable = self.buffer.writable
#         self.write = lambda s: self.buffer.write(s.encode("ascii"))
#         self.read = lambda: self.buffer.read().decode("ascii")
#         self.readline = lambda: self.buffer.readline().decode("ascii")
# sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
# input = lambda: sys.stdin.readline().rstrip("\r\n")

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
        
        # print(aroute, broute)
        return aroute + [p] + broute[::-1]

# @TIME
def solve(testcase):
    n = II()
    adj = defaultdict(lambda : defaultdict(tuple))
    L = LCA(n + 10)
    
    for _ in range(n - 1):
        x, y, v, c, s = MI()
        x -= 1
        y -= 1
        adj[x][y] = (v, c, s)
        adj[y][x] = (v, c, s)
        L.addedge(x, y)
    
    L.bfs(0)
    
    # print(L.routes(0, 1))
    # print('adj', adj)
    
    @lru_cache(None)
    def calc(a, b):
        R = L.routes(a, b)
        lst = []
        m = len(R)
        
        # print('R', R)
        
        for i in range(1, m):
            u, v = R[i - 1], R[i]
            v, c, s = adj[u][v]
            lst.append((v, 0, i))
            lst.append((s, c, i))
        
        lst.sort()
        # print('lst', lst)
        
        freq = [0 for _ in range(m)]
        cnt = 0
        cur = 0
        l, r = 0, 0
        
        res = []
        costs = []
        
        while r < len(lst):
            while r < len(lst) and cnt < m - 1:
                speed, cost, idx = lst[r]
                cur += cost
                freq[idx] += 1
                if freq[idx] == 1:
                    cnt += 1
                r += 1
            
            speed, cost, idx = lst[l]

            # print(l, r, cnt)
            
            if cnt == m - 1:
                res.append(speed)
                costs.append(cur)

            cur -= cost
            freq[idx] -= 1
            if freq[idx] == 0:
                cnt -= 1
            l += 1
        
        for i in range(len(costs) - 2, -1, -1):
            costs[i] = min(costs[i], costs[i + 1])
        
        # print(res, costs)
        
        return res, costs
        pass
    
    q = II()
    for _ in range(q):
        a, b, e = MI()
        a -= 1
        b -= 1
        res, costs = calc(a, b)
        idx = bisect_right(costs, e) - 1
        print(res[idx])

for testcase in range(1):
    solve(testcase)