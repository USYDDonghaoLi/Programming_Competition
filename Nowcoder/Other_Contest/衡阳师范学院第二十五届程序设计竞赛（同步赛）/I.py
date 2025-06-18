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

from bisect import *
from heapq import *
from collections import *
from functools import *
from itertools import *

class UnionFind:
    def __init__(self, n: int):
        self.parent = [x for x in range(n)]
        self.size = [1 for _ in range(n)]
        self.n = n
        self.setCount = n
    
    def Find(self, a: int) -> int:
        a = self.parent[a]
        acopy = a
        while a != self.parent[a]:
            a = self.parent[a]
        while acopy != a:
            self.parent[acopy], acopy = a, self.parent[acopy]
        return a
    
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
    n = II()
    adj = [[] for _ in range(n)]

    for _ in range(n - 1):
        u, v = GMI()
        adj[u].append(v)
        adj[v].append(u)
    
    uf = UnionFind(n)
    for u in range(n):
        m = len(adj[u])
        if m == 3:
            for v in adj[u]:
                if len(adj[v]) == 3:
                    uf.Union(u, v)
    
    mp = uf.all_group_members()
    for rt in mp:
        a, b = -1, -1
        if len(adj[rt]) == 3:
            for o in mp[rt]:
                for u in adj[o]:
                    if len(adj[u]) == 2:
                        if a == -1:
                            a = u
                        elif b == -1 and a != u:
                            b = u
            if a != -1 and b != -1:
                adj[a].append(b)
                adj[b].append(a)
                uf.Union(a, rt)
                uf.Union(b, rt)

                cycle = set()
                other = set()

                for i in range(n):
                    if uf.Find(i) == uf.Find(rt):
                        cycle.add(i)
                    else:
                        other.add(i)
                
                for u in cycle:
                    cnt = 0
                    for v in adj[u]:
                        if v in other:
                            cnt += 1
                    if cnt != 1:
                        print(-1)
                        return
                
                for u in other:
                    if len(adj[u]) != 1:
                        print(-1)
                        return
                    if adj[u][0] not in cycle:
                        print(-1)
                        return
                
                print(fmin(a, b) + 1, fmax(a, b) + 1)
                return

    
    print(-1)

for testcase in range(1):
    solve(testcase)