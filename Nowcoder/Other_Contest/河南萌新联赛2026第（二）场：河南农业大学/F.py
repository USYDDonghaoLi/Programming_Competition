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
    
    n = II()
    A = LII()

    B = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = GMI()
        B[u].append(v)
        B[v].append(u)
    
    Child = [[] for _ in range(n)]
    q = deque()
    q.append((0, -1))
    while q:
        u, p = q.popleft()
        for v in B[u]:
            if v == p:
                continue
            Child[u].append(v)
            q.append((v, u))
    
    def f(mid):
        C = [A[i] - mid for i in range(n)]

        D = [0 for _ in range(n)]

        flag = False

        @bootstrap
        def dfs(u):
            nonlocal flag
            M1, M2 = -inf, -inf
            if not Child[u]:
                D[u] = C[u]
                yield None
                return
            
            for v in Child[u]:
                yield dfs(v)
                if D[v] > M1:
                    M2 = M1
                    M1 = D[v]
                elif D[v] > M2:
                    M2 = D[v]
            
            if M2 == -inf:
                val = C[u] + M1
                if val >= 0:
                    flag = True
                D[u] = fmax(val, C[u])
                

            else:
                val = fmax(C[u] + M1 + M2, C[u] + M1)
                if val >= 0:
                    flag = True
                D[u] = fmax(C[u] + M1, C[u])
            yield None

        dfs(0)

        return flag


    l, r = 0, 10 ** 9 + 10
    while r - l > 2e-4:
        mid = (l + r) / 2
        if f(mid):
            l = mid
        else:
            r = mid
    
    # print(f(8))

    print(f"{l:.2f}")

for testcase in range(II()):
    solve(testcase)