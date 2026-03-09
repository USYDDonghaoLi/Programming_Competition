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

# @TIME
def solve(testcase):
    n = II()
 
    if n <= 2:
        print(0)
    else:
        path = [[] for _ in range(n)]
    
        for _ in range(n - 1):
            u, v = GMI()
            path[u].append(v)
            path[v].append(u)
    
        parent = [-1] * n
        que = [0]
        col = [0] * n
    
        for u in que:
            for v in path[u]:
                if parent[u] != v:
                    parent[v] = u
                    que.append(v)
                    col[v] = col[u] ^ 1
    
        c0 = col.count(0)
        c1 = col.count(1)
    
        sz0 = [v ^ 1 for v in col]
        sz1 = col[:]
    
        for x in reversed(que):
            if x:
                sz0[parent[x]] += sz0[x]
                sz1[parent[x]] += sz1[x]
        
        mod = 998244353
        
        ans = 0
        
        for i in range(n):
            flg = False
            
            t0, t1 = c0, c1
            if col[i]: t1 -= 1
            else: t0 -= 1
            
            cur = 1
            
            for j in path[i]:
                if parent[j] == i:
                    x, y = sz0[j], sz1[j]
                    t0 -= x
                    t1 -= y
                    
                    v = 0
                    val = pow(x + y, mod - 2, mod)
                    if x == 1:
                        v += val
                    if y == 1:
                        v += val
                    
                    cur = cur * v % mod
                    
                    if x + y != 1:
                        flg = True
            
            x, y = t0, t1
            
            if x + y:
                v = 0
                val = pow(x + y, mod - 2, mod)
                
                if x == 1:
                    v += val
                if y == 1:
                    v += val
                
                cur = cur * v % mod
                
                if x + y != 1:
                    flg = True
            
            if flg:
                ans += cur
                ans %= mod
    
        print(ans * pow(n, mod - 2, mod) % mod)

for testcase in range(1):
    solve(testcase)