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
#dfs - stack#
#check top!#

def solve():
    n = II()
    grid = [[-1 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        line = LII()
        for j in range(n):
            grid[i][j] = line[j]
    
    dp1 = [[None for _ in range(n)] for _ in range(n)]
    dp1[0][0] = defaultdict(int)
    dp1[0][0][grid[0][0]] = 1

    for i in range(n):
        for j in range(n - i):
            if not i and not j:
                continue
            dp1[i][j] = defaultdict(int)
            if i:
                for c in dp1[i - 1][j]:
                    dp1[i][j][c ^ grid[i][j]] += dp1[i - 1][j][c]
            if j:
                for c in dp1[i][j - 1]:
                    dp1[i][j][c ^ grid[i][j]] += dp1[i][j - 1][c]
    
    dp2 = [[None for _ in range(n)] for _ in range(n)]
    dp2[-1][-1] = defaultdict(int)
    dp2[-1][-1][grid[-1][-1]] = 1

    for i in range(n - 1, -1, -1):
        for j in range(n - 1, n - 2 - i, -1):
            if i == n - 1 and j == n - 1:
                continue
            dp2[i][j] = defaultdict(int)
            if j != n - 1:
                for c in dp2[i][j + 1]:
                    dp2[i][j][c ^ grid[i][j]] += dp2[i][j + 1][c]
            if i != n - 1:
                for c in dp2[i + 1][j]:
                    dp2[i][j][c ^ grid[i][j]] += dp2[i + 1][j][c]
    
    res = 0
    for i in range(n):
        for c in dp1[i][n - 1 - i]:
            res += dp1[i][n - 1 - i][c] * dp2[i][n - 1 - i][c ^ grid[i][n - 1 - i]]
    
    print(res)


for _ in range(1):solve()

