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

'''
手写栈防止recursion limit
注意要用yield 不要用return
函数结尾要写yield None
'''
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

mod = 998244353
inv2 = pow(2, mod - 2, mod)

def ask():
    pass

def answer():
    pass

def solve(testcase):
    n, m = MI()
    A = LII()
    adj = defaultdict(list)
    edges = []
    for _ in range(1, n):
        a, b = MI()
        adj[a].append(b)
        adj[b].append(a)
        edges.append((a, b))
    
    prob = [0 for _ in range(n + 1)]
    for a in A:
        prob[a] = 1
    
    parent = [0 for _ in range(n + 1)]
    TOT = [0 for _ in range(n + 1)]
    @bootstrap
    def dfs(node, p):
        parent[node] = p
        ret = prob[node]
        for o in adj[node]:
            if o == p:
                continue
            else:
                yield dfs(o, node)
                ret += TOT[o]
        TOT[node] = ret
        yield None
    
    dfs(1, 0)
    res = 0

    for x, y in edges:
        '''
        x -> y
        '''
        if parent[x] == y:
            x, y = y, x
        upper, lower = m - TOT[y], TOT[y]

        p, q = prob[x], prob[y]
        tt, tf, ft, ff = p * q % mod, p * (1 - q) % mod, (1 - p) * q % mod, (1 - p) * (1 - q) % mod
        stay = (tt + ff + (tf + ft) * inv2) % mod
        x2y = tf * inv2 % mod
        y2x = ft * inv2 % mod

        res += upper * lower * stay % mod
        res += (upper - 1) * (lower + 1) * x2y % mod
        res += (upper + 1) * (lower - 1) * y2x % mod

        prob[x] = prob[y] = (prob[x] + prob[y]) * inv2 % mod
    
    print(res * pow(m * (m - 1) // 2, mod - 2, mod) % mod)

for testcase in range(1):
    solve(testcase)