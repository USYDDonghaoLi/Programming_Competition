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

N = 200010
s = [0 for _ in range(N)]
x = [None for _ in range(N)]
y = [None for _ in range(N)]

def solve():
    n = II()
    for i in range(n):
        xx, yy = MI()
        x[i] = xx
        y[i] = yy

    for i in range(n + 1):
        x[i + n] = x[i]
        y[i + n] = y[i]
    
    for i in range(2 * n):
        s[i + 1] = s[i] + x[i] * y[i + 1] - x[i + 1] * y[i]
    
    ans = 7 * 10 ** 18
    r = 0
    S = s[n]

    def calc(l, r):
        return s[r] - s[l] + x[r] * y[l] - y[r] * x[l]
    
    for l in range(n):
        while calc(l, r + 1) * 4 <= S:
            r += 1
        ans = min(ans, abs(S - calc(l, r) * 4))
        ans = min(ans, abs(S - calc(l, r + 1) * 4))
    
    print(ans)
solve()
