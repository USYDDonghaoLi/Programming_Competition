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
from math import log, gcd, sqrt

def solve():
    n, m = MI()
    points = []
    for _ in range(n + m):
        x, y = MI()
        points.append((x, y))
    points.append((0, 0))

    dist = [[0 for _ in range(n + m)] for _ in range(n + m + 1)]
    for i in range(n + m + 1):
        x1, y1 = points[i]
        for j in range(n + m):
            x2, y2 = points[j]
            dist[i][j] = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    
    dp = [[float('inf') for _ in range(n + m)] for _ in range(1 << n + m)]
    for i in range(n + m):
        dp[1 << i][i] = dist[-1][i]

    mask = ((1 << m) - 1) << n
    for state in range(1, 1 << n + m):
        for i in range(n + m):
            if not state >> i & 1:
                continue
            t = (state ^ (1 << i)) & mask
            speed = 1
            while t:
                speed *= 0.5
                t -= t & (-t)
            for j in range(n + m):
                if (state ^ (1 << i)) >> j & 1:
                    dp[state][i] = min(dp[state][i], dp[state ^ (1 << i)][j] + dist[i][j] * speed)
    
    res = float('inf')
    final = (1 << n) - 1
    for state in range(1, 1 << n + m):
        if ~state & final:
            continue
        t = state & mask
        speed = 1
        while t:
            speed *= 0.5
            t -= t & (-t)

        for i in range(n + m):
            if not state >> i & 1:
                continue

            res = min(res, dp[state][i] + dist[-1][i] * speed)
    
    print(res)

for _ in range(1):solve()