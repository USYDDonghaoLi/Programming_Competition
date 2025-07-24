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

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

# @TIME
def solve(testcase):
    n, k = MI()
    A = LII()

    leaves = [0 for _ in range(n)]
    mp = [[] for _ in range(n)]

    adj = [[] for _ in range(n)]

    for _ in range(n - 1):
        u, v = GMI()
        adj[u].append(v)
        adj[v].append(u)
    
    @bootstrap
    def dfs(u, fa):
        cnt = 0
        for v in adj[u]:
            if v != fa:
                cnt += 1
                yield dfs(v, u)
                leaves[u] += leaves[v]
        
        if not cnt:
            leaves[u] = 1

        mp[u] = [0 for _ in range(fmin(leaves[u], k) + 1)]

        cur = 0

        for v in adj[u]:
            if v != fa:
                for i in range(cur, -1, -1):
                    for j in range(leaves[v] + 1):
                        if i + j >= len(mp[u]):
                            break
                        mp[u][i + j] = fmax(mp[u][i + j], mp[u][i] + mp[v][j])
                cur += leaves[v]

                # m = leaves[v]
                # rightmost = fmin(cur + m, len(mp[u]) - 1)
                # leftmost = 0
                

                # for t in range(rightmost, leftmost - 1, -1):
                #     for idx in range(fmax(cur - t, 1), fmin(len(mp[v]) - 1, t) + 1):
                #         mp[u][t] = fmax(mp[u][t], mp[v][idx] + mp[u][t - idx])
                

                # cur += m
        
        try:
            mp[u][leaves[u]] += A[u]
        except:
            pass

        yield None
    
    dfs(0, -1)

    print(mp[0][k])

for testcase in range(1):
    solve(testcase)