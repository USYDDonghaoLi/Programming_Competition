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
    n, m = MI()
    grid = [['' for _ in range(m)] for _ in range(n)]

    for i in range(n):
        line = I()
        for j in range(m):
            grid[i][j] = line[j]
    
    #print('grid', grid)
    
    res = 0
    M = 10
    idxi, idxj = -1, -1

    for i in range(n - 1):
        for j in range(m - 1):
            t = 0
            if grid[i][j] == '1':
                t += 1
            if grid[i + 1][j] == '1':
                t += 1
            if grid[i][j + 1] == '1':
                t += 1
            if grid[i + 1][j + 1] == '1':
                t += 1
        
            if t < M:
                M = t
                idxi = i
                idxj = j
    
    if M == 0:
        res += 0
    elif M == 1:
        res += 1
    else:
        res += 2
    
    for i in range(n):
        for j in range(m):
            if (i, j) not in [(idxi, idxj), (idxi + 1, idxj), (idxi, idxj + 1), (idxi + 1, idxj + 1)]:
                if grid[i][j] == '1':
                    res += 1
    
    print(res)

for _ in range(II()):solve()

