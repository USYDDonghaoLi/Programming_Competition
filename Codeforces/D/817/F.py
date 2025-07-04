import sys
import os
from io import BytesIO, IOBase
from tabnanny import check
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
#dfs - stack#
#check top!#

def solve():
    n, m = MI()
    grid = [['' for _ in range(m)] for _ in range(n)]
    v = [[False for _ in range(m)] for _ in range(n)]

    for i in range(n):
        line = I()
        for j in range(m):
            grid[i][j] = line[j]

    d = ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1))

    def check(x, y):
        for di, dj in d:
            chx, chy = x + di, y + dj
            if 0 <= chx < n and 0 <= chy < m and v[chx][chy]:
                return False
        return True

    for i in range(n):
        for j in range(m):
            if grid[i][j] == '*' and not v[i][j]:
                for di, dj in d:
                    chx, chy = i + di, j + dj
                    if 0 <= chx < n and 0 <= chy < m and v[chx][chy]:
                        print('NO')
                        return
                
                if not v[i][j]:
                    nx1, ny1 = i, j + 1
                    nx2, ny2 = i + 1, j + 1
                    if 0 <= nx1 < n and 0 <= nx2 < n and 0 <= ny1 < m and 0 <= ny2 < m and grid[nx1][ny1] == '*' and grid[nx2][ny2] == '*' and check(nx1, ny1) and check(nx2, ny2):
                        v[i][j] = v[nx1][ny1] = v[nx2][ny2] = True
                
                if not v[i][j]:
                    nx1, ny1 = i + 1, j
                    nx2, ny2 = i + 1, j + 1
                    if 0 <= nx1 < n and 0 <= nx2 < n and 0 <= ny1 < m and 0 <= ny2 < m and grid[nx1][ny1] == '*' and grid[nx2][ny2] == '*' and check(nx1, ny1) and check(nx2, ny2):
                        v[i][j] = v[nx1][ny1] = v[nx2][ny2] = True
                
                if not v[i][j]:
                    nx1, ny1 = i + 1, j
                    nx2, ny2 = i + 1, j - 1
                    if 0 <= nx1 < n and 0 <= nx2 < n and 0 <= ny1 < m and 0 <= ny2 < m and grid[nx1][ny1] == '*' and grid[nx2][ny2] == '*' and check(nx1, ny1) and check(nx2, ny2):
                        v[i][j] = v[nx1][ny1] = v[nx2][ny2] = True
                
                if not v[i][j]:
                    nx1, ny1 = i + 1, j
                    nx2, ny2 = i, j + 1
                    if 0 <= nx1 < n and 0 <= nx2 < n and 0 <= ny1 < m and 0 <= ny2 < m and grid[nx1][ny1] == '*' and grid[nx2][ny2] == '*' and check(nx1, ny1) and check(nx2, ny2):
                        v[i][j] = v[nx1][ny1] = v[nx2][ny2] = True

                if not v[i][j]:
                    print('NO')
                    return
    print('YES')

for _ in range(II()):solve()

