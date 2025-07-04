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

    if n == 3:
        grid = [[5, 9, 1], [3, 7, 8], [6, 2, 4]]
        for i in range(3):
            print(*grid[i])
        return

    if n & 1:
        m = n >> 1
        grid[m][m] = 1
        grid[m + 1][m] = n * n - 1
        grid[m][m + 1] = n * n - 2 * n - 1
        grid[m - 1][m + 1] = 2 * n + 1
        v = [False for _ in range(n * n + 1)]
        v[1] = v[n * n - 1] = v[n * n - 2 * n - 1] = v[2 * n + 1] = True

        d = (n + 1) >> 1
        u = d - 1
        cy = 0
        for i in range(2, n * n):
            if v[i]:
                continue
            #print('i', i)
            if cy < m:
                if i & 1:
                    grid[u][cy] = i
                    grid[d][cy] = n * n - i
                else:
                    grid[u][cy] = n * n - i
                    grid[d][cy] = i
            else:
                if i & 1:
                    grid[u - 1][cy] = i
                    grid[d - 1][cy] = n * n - i
                else:
                    grid[u - 1][cy] = n * n - i
                    grid[d - 1][cy] = i
            
            v[i] = v[n * n - i] = True
            cy += 1
            if cy == m:
                cy = m + 2
            if cy == n:
                break
        
        c1, r1 = 0, 0
        c2, r2 = m + 1, m + 1
        for i in range(1, n * n + 1):
            #print(i, v[i], r2, c2)
            if v[i]:
                continue

            if i & 1:
                grid[r1][c1] = i
                c1 += 1
                if c1 == n:
                    r1 += 1
                    c1 = 0
            else:
                grid[r2][c2] = i
                c2 += 1
                if c2 == n:
                    r2 += 1
                    c2 = 0
            v[i] = True
                
    else:
        d = n >> 1
        u = d - 1
        for i in range(1, n + 1):
            if i & 1:
                grid[u][i - 1] = i
                grid[d][i - 1] = n * n - 1 - i
            else:
                grid[d][i - 1] = i
                grid[u][i - 1] = n * n - 1 - i

        r1, c1 = 0, 0
        r2, c2 = d + 1, 0
        for i in range(n + 1, n * (n - 1) - 1):
            if i & 1:
                grid[r1][c1] = i
                c1 += 1
                if c1 == n:
                    r1 += 1
                    c1 = 0
            else:
                grid[r2][c2] = i
                c2 += 1
                if c2 == n:
                    r2 += 1
                    c2 = 0
        
        grid[r1][c1] = n * n - 1
        grid[r2][c2] = n * n
    
    # for i in range(n):
    #     print(*grid[i])

    mp = defaultdict(int)
    for i in range(n):
        for j in range(n):
            mp[grid[i][j]] += 1
        
    for i in range(n):
        print(*grid[i])
    
    # for i in range(1, n * n + 1):
    #     if mp[i] != 1:
    #         print(t, i)

for _ in range(1):solve()

