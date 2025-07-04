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

class AuxiliaryTree:
    def __init__(self, n, edge, root=0):
        self.n = n
        self.edge = edge
        '''
        eular: dfs时节点的访问顺序
        first: 每个节点在欧拉序列中第一次出现的位置
        '''
        self.eular = [-1] * (2 * n - 1)
        self.first = [-1] * n
        self.depth = [-1] * n
        self.lgs = [0] * (2 * n)
        for i in range(2, 2 * n):
            self.lgs[i] = self.lgs[i >> 1] + 1
        self.st = []
        self.G = [[] for i in range(n)]

        self.dfs(root)
        self.construct_sparse_table()

    def dfs(self, root):
        stc = [root]
        self.depth[root] = 0
        num = 0
        while stc:
            v = stc.pop()
            if v >= 0:
                self.eular[num] = v
                self.first[v] = num
                num += 1
                for u in self.edge[v][::-1]:
                    if self.depth[u] == -1:
                        self.depth[u] = self.depth[v] + 1
                        stc.append(~v)
                        stc.append(u)
            else:
                self.eular[num] = ~v
                num += 1

    def construct_sparse_table(self):
        self.st.append(self.eular)
        sz = 1
        while 2 * sz <= 2 * self.n - 1:
            prev = self.st[-1]
            nxt = [0] * (2 * self.n - 2 * sz)
            for j in range(2 * self.n - 2 * sz):
                v = prev[j]
                u = prev[j + sz]
                if self.depth[v] <= self.depth[u]:
                    nxt[j] = v
                else:
                    nxt[j] = u
            self.st.append(nxt)
            sz *= 2

    def lca(self, u, v):
        x = self.first[u]
        y = self.first[v]
        if x > y : x , y = y , x
        d = self.lgs[y - x + 1]
        return (
            self.st[d][x]
            if self.depth[self.st[d][x]] <= self.depth[self.st[d][y - (1 << d) + 1]]
            else self.st[d][y - (1 << d) + 1]
        )

    def query(self, vs):
        """
        vs: 虚树中包含的顶点集合
        self.G: 虚树
        return: 虚树的根 (sz中所有顶点的lca)
        """

        k = len(vs)
        if k == 0:
            return -1
        vs.sort(key=self.first.__getitem__)
        stc = [vs[0]]
        self.G[vs[0]] = []

        for i in range(k - 1):
            w = self.lca(vs[i], vs[i + 1])
            if w != vs[i]:
                last = stc.pop()
                while stc and self.depth[w] < self.depth[stc[-1]]:
                    self.G[stc[-1]].append(last)
                    last = stc.pop()

                if not stc or stc[-1] != w:
                    stc.append(w)
                    vs.append(w)
                    self.G[w] = [last]
                else:
                    self.G[w].append(last)
            stc.append(vs[i + 1])
            self.G[vs[i + 1]] = []

        for i in range(len(stc) - 1):
            self.G[stc[i]].append(stc[i + 1])

        return stc[0]
# @TIME
def solve(testcase):
    n = II()
    adj = defaultdict(list)
    
    for _ in range(n - 1):
        u, v = MI()
        u -= 1
        v -= 1
        adj[u].append(v)
        adj[v].append(u)
    
    A = LII()
    mp = defaultdict(list)
    for i in range(n):
        A[i] -= 1
    for i, a in enumerate(A):
        mp[a].append(i)
    
    depth = [-1 for _ in range(n)]
    depth[0] = 0
    todo = [0]
    
    while todo:
        v = todo.pop()
        for u in adj[v]:
            if depth[u] == -1:
                depth[u] = depth[v] + 1
                todo.append(u)
    
    # print(depth)
    
    T = AuxiliaryTree(n, adj)
    
    res = 0
    dp = [0 for _ in range(n)]
    
    for c in range(n):
        if c in mp and len(mp[c]) > 1:
            s = len(mp[c])
            rt = T.query(mp[c])
            todo = [~rt, rt]
            # print(T.G)
            
            while todo:
                v = todo.pop()
                if v >= 0:
                    dp[v] = 0
                    for u in T.G[v]:
                        todo.extend([~u, u])
                else:
                    v = ~v
                    for u in T.G[v]:
                        res += (s - dp[u]) * dp[u] * (depth[u] - depth[v])
                        dp[v] += dp[u]
                    if A[v] == c:
                        dp[v] += 1
                # print('dp', dp, todo)
    
    print(res)

for testcase in range(1):
    solve(testcase)