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
#dfs - stack#

def solve():
    n = II()
    cur = [[0 for _ in range(n)] for _ in range(2)]
    target = [[0 for _ in range(n)] for _ in range(2)]

    cnt = 0
    for i in range(2):
        line = LII()
        for j in range(n):
            cur[i][j] = line[j]
            if line[j]:
                cnt += 1
    
    for i in range(2):
        line = LII()
        for j in range(n):
            target[i][j] = line[j]
            if line[j]:
                cnt -= 1
    
    if cnt != 0:
        print(-1)
    else:
        top, bottom = 0, 0
        res = 0
        for i in range(n):
            a, b, c, d = cur[0][i], cur[1][i], target[0][i], target[1][i]

            if a == 1 and c == 0:
                top += 1
            if a == 0 and c == 1:
                top -= 1
            if b == 1 and d == 0:
                bottom += 1
            if b == 0 and d == 1:
                bottom -= 1
            
            if top > 0 and bottom < 0:
                top -= 1
                bottom += 1
                res += 1
            
            if top < 0 and bottom > 0:
                top += 1
                bottom -= 1
                res += 1
            
            res += abs(top) + abs(bottom)
        print(res)
solve()