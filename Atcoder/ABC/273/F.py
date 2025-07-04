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
    n, x = MI()
    Y = LII()
    Z = LII()

    helper = list(sorted(set(Y + Z + [0, x])))
    m = len(helper)
    d = {}
    start, end = -1, -1

    for i, v in enumerate(helper):
        d[v] = i
        if v == 0:
            start = i
        if v == x:
            end = i
    
    Walls = [None for _ in range(m)]
    for i, y in enumerate(Y):
        Walls[d[y]] = i
    
    ans = [float('inf') for _ in range(m)]
    ans[start] = 0
    L = R = start
    while True:
        process = False
        while Walls[L] == None:
            if L - 1 < 0:
                break
            L -= 1
            ans[L] = ans[L + 1] + helper[L + 1] - helper[L]
            process = True
        
        while Walls[R] == None:
            if R + 1 == m:
                break
            R += 1
            ans[R] = ans[R - 1] + helper[R] - helper[R - 1]
            process = True
        
        if L >= 0 and Walls[L] != None:
            h = d[Z[Walls[L]]]
            if ans[h] < float('inf'):
                ans[L] = max(ans[L], ans[h] + abs(helper[L] - helper[h]))
                Walls[L] = None
        
        if R < m and Walls[R] != None:
            h = d[Z[Walls[R]]]
            if ans[h] < float('inf'):
                ans[R] = max(ans[R], ans[h] + abs(helper[R] - helper[h]))
                Walls[R] = None
        
        if not process:
            break
    if ans[end] == float('inf'):
        print(-1)
    else:
        print(ans[end])

for _ in range(1):solve()

