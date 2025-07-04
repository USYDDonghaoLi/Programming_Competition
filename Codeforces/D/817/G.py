from re import A
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
    res = [0 for _ in range(n)]

    if n == 3:
        print(*[2, 1, 3])
        return

    x, y = 101, 103
    q, r = divmod(n, 4)
    if r == 0:
        for i in range(n):
            if i % 4 == 0:
                res[i] = x
                res[i + 2] = x - 1
                x += 4
            elif i % 4 == 1:
                res[i] = y
                res[i + 2] = y - 1
                y += 4

    elif r == 1:
        res[:5] = [2, 0, 5, 4, 3]
        for i in range(5, n):
            if i % 4 == 1:
                res[i] = x
                res[i + 2] = x - 1
                x += 4
            elif i % 4 == 2:
                res[i] = y
                res[i + 2] = y - 1
                y += 4
    elif r == 2:
        res[:6] = [4, 1, 2, 12, 3, 8]
        for i in range(6, n):
            if i % 4 == 2:
                res[i] = x
                res[i + 2] = x - 1
                x += 4
            elif i % 4 == 3:
                res[i] = y
                res[i + 2] = y - 1
                y += 4
    elif r == 3:
        res[:7] = [1, 2, 3, 4, 5, 6, 7]
        for i in range(7, n):
            if i % 4 == 3:
                res[i] = x
                res[i + 2] = x - 1
                x += 4
            elif i % 4 == 0:
                res[i] = y
                res[i + 2] = y - 1
                y += 4

    #print(*res)

    e, o = 0, 0
    for i in range(n):
        if i & 1:
            e ^= res[i]
        else:
            o ^= res[i]
    
    print(e, o, e == o)
for _ in range(II()):solve()

