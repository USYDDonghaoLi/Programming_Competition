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
#dfs - stack#
#check top!#

def solve():
    n = II()
    A = LII()
    B = LII()

    da = dict()
    db = dict()
    for a in A:
        da[a] = da.get(a, 0) + 1
    for b in B:
        if b in da:
            da[b] -= 1
            if da[b] == 0:
                del da[b]
        else:
            db[b] = db.get(b, 0) + 1
    
    cnta = [0 for _ in range(10)]
    cntb = [0 for _ in range(10)]

    cnt = 0
    for a in da:
        if a < 10:
            cnta[a] += da[a]
        else:
            cnta[int(len(str(a)))] += da[a]
            cnt += da[a]
    
    for b in db:
        if b < 10:
            cntb[b] += db[b]
        else:
            cntb[int(len(str(b)))] += db[b]
            cnt += db[b]

    for i in range(1, 10):
        m = min(cnta[i], cntb[i])
        cnta[i] -= m
        cntb[i] -= m
    
    cnt += sum(cnta[2:]) + sum(cntb[2:])
    print(cnt)

for _ in range(II()):solve()

