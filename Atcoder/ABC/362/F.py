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
    
    # print(adj)
        
    FA = [-1 for _ in range(n)]
    SZ = [1 for _ in range(n)]
    
    @bootstrap
    def dfs(cur, fa):
        for o in adj[cur]:
            if o != fa:
                yield dfs(o, cur)
                FA[o] = cur
                SZ[cur] += SZ[o]
        
        yield None
    
    dfs(0, -1)
    
    # print('FA', FA)
    # print('SZ', SZ)
    
    SUB = [[] for _ in range(n)]
    
    @bootstrap
    def dfs2(cur, fa):
        if cur:
            SUB[cur].append((n - SZ[cur], fa))
        for o in adj[cur]:
            if o != fa:
                SUB[cur].append((SZ[o], o))
                yield dfs2(o, cur)
        yield None
    
    dfs2(0, -1)
    
    # print('SUB', SUB)
    
    rt = -1
    
    for i in range(n):
        M = 0
        for sz, o in SUB[i]:
            if sz > M:
                M = sz
        if M <= n - M:
            rt = i
            break
        if rt != -1:
            break
    
    # print('rt: ', rt, 'branch: ', branch)
    
    nodes = defaultdict(list)
    nodes[rt] = [rt]
    depth = [0 for _ in range(n)]
    
    q = deque()
    for o in adj[rt]:
        q.append((o, rt, o))
        depth[o] = 1
    
    while q:
        cur, fa, ancestor = q.popleft()
        nodes[ancestor].append(cur)
        for o in adj[cur]:
            if o != fa:
                q.append((o, cur, ancestor))
                depth[o] = depth[cur] + 1
    
    # print('nodes', nodes)
    
    pq = []
    for o in nodes:
        heappush(pq, (-len(nodes[o]), -depth[nodes[o][-1]], o))
    
    res = []
    while len(pq) >= 2:
        a1, _, o1 = heappop(pq)
        a2, _, o2 = heappop(pq)
        
        res.append((nodes[o1].pop(), nodes[o2].pop()))
        a1 += 1
        if a1:
            heappush(pq, (a1, -depth[nodes[o1][-1]], o1))
        a2 += 1
        if a2:
            heappush(pq, (a2, -depth[nodes[o2][-1]], o2))
    
    for u, v in res:
        print(u + 1, v + 1)

for testcase in range(1):
    solve(testcase)