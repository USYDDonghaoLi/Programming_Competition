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

mod = 998244353
pw = [1 for _ in range(200010)]
inv = [1 for _ in range(200010)]
for i in range(1, 200010):
    pw[i] = i * i % mod
    inv[i] = pow(pw[i], mod - 2, mod)

class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0 for _ in range(n)]

    def lowbit(self, x):
        return x & (-x)

    def update(self, pos, x):
        while pos < self.n:
            self.tree[pos] += x
            self.tree[pos] %= mod
            pos += self.lowbit(pos)

    def query(self, pos):
        to_ret = 0
        while pos:
            to_ret += self.tree[pos]
            to_ret %= mod
            pos -= self.lowbit(pos)
        return to_ret

    def query_sum(self, l, r):
        return (self.query(r) - self.query(l - 1)) % mod

def solve():
    n = II()
    nums = LII()
    res = [0]

    ft1 = FenwickTree(200010)
    ft2 = FenwickTree(200010)

    for i in range(n):
        ft1.update(nums[i], nums[i])
        ft2.update(nums[i], 1)

        t = res[-1] * pw[i] % mod * inv[i + 1] % mod
        sm = ft2.query_sum(1, nums[i])
        t += (2 * sm - 1) * nums[i] % mod * inv[i + 1] % mod
        t %= mod
        la = ft1.query_sum(nums[i] + 1, 200001)
        t += la * 2 * inv[i + 1] % mod
        t %= mod
        res.append(t)

    for i in range(1, n + 1):
        print(res[i])

for _ in range(1):solve()