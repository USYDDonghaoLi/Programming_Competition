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

class Recoverable_UnionFind:

    def __init__(self, n):
        self.n = n
        self.parent = [i for i in range(self.n)]
        self.size = [1 for _ in range(self.n)]
        self.operation = []
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
        self.operation.append((root_y, root_x))
        self.setCount -= 1
        return True

    def current(self):
        return len(self.operation)

    def rollback(self, history):
        while len(self.operation) > history:
            a, b = self.operation.pop()
            self.parent[b] = b
            self.size[a] -= self.size[b]
            self.setCount += 1

def f(u, v):
    return v << 20 ^ u

# @TIME
def solve(testcase):
    n, m = MI()
    # adj = [[] for _ in range(n)]

    edges = []

    mp = defaultdict(list)

    for i in range(m):
        u, v, w = MI()
        u -= 1
        v -= 1
        # adj[u].append((v, w))
        # adj[v].append((u, w))
        edges.append((u, v, w))
        mp[w].append(i)
    
    UF = UnionFind(n)
    '''
    编号为i的边能不能成为最小生成树的一部分（能不能把两个连通块连接起来）
    前提是比它权重小的边都试过了
    '''
    A = [0 for _ in range(m)]
    mp2 = defaultdict(int)

    for weight in sorted(mp.keys()):
        for ID in mp[weight]:
            u, v, w = edges[ID]
            mp2[f(u, w)] = UF.Find(u)
            mp2[f(v, w)] = UF.Find(v)
            A[ID] = UF.Find(u) != UF.Find(v)
        
        for ID in mp[weight]:
            u, v, w = edges[ID]
            UF.Union(u, v)
    
    q = II()
    RUF = Recoverable_UnionFind(n)

    for _ in range(q):
        B = LII()[1:]
        k = len(B)
        flag = True

        for i in range(k):
            B[i] -= 1
            '''
            A[B[i]] = False: 不可能是最小生成树的一部分
            '''
            flag &= A[B[i]]
        
        '''
        判断是否同在一个连通块
        '''
        for i in range(k - 1):
            flag &= UF.Find(edges[B[i]][0]) == UF.Find(edges[B[i + 1]][0])
        
        if flag:
            tmp = defaultdict(list)
            for b in B:
                u, v, w = edges[b]
                tmp[w].append(b)
            
            '''
            从小到大遍历每个w, 对于每个w, 判断这条边加上以后，可撤销并查集中是否会生成环
            su, sv的意义是假设比w小的权重的边都考虑过了
            '''
            
            for w in sorted(tmp.keys()):
                RUF.rollback(0)
                for ID in tmp[w]:
                    u, v, w = edges[ID]
                    su = mp2[f(u, w)]
                    sv = mp2[f(v, w)]
                    flag &= RUF.Find(su) != RUF.Find(sv)

                    if not flag:
                        break

                    RUF.Union(su, sv)
        
        print('YES' if flag else 'NO')


for testcase in range(1):
    solve(testcase)