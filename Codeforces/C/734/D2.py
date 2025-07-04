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

def solve():
    n, m, k = MI()
    grid = [['.' for _ in range(m)] for _ in range(n)]
    if n & 1:
        if k < m // 2 or (k - m // 2) & 1:
            print('NO')
            return
        else:
            print('YES')
            for i in range(0, m, 2):
                if i >> 1 & 1:
                    grid[-1][i] = grid[-1][i + 1] = 'x'
                else:
                    grid[-1][i] = grid[-1][i + 1] = 'y'
            
            k -= m // 2
            cnt = 0
            for i in range(0, n - 1, 2):
                for j in range(0, m, 2):
                    if cnt < k:
                        cnt += 2
                        if (i // 2 + j // 2) & 1:
                            grid[i][j] = grid[i][j + 1] = 'a'
                            grid[i + 1][j] = grid[i + 1][j + 1] = 'b'
                        else:
                            grid[i][j] = grid[i][j + 1] = 'c'
                            grid[i + 1][j] = grid[i + 1][j + 1] = 'd'
                    else:
                        if (i // 2 + j // 2) & 1:
                            grid[i][j] = grid[i + 1][j] = 'a'
                            grid[i][j + 1] = grid[i + 1][j + 1] = 'b'
                        else:
                            grid[i][j] = grid[i + 1][j] = 'c'
                            grid[i][j + 1] = grid[i + 1][j + 1] = 'd'

    elif m & 1:
        if k > n * (m - 1) // 2 or (n * (m - 1) // 2 - k) & 1:
            print('NO')
            return
        else:
            print('YES')
            for i in range(0, n, 2):
                if i >> 1 & 1:
                    grid[i][-1] = grid[i + 1][-1] = 'x'
                else:
                    grid[i][-1] = grid[i + 1][-1] = 'y'
            
            cnt = 0
            for i in range(0, n, 2):
                for j in range(0, m - 1, 2):
                    if cnt < k:
                        cnt += 2
                        if (i // 2 + j // 2) & 1:
                            grid[i][j] = grid[i][j + 1] = 'a'
                            grid[i + 1][j] = grid[i + 1][j + 1] = 'b'
                        else:
                            grid[i][j] = grid[i][j + 1] = 'c'
                            grid[i + 1][j] = grid[i + 1][j + 1] = 'd'
                    else:
                        if (i // 2 + j // 2) & 1:
                            grid[i][j] = grid[i + 1][j] = 'a'
                            grid[i][j + 1] = grid[i + 1][j + 1] = 'b'
                        else:
                            grid[i][j] = grid[i + 1][j] = 'c'
                            grid[i][j + 1] = grid[i + 1][j + 1] = 'd'
    else:
        if k & 1:
            print('NO')
            return
        else:
            print('YES')
            cnt = 0
            for i in range(0, n, 2):
                for j in range(0, m, 2):
                    if cnt < k:
                        cnt += 2
                        if (i // 2 + j // 2) & 1:
                            grid[i][j] = grid[i][j + 1] = 'a'
                            grid[i + 1][j] = grid[i + 1][j + 1] = 'b'
                        else:
                            grid[i][j] = grid[i][j + 1] = 'c'
                            grid[i + 1][j] = grid[i + 1][j + 1] = 'd'
                    else:
                        if (i // 2 + j // 2) & 1:
                            grid[i][j] = grid[i + 1][j] = 'a'
                            grid[i][j + 1] = grid[i + 1][j + 1] = 'b'
                        else:
                            grid[i][j] = grid[i + 1][j] = 'c'
                            grid[i][j + 1] = grid[i + 1][j + 1] = 'd'
    
    for i in range(n):
        print(''.join(grid[i]))


for _ in range(II()):solve()