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
    b, k, sx, sy, gx, gy = MI()
    ss = []
    gg = []

    q, r = divmod(sx, b)
    if not r:
        ss.append((q * b, sy))
    else:
        ss.append((q * b, sy))
        ss.append(((q + 1) * b, sy))
    
    q, r = divmod(gx, b)
    if not r:
        gg.append((q * b, gy))
    else:
        gg.append((q * b, gy))
        gg.append(((q + 1) * b, gy))
    
    q, r = divmod(sy, b)
    if not r:
        ss.append((sx, q * b))
    else:
        ss.append((sx, q * b))
        ss.append((sx, (q + 1) * b))
    
    q, r = divmod(gy, b)
    if not r:
        gg.append((gx, q * b))
    else:
        gg.append((gx, q * b))
        gg.append((gx, (q + 1) * b))

    def d(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    print(ss)
    print(gg)

    res = float('inf')
    for x1, y1 in ss:
        for x2, y2 in gg:
            res = min(res, d(x1, y1, sx, sy) * k + d(x1, y1, x2, y2) + d(x2, y2, gx, gy) * k)
            print(x1, y1, x2, y2, res)
    if sx // b == gx // b and sy // b == gy // b:
        res = min(res, d(sx, sy, gx, gy) * k)
    print(res)
for _ in range(II()):solve()