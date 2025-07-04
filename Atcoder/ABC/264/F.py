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
#dfs - stack#
#check top!#

def solve():
    h, w = MI()
    r = LII()
    c = LII()
    grid = [[0 for _ in range(w)] for _ in range(h)]
    for i in range(h):
        line = I()
        for j in range(w):
            if line[j] == '1':
                grid[i][j] == 1
    
    dp = [[float('inf') for _ in range(w)] for _ in range(h)]
    rm = [float('inf') for _ in range(h)]
    cm = [float('inf') for _ in range(w)]
    rm[0] = 0 if grid[0][0] == 1 else c[0]
    cm[0] = 0 if grid[0][0] == 1 else r[0]
    dp[0][0] = min(rm[0], cm[0])

    for j in range(1, w):
        if grid[0][j] == 0:
            dp[0][j] = min(dp[0][j], r[0], cm[j - 1] + c[j])            
        else:
            dp[0][j] = dp[0][j - 1]
        rm[0] = min(rm[0], dp[0][j])
    for i in range(1, h):
        if grid[i][0] == 0:
            dp[i][0] = min(dp[i][0], c[0], rm[i - 1] + r[i])
        else:
            dp[i][0] = dp[i - 1][0]
        cm[0] = min(cm[0], dp[i][0])
    
    print(dp)

    for i in range(1, h):
        for j in range(1, w):
            if dp[i][j] == 0:
                dp[i][j] = min(dp[i][j], rm[i - 1] + r[i], cm[j - 1] + c[j])
            else:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1])
            rm[i] = min(rm[i], dp[i][j])
            cm[j] = min(cm[j], dp[i][j])
    
    print(dp)
    print(dp[-1][-1])

for _ in range(1):solve()

