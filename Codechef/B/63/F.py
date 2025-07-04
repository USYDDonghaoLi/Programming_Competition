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

def solve():
    n, m = MI()
    grid = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        line = LII()
        for j in range(m):
            grid[i][j] = line[j]
    
    if n == 1:
        print(max(grid[0]))
        return
    if m == 1:
        print(max(grid[i][0] for i in range(n)))
        return
    
    q = deque()
    v = [[False for _ in range(m)] for _ in range(n)]
    v[-1][-1] = True
    v[-1][-2] = v[-2][-1] = True
    q.append((n - 2, m - 1))
    q.append((n - 1, m - 2))
    step = (n + m) & 1

    dp = [[grid[i][j] for j in range(m)] for i in range(n)]

    while q:
        k = len(q)
        for _ in range(k):
            x, y = q.popleft()
            if not step:
                if x == n - 1:
                    dp[x][y] = max(dp[x][y], dp[x][y + 1])
                elif y == m - 1:
                    dp[x][y] = max(dp[x][y], dp[x + 1][y])
                else:
                    if grid[x][y + 1] > grid[x + 1][y]:
                        dp[x][y] = max(dp[x][y], dp[x][y + 1])
                    else:
                        dp[x][y] = max(dp[x][y], dp[x + 1][y])
            else:
                mn = float('inf')
                for nx, ny in ((x + 1, y), (x, y + 1)):
                    if 0 <= nx < n and 0 <= ny < m:
                        mn = min(mn, dp[nx][ny])
                dp[x][y] = max(dp[x][y], mn)

            for nx, ny in ((x - 1, y), (x, y - 1)):
                if 0 <= nx < n and 0 <= ny < m and not v[nx][ny]:
                    v[nx][ny] = True
                    q.append((nx, ny))
        step ^= 1
    
    print(dp[0][0])
for _ in range(II()):solve()