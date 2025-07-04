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
    h, w, sx, sy = MI()
    rows = defaultdict(lambda : [0, w + 1])
    cols = defaultdict(lambda : [0, h + 1])

    n = II()
    for _ in range(n):
        r, c = MI()
        rows[r].append(c)
        cols[c].append(r)
    
    for r in rows:
        rows[r].sort()
    for c in cols:
        cols[c].sort()

    
    q = II()
    x, y = sx, sy
    for _ in range(q):
        d, l = LI()
        l = int(l)
        if d == 'L':
            idx = bisect_left(rows[x], y) - 1
            left = rows[x][idx]
            y = max(left + 1, y - l)
        elif d == 'R':
            idx = bisect_left(rows[x], y)
            right = rows[x][idx]
            y = min(right - 1, y + l)
        elif d == 'U':
            idx = bisect_left(cols[y], x) - 1
            up = cols[y][idx]
            x = max(up + 1, x - l)
        else:
            idx = bisect_left(cols[y], x)
            down = cols[y][idx]
            x = min(down - 1, x + l)
        print(x, y)

for _ in range(1):solve()

