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

inf = float('inf')
fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

mod = 10 ** 9 + 7

class Factorial:
    def __init__(self, N, mod) -> None:
        self.mod = mod
        self.f = [1] * N
        self.g = [1] * N
        for i in range(1, N):
            self.f[i] = self.f[i - 1] * i % mod
        self.g[-1] = pow(self.f[-1], mod - 2, mod)
        for i in range(N - 2, -1, -1):
            self.g[i] = self.g[i + 1] * (i + 1) % mod

    def comb(self, n, m):
        if n < m or n < 0 or m < 0:
            return 0
        return self.f[n] * self.g[m] % self.mod * self.g[n - m] % self.mod

F = Factorial(2010, mod)

pw2 = [1] * 2010
inv2 = pow(2, mod - 2, mod)
inv_pw2 = [1] * 2010
for i in range(1, 2010):
    pw2[i] = pw2[i - 1] * 2 % mod
    inv_pw2[i] = inv_pw2[i - 1] * inv2 % mod

def solve(testcase):
    n = II()
    A = LII()

    pos = defaultdict(list)
    for i, v in enumerate(A):
        pos[v].append(i)

    res = 0

    for k in range(n):
        # L[i] = C(i, k), R[j] = C(n-j-1, k)
        L = [0] * n
        R = [0] * n
        for i in range(k, n):
            L[i] = F.comb(i, k)
        for j in range(n):
            right = n - j - 1
            if right >= k:
                R[j] = F.comb(right, k)

        pref = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = (pref[i] + L[i] * inv_pw2[i]) % mod

        total = 0
        for j in range(1, n):
            if R[j] == 0:
                continue
            total = (total + pref[j] * pw2[j - 1] % mod * R[j]) % mod

        same = 0
        for v, p in pos.items():
            m = len(p)
            if m < 2:
                continue
            pref_v = [0] * (m + 1)
            for idx in range(m):
                i = p[idx]
                pref_v[idx + 1] = (pref_v[idx] + L[i] * inv_pw2[i]) % mod

            for idx in range(1, m):
                j = p[idx]
                if R[j] == 0:
                    continue
                same = (same + pref_v[idx] * pw2[j - 1] % mod * R[j]) % mod

        res = (res + total - same) % mod

    print(res)

for testcase in range(1):
    solve(testcase)