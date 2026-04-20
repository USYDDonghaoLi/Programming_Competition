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

inf = float('inf')

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

def solve(testcase):
    n = II()
    to_ = LGMI()
    deg = [0] * n
    for x in to_:
        deg[x] += 1
    sz = [1] * n
    q = deque()
    for i in range(n):
        if deg[i] == 0:
            q.append(i)
    c = [True] * n
    while q:
        u = q.popleft()
        c[u] = False
        v = to_[u]
        sz[v] += sz[u]
        deg[v] -= 1
        if deg[v] == 0:
            q.append(v)
    MOD = 998244353
    pow25 = [1] * (n + 1)
    for i in range(1, n + 1):
        pow25[i] = pow25[i - 1] * 25 % MOD
    vis = [False] * n
    ans = 1
    for i in range(n):
        if c[i] and not vis[i]:
            cycle = []
            cur = i
            while not vis[cur]:
                vis[cur] = True
                cycle.append(cur)
                cur = to_[cur]
            num = len(cycle)
            x = 1
            for e in cycle:
                x = x * pow25[sz[e] - 1] % MOD
            y = (pow25[num] + (MOD - 25 if num & 1 else 25)) % MOD
            ans = ans * x % MOD * y % MOD
    print(ans)

for testcase in range(1):
    solve(testcase)