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
    n = II()
    grid = [[0 for _ in range(n)] for _ in range(1 << n)]
    for i in range(1 << n):
        line = LII()
        for j in range(n):
            grid[i][j] = line[j]
    
    S = set()
    res = 0
    def find(round):
        #print('rrrrrrrrr', round)
        if round == 0:
            return
        nonlocal res, n
        l, r = 0, (1 << round) - 1
        #print(l, r)
        while r < 1 << n:
            #print('lr', l, r)
            if any(s // (1 << round) == l // (1 << round) for s in S):
                l += 1 << round
                r += 1 << round
                continue
            else:
                M = 0
                idx = -1
                for i in range(l, r + 1):
                    if grid[i][round - 1] > M:
                        M = grid[i][round - 1]
                        idx = i
                l += 1 << round
                r += 1 << round
                S.add(idx)
                res += M
        #print('res', res)
        find(round - 1)

    find(n)
    print(res)
for _ in range(1):solve()