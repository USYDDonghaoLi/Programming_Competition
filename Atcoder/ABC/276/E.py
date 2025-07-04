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

d = ((1, 0), (0, 1), (-1, 0), (0, -1))

def solve():
    n, m = MI()
    grid = [['' for _ in range(m)] for _ in range(n)]
    sx, sy = -1, -1
    for i in range(n):
        line = I()
        for j in range(m):
            grid[i][j] = line[j]
            if line[j] == 'S':
                sx, sy = i, j
    
    color = [[set() for _ in range(m)] for _ in range(n)]
    q = deque()
    for i in range(4):
        dx, dy = d[i]
        q.append((sx + dx, sy + dy, i))
    for _ in range(4):
        x, y, c = q.popleft()
        if 0 <= x < n and 0 <= y < m and grid[x][y] == '.':
            color[x][y].add(c)
            q.append((x, y, c))
    
    while q:
        k = len(q)
        for _ in range(k):
            x, y, c = q.popleft()
            for dx, dy in d:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < m and grid[nx][ny] == '.' and c not in color[nx][ny]:
                    q.append((nx, ny, c))
                    color[nx][ny].add(c)
                    if len(color[nx][ny]) > 1:
                        print('Yes')
                        return
    print('No')
for _ in range(1):solve()