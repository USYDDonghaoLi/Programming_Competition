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

def get_divisors(num):
    if num <= 0:
        return []
    divs = []
    i = 1
    while i * i <= num:
        if num % i == 0:
            divs.append(i)
            if i * i != num:
                divs.append(num // i)
        i += 1
    return divs

def solve(testcase):
    n, k = MI()
    A = LII()

    if n == 1 or all(a == A[0] for a in A):
        print(k, k * (k + 1) // 2)
        return
    min_d = inf
    best = -1
    for i in range(n - 1):
        d = abs(A[i] - A[i + 1])
        if 0 < d < min_d:
            min_d = d
            best = i

    m = min(A[best], A[best + 1])
    candidates = set()
    for div in get_divisors(min_d):
        x = div - m
        if 1 <= x <= k:
            candidates.add(x)

    cnt = 0
    res = 0
    for x in candidates:
        ok = True
        for i in range(n - 1):
            d = abs(A[i] - A[i + 1])
            if d == 0:
                continue
            mi = min(A[i], A[i + 1])
            if d % (mi + x) != 0:
                ok = False
                break
        if ok:
            cnt += 1
            res += x

    print(cnt, res)


for testcase in range(II()):
    solve(testcase)