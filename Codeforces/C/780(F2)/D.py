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
    n = int(input())
    a = list(map(int, input().split()))
    beg = 0
    anssgn = 1
    anslog2 = 0
    ansbeg = n
    ansend = 0
    while beg < n:
        if a[beg] == 0:
            if anssgn == -1:
                anssgn = 0
                anslog2 = 0
                ansbeg = beg
                ansend = n - beg - 1
            beg += 1
            continue
        end = beg
        while end < n and a[end] != 0:
            end += 1
        sgn = 1
        log2 = 0
        for i in range(beg, end):
            if a[i] < 0:
                sgn *= -1
            if abs(a[i]) == 2:
                log2 += 1
            if sgn * (log2 + 1) > anssgn * (anslog2 + 1):
                anssgn = sgn
                anslog2 = log2
                ansbeg = beg
                ansend = n - 1 - i
        sgn = 1
        log2 = 0
        for i in reversed(range(beg, end)):
            if a[i] < 0:
                sgn *= -1
            if abs(a[i]) == 2:
                log2 += 1
            if sgn * (log2 + 1) > anssgn * (anslog2 + 1):
                anssgn = sgn
                anslog2 = log2
                ansbeg = i
                ansend = n - end
        beg = end
    print(ansbeg, ansend)

for _ in range(II()):solve()