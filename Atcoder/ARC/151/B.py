'''
Hala Madrid!
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
from math import log, gcd

mod = 998244353

class UnionFind:
    def __init__(self, n: int):
        self.parent = [x for x in range(n)]
        self.size = [1 for _ in range(n)]
        self.n = n
        self.setCount = n
    
    def Find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.Find(self.parent[x])
        return self.parent[x]
    
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

class Factorial:
    def __init__(self, N, mod) -> None:
        self.mod = mod
        self.f = [1 for _ in range(N)]
        self.g = [1 for _ in range(N)]
        for i in range(1, N):
            self.f[i] = self.f[i - 1] * i % self.mod
        self.g[-1] = pow(self.f[-1], mod - 2, mod)
        for i in range(N - 2, -1, -1):
            self.g[i] = self.g[i + 1] * (i + 1) % self.mod
    
    def comb(self, n, m):
        return self.f[n] * self.g[m] % self.mod * self.g[n - m] % self.mod
    
    def perm(self, n, m):
        return self.f[n] * self.g[n - m] % self.mod

fact = Factorial(2 * 10 ** 5 + 10, mod)

def solve():
    n, m = MI()
    p = [0] + LII()
    res = 0
    uf = UnionFind(n + 10)
    
    pw = [1 for _ in range(n + 10)]
    for i in range(1, n + 10):
        pw[i] = pw[i - 1] * m % mod
    
    tot = 0
    S = set()
    for i in range(1, n + 1):
        S.add(i)
    
    for i in range(1, n + 1):
        if i == p[i]:
            tot += 1
            S.discard(i)
            continue
        
        tmp = 0
        if uf.size[uf.Find(i)] == 1 and uf.size[uf.Find(p[i])] == 1:
            uf.Union(i, p[i])
            tmp = m * (m - 1) // 2
            tmp %= mod
            tmp *= pw[tot]
            tmp %= mod
            S.discard(i)
            S.discard(p[i])
            tmp *= pw[len(S)]
            tmp %= mod
            tot += 1
        elif uf.size[uf.Find(i)] == 1:
            uf.Union(i, p[i])
            tmp = m * (m - 1) // 2
            tmp %= mod
            tmp *= pw[tot - 1]
            tmp %= mod
            S.discard(i)
            tmp *= pw[len(S)]
            tmp %= mod
        elif uf.size[uf.Find(p[i])] == 1:
            uf.Union(i, p[i])
            tmp = m * (m - 1) // 2
            tmp %= mod
            tmp *= pw[tot - 1]
            tmp %= mod
            S.discard(p[i])
            tmp *= pw[len(S)]
            tmp %= mod
        else:
            if not uf.Union(i, p[i]):
                tot -= 1
        
        res += tmp
        res %= mod
        print(i, tmp, res, tot)
    print(res)

for _ in range(1):solve()

