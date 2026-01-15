'''
Hala Madrid!
https://github.com/USYDDonghaoLi/Programming_Competition
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



# @TIME
def solve(testcase):
    n = II()
    adj = [[] for _ in range(n)]
    deg = [0 for _ in range(n)]

    for _ in range(n):
        u, v = GMI()
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1
    
    vis = [False for _ in range(n)]
    rest = n
    q = deque()
    for i in range(n):
        if deg[i] == 1:
            q.append(i)
            vis[i] = True
    
    # try:
    #     st = deg.index(3)
    # except:
    #     st = 0
    st = 0
    
    while q:
        u = q.popleft()
        rest -= 1
        for v in adj[u]:
            deg[v] -= 1
            if not vis[v]:
                if deg[v] == 1:
                    vis[v] = True
                    q.append(v)
                else:
                    st = v
    
    # print("st", st)

    res = [-1 for _ in range(n)]
    # print("st", st)
    flag = vis[:]


    q = deque()
    for i in range(n):
        if not vis[i]:
            q.append(i)
    
    res[st] = 1
    vis[st] = True
    # print("res", res)
    # q = deque()
    # q.append(st)
    # while q:
    #     u = q.popleft()
    #     for v in adj[u]:
    #         if vis[v] and res[v] == -1:
    #             res[v] = (res[u] + 1) % 3
    #             vis[v] = True
    #             q.append(v)
    # u = st
    # for _ in range(n - rest):
    #     for v in adj[u]:
    #         if vis[v] and res[v] == -1:
    #             res[v] = (res[u] + 1) % 3
    #             u = v
    #             break

    # print("vis", vis)
    # print("res", res)

    '''
    3n + 1
    RGB...RGB RGR(G)
    3n + 2
    RGB...RGBR(G)
    3n + 3
    RGB...RGBRB(G)
    '''

    # print(*res)
    a, b = divmod(rest, 3)
    if b == 1:
        # print("111", a, b)
        # print("res", res)
        # print("vis", vis)
        u = st
        co = 0
        for _ in range((a - 1) * 3):
            for v in adj[u]:
                if not vis[v] and res[v] == -1:
                    # print("GO", u, v)
                    vis[v] = True
                    res[v] = co
                    co = (co + 1) % 3
                    u = v
                    break
        CO = "010"
        idx = 0
        for _ in range((a - 1) * 3, rest - 1):
            for v in adj[u]:
                # print("GO", u, v, not vis[v], res[v] == -1)
                if not vis[v] and res[v] == -1:
                    vis[v] = True
                    res[v] = int(CO[idx])
                    idx += 1
                    u = v
                    break
        
    
    elif b == 2:
        # print("st", st)
        u = st
        co = 0
        for _ in range(a * 3):
            for v in adj[u]:
                if not vis[v] and res[v] == -1:
                    # print("GO", u, v)
                    vis[v] = True
                    res[v] = co
                    co = (co + 1) % 3
                    u = v
                    break
        
        # print(u, v, res)

        CO = "0"
        idx = 0
        for _ in range(a * 3, rest - 1):
            for v in adj[u]:
                if not vis[v] and res[v] == -1:
                    # print("GO", u, v)
                    vis[v] = True
                    res[v] = int(CO[idx])
                    idx += 1
                    u = v
                    break
    else:
        # print("333", a, b)
        u = st
        co = 0
        for _ in range((a - 1) * 3):
            for v in adj[u]:
                if not vis[v] and res[v] == -1:
                    vis[v] = True
                    res[v] = co
                    co = (co + 1) % 3
                    u = v
                    break
        # print((a - 1) * 3, rest - 1)
        CO = "02"
        idx = 0
        for _ in range((a - 1) * 3, rest - 1):
            for v in adj[u]:
                if not vis[v] and res[v] == -1:
                    # print("GO", u, v)
                    vis[v] = True
                    res[v] = int(CO[idx])
                    idx += 1
                    u = v
                    break
    
    while q:
        u = q.popleft()
        for v in adj[u]:
            if flag[v] and res[v] == -1:
                res[v] = (res[u] + 1) % 3
                q.append(v)

    for u in range(n):
        for v in adj[u]:
            assert res[u] != res[v]
    
    for i in range(n):
        res[i] += 1
    
    print(*res)

for testcase in range(1):
    solve(testcase)